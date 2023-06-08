from functools import reduce
from typing import List

from asgiref.sync import sync_to_async

from core.const import FIRST_CHANGE_CARD_NUMBER, LAST_TURN
from core.const import NO_USER
from core.models import Base
from core.redis import connection
from play.enum import CommandType
from play.exception import IsNotPlayerTurnException
from play.models.action import Action
from play.models.card import Card
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
        # job_cards = list(filter(lambda card: "JOB" in card, cards))
        # sub_cards = list(filter(lambda card: "SUB_FAC" in card, cards))
        # shuffle(job_cards)
        # shuffle(sub_cards)
        job_cards = list(filter(lambda card: "JOB_03" in card, cards)) * 28
        sub_cards = list(filter(lambda card: "SUB_FAC" in card, cards))

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
        command = CommandType(command)
        worked = len(list(filter(lambda p: p.get('player') is not None, self.action_cards)))

        # TODO
        # 직업 카드 및 보조 설비 카드에서 제공하는 특정한 이펙트를 적용시킴.

        # 턴에 맞지 않는 플레이어가 행동을 하려고 할 때 에러를 발생시킴.
        if player != self._turn:
            raise IsNotPlayerTurnException

        # 플레이어에 존재하는 라운드 카드들에 적용하는 카드 이펙트들을 적용한다.
        for p in self._players:
            used_cards = filter(lambda c: c.get('is_used'), p.get('cards'))
            [c.run(
                player=p,
                turn=self._turn,
                round_card_number=card_number,
                round_cards=self._round_cards,
                card_number=c.get('card_number'),
                now_round=self._round
            ) for c in used_cards]

        # 플레이어의 행동 명령을 받아서 처리한다.
        is_done = Action.run(
            command=command, card_number=card_number, players=self._players,
            action_cards=self.action_cards, turn=self._turn, common_resource=self._common_resources,
            additional=additional, used_round=self._round, round_cards=self._round_cards
        )

        # 만약 선을 번경하는 카드를 낸 경우 게임의 선을 변경
        if card_number == FIRST_CHANGE_CARD_NUMBER:
            self._first = self._turn

        # 게임의 정보를 바탕으로 게임의 턴을 변경
        self.change_turn_and_round_and_phase(is_done=is_done, total_worked=worked)

        # 라운드 카드에 존재하는 카드 이펙트들을 전체적으로 적용한다.
        for player_index, resources in self._round_cards[self._round].get('additional_action').items():
            for resource, count in resources.items():
                if count != 0:
                    self._players[int(player_index)].get('resource').set(
                        resource, self._players[int(player_index)].get('resource').get(resource) + count
                    )
                    resources[resource] = 0

        return self.to_dict()

    def increment_resource(self) -> None:
        # FIXME: 라운드 카드 누적 행동칸 처리 시 수정
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

            print(player_family)
            print(player_worked)

            if player_family > player_worked:
                return

        # 만약, 게임 판에 존재하는 모든 플레이어가 가족 구성원들을 사용했다면, 바로 다음 라운드로 변경하는 로직을 진행한다.
        # TODO: 라운드 변경 시 페이즈 변경 처리
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
