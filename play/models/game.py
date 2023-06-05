import random
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
        self._common_resources = Resource.from_dict(
            **common_resources) if common_resources else Resource.initialize_common_resource()

    @property
    def action_cards(self) -> List[RoundCard]:
        return self._base_cards + self._round_cards

    def get_action_card_by_card_number(self, card_number: str) -> RoundCard | None:
        cards = list(filter(lambda card: card.get('card_number') == card_number, self.action_cards))
        return cards[0] if cards else None

    # TODO: initialize 실행 시 플레이어에 대한 정보를 어느정도 넣어줄지에 대해서 수정하기
    @classmethod
    async def initialize(cls, players: List[str]) -> 'Game':
        redis = connection()
        cards = redis.hvals('cards')
        job_cards = list(filter(lambda card: "JOB" in card, cards))
        sub_cards = list(filter(lambda card: "SUB_FAC" in card, cards))
        random.shuffle(job_cards)
        random.shuffle(sub_cards)

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
        # 기본 값 설정
        is_done: bool = False
        command, card_number, player, additional = self.parse_command(command)
        command = CommandType(command)

        # 턴에 맞지 않는 플레이어가 행동을 하려고 할 때 에러를 발생시킴.
        if player != self._turn:
            raise IsNotPlayerTurnException

        # 플레이어의 행동 명령을 받아서 처리한다.
        round_card = self.get_action_card_by_card_number(card_number)
        is_done = Action.run(
            command=command, card_number=card_number, players=self._players,
            round_cards=self.action_cards, turn=self._turn, common_resource=self._common_resources,
            additional=additional
        )

        # 게임의 정보를 바탕으로 게임의 턴을 변경
        self.change_turn_and_round_and_phase(is_done=is_done)

        # 만약 선을 번경하는 카드를 낸 경우 게임의 선을 변경
        if card_number == FIRST_CHANGE_CARD_NUMBER:
            self._first = self._turn

        return self.to_dict()

    def increment_resource(self) -> None:
        opend_round_cards = self._round_cards[:self._round]
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

    def change_turn_and_round_and_phase(self, is_done: bool) -> None:
        # 만약, 턴이 끝나지 않은 상태로 온다면 아무것도 하지 않음.
        if not is_done:
            return

        total_family = reduce(lambda acc, player: acc + player.get('resource').get('family'), self._players, 0)
        total_worked = len(list(filter(lambda p: p.get('player') is not None, self.action_cards)))

        while total_family != total_worked:
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
        # 라운드 변경 시 페이즈 변경 처리
        self._round = self._round + 1
        self._turn = self._first
        # 만약, 모든 사람이 할 수 있는 턴이 끝난 상태인지
        return

    @staticmethod
    @sync_to_async
    def get_cards(card_type: str):
        from cards.models import Card
        return list(Card.objects.filter(card_type=card_type).values_list('card_number', flat=True))
