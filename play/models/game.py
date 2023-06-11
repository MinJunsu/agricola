import logging
from functools import reduce
from random import shuffle
from typing import List

from asgiref.sync import sync_to_async

from core.const import FIRST_CHANGE_CARD_NUMBER, LAST_TURN
from core.const import NO_USER
from core.models import Base
from core.redis import connection
from play.enum import CommandType, FieldType
from play.exception import IsNotPlayerTurnException
from play.models.action import Action
from play.models.card import Card
from play.models.field import Field
from play.models.player import Player
from play.models.primary_card import PrimaryCard
from play.models.resource import Resource
from play.models.round_card import RoundCard

"""
게임 정보를 담는 클래스
first: 게임의 선 플레이어
turn: 게임의 턴
"""


class Game(Base):
    _first: int
    _turn: int
    _round: int
    _phase: int
    _players: List[Player]
    _base_cards: List[RoundCard]
    _round_cards: List[RoundCard]
    _primary_cards: List[PrimaryCard]
    _common_resources: Resource

    def __init__(
            self,
            first: int = 0,
            turn: int = 0,
            round: int = 0,
            phase: int = 0,
            common_resources: dict = None,
            players: List[dict] = None,
            actions: List[dict] = None,
            base_cards: List[dict] = None,
            round_cards: List[dict] = None,
            primary_cards: List[dict] = None,
    ):
        # 게임 정보 초기화
        self._first = first
        self._turn = turn
        self._round = round
        self._phase = phase
        self._players = [Player.from_dict(**player) for player in players] if players else []
        self._actions = [Action.from_dict(**action) for action in actions] if actions else []
        self._base_cards = [
            RoundCard.from_dict(**base_card) for base_card in base_cards
        ] if base_cards else RoundCard.initialize_base_cards()
        self._round_cards = [
            RoundCard.from_dict(**round_card) for round_card in round_cards
        ] if round_cards else RoundCard.initialize_round_cards()
        self._primary_cards = [
            PrimaryCard.from_dict(**primary_card) for primary_card in primary_cards
        ] if primary_cards else PrimaryCard.initialize_primary_cards()
        self._common_resources = Resource.from_dict(
            **common_resources) if common_resources else Resource.initialize_common_resource()

    @property
    def action_cards(self) -> List[RoundCard]:
        return self._base_cards + self._round_cards

    # TODO: initialize 실행 시 플레이어에 대한 정보를 어느정도 넣어줄지에 대해서 수정하기
    @classmethod
    async def initialize(cls, players: List[str]) -> 'Game':
        redis = connection()
        cards = redis.hvals('cards')
        job_cards = list(filter(lambda card: "JOB" in card, cards))
        sub_cards = list(filter(lambda card: "SUB_FAC" in card, cards))
        shuffle(job_cards)
        shuffle(sub_cards)

        instance = cls()
        players_instance = [Player(name=player) for player in players]

        for player in players_instance:
            player_cards = job_cards[:7] + sub_cards[:7]
            job_cards = job_cards[7:]
            sub_cards = sub_cards[7:]

            player.set("cards", [Card.from_dict(**eval(card)) for card in player_cards])

        instance.set("players", players_instance)
        instance.increment_resource()

        return instance

    @staticmethod
    def parse_command(command_str: dict) -> tuple[CommandType, str, int, dict]:
        command: CommandType = command_str.get('command', CommandType.ACTION)
        card_number: str = command_str.get('card_number', None)
        player: int = command_str.get('player', NO_USER)
        additional: dict = command_str.get('additional', {})
        return command, card_number, player, additional

    def play(self, command: dict) -> dict:
        # 기본 값 설정 (is_done, command 파싱, 플레이어 행동 수)
        is_done: bool = False
        command, card_number, player, additional = self.parse_command(command)
        logger = logging.getLogger(__name__)
        logger.info(f"command: {command}, card_number: {card_number}, player: {player}, additional: {additional}")

        command = CommandType(command)
        worked = len(list(filter(lambda p: p.get('player') is not None, self.action_cards)))

        # 턴에 맞지 않는 플레이어가 행동을 하려고 할 때 에러를 발생시킴.
        if player != self._turn and command != CommandType.ALWAYS:
            raise IsNotPlayerTurnException

        # FIXME: TEST 환경에서만 주석 처리
        # 오픈되지 않은 라운드 카드에 접근하려하면 에러를 발생시킴.
        # round_card = find_object_or_raise_exception(
        #     array=self._round_cards,
        #     key="card_number", value=card_number
        # )

        # TODO: 라운드 카드 이펙트 적용과 행동 명령 처리 순서 확인 -> 이펙트 처리가 먼저라면 round_card 예외 처리 추가해주어야함.
        # 플레이어의 행동 명령을 받아서 처리한다.
        is_done = Action.run(
            command=command, card_number=card_number, players=self._players,
            action_cards=self.action_cards, turn=self._turn, common_resource=self._common_resources,
            additional=additional, used_round=self._round, round_cards=self._round_cards,
            primary_cards=self._primary_cards
        )

        prev_round = self._round

        # 만약 선을 번경하는 카드를 낸 경우 게임의 선을 변경
        if card_number == FIRST_CHANGE_CARD_NUMBER:
            self._first = self._turn

        # 게임의 정보를 바탕으로 게임의 턴을 변경
        self.change_turn_and_round_and_phase(is_done=is_done, total_worked=worked)

        # 플레이어에 존재하는 라운드 카드들에 적용하는 카드 이펙트들을 적용한다.
        for p in self._players:
            used_cards = filter(lambda c: c.get('is_used'), p.get('cards'))
            [c.run(
                player=p,
                turn=self._turn,
                round_card_number=card_number,
                round_cards=self._round_cards,
                card_number=c.get('card_number'),
                now_round=self._round,
                is_round_start=prev_round != self._round
            ) for c in used_cards]

        # 직업 카드 및 보조 설비 카드에서 제공하는 특정한 이펙트를 적용시킴.
        # 라운드 카드에 존재하는 카드 이펙트들을 전체적으로 적용한다.
        for player_index, resources in self._round_cards[self._round].get('additional_action').items():
            for resource, count in resources.items():
                if count != 0:
                    self._players[int(player_index)].get('resource').set(
                        resource, self._players[int(player_index)].get('resource').get(resource) + count
                    )
                    resources[resource] = 0

        # 게임 스코어 결과 처리 확인 테스트용
        # for p in self._players:
        #     print(p.calculate_score())

        return self.to_dict()

    def increment_resource(self) -> None:
        # FIXME: 라운드 카드 누적 행동칸 처리 시 수정
        # opend_round_cards = self._round_cards
        opend_round_cards = self._round_cards[:self._round + 1]
        stacked_cards = filter(lambda c: c.get('is_stacked'), [*self._base_cards, *opend_round_cards])
        for card in stacked_cards:
            # 리소스 dict 으로부터 특정한 리소스 키를 가져옴.
            resource = list(card.get("resource").keys())[-1]
            common_resource_count = self._common_resources.get(resource)

            # 리소스가 스택되는 상황이며, 공용 자원에서 충분히 배분해줄 수 있는 상황일 때 자원 변경
            if card.get('is_stacked') and common_resource_count - card.get('count') > 0:
                # 리소스는 추가해주고,
                card.get('resource')[resource] += card.get('count')
                self._common_resources.set(resource, common_resource_count - card.get('count'))

    def change_turn_and_round_and_phase(
            self,
            is_done: bool,
            total_worked: int
    ) -> None:
        # 만약, 턴이 끝나지 않은 상태로 온다면 아무것도 하지 않음.
        if not is_done:
            return

        total_family = reduce(lambda acc, player: acc + player.get('resource').get('family'), self._players, 0)

        while total_family != total_worked + 1:
            # for _ in range(10):
            # 우선 턴을 진행 시키고, 이 플레이어가 턴을 진행할 수 있는지 확인한다.
            self._turn += 1

            # 만약, turn이 4 라면, 다시 0으로 변경하여 원형으로 돌 수 있게 한다.
            if self._turn > LAST_TURN:
                self._turn = 0

            # 플레이어가 들고 있는 가족 구성원 수
            player_family = self._players[self._turn].get("resource").get("family")
            # 플레이어가 말판에 이동 시킨 가족 구성원 수 (일한 가족 구성원 수)
            player_worked = len(list(filter(lambda p: p.get('player') == self._turn, self.action_cards)))

            if player_family > player_worked:
                return

        # 만약, 게임 판에 존재하는 모든 플레이어가 가족 구성원들을 사용했다면, 바로 다음 라운드로 변경하는 로직을 진행한다.
        harvest_round = [3, 6, 8, 10, 12, 13]
        if self._round in harvest_round:
            self.harvest()

        self._round = self._round + 1
        self._turn = self._first

        # 누적 행동칸 자원 증가 처리 & 유저 행동칸 이동 처리 초기화
        self.increment_resource()
        [action.set('player', None) for action in self.action_cards]
        return

    @staticmethod
    @sync_to_async
    def get_cards(card_type: str):
        from cards.models import Card
        return list(Card.objects.filter(card_type=card_type).values_list('card_number', flat=True))

    def harvest(self) -> None:
        for player in self._players:
            fields = player.get("fields")
            player_resource = player.get("resource")

            # 농장 단계
            for farm in filter(lambda f: f.get('field_type') == FieldType.FARM, fields):
                resource = farm.get_resource()
                amount = farm.get('is_in').get(resource)
                if amount > 0:
                    farm.get("is_in").set(resource, amount - 1)
                    player.get("resource").set(resource, player_resource.get(resource) + 1)

            # 가족 먹여살리기 단계 - 음식 지불
            player_food = player_resource.get('food')
            player_family = player_resource.get('family')
            cost = player_family * 2
            if player_food > cost:
                player_resource.set("food", player_food - cost)

            # 가족 먹여살리기 단계 - 음식이 부족한 경우
            else:
                player_resource.set(
                    "begging",
                    player_resource.get("begging") + (cost - player_food)
                )
                player_resource.set("food", 0)

            # 번식 단계
            animals = ['cattle', 'boar', 'sheep']
            MAX_BREED = 1
            for animal in animals:
                # 1차 validation: 번식 가능한지 여부 확인
                if player_resource.get(animal) < 2:
                    continue

                # 2차 validation: 번식 가능한 공간이 있는지 여부 확인
                available = list(filter(
                    lambda f: f.get('is_barn') or f.get('field_type') == FieldType.CAGE,
                    player.get('fields')
                ))
                while available:
                    field: Field = available[0]
                    if field.place_or_none(animal, MAX_BREED):
                        player_resource.set(animal, player_resource.get(animal) + MAX_BREED)
                        break
                    available = available[1:]

            # 마무리 단계 - 모든 게임이 종료된 이후 처리
            if self._round == 13:
                # 농장 단계
                for farm in filter(lambda f: f.get('field_type') == FieldType.FARM, fields):
                    resource = farm.get_resource()
                    remain = farm.get('is_in').get(resource)
                    if remain > 0:
                        farm.get("is_in").set(resource, 0)
                        player.get("resource").set(resource, player_resource.get(resource) + remain)
