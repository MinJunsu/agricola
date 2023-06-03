import random
from enum import Enum
from typing import List

from asgiref.sync import sync_to_async

from core.const import FIRST_CHANGE_CARD_NUMBER, LAST_TURN
from core.const import NO_USER
from core.models import Base
from core.redis import connection
from play.models.action import Action
from play.models.player import Player
from play.models.resource import Resource
from play.models.round_card import RoundCard

"""
게임 정보를 담는 클래스
first: 게임의 선 플레이어
turn: 게임의 턴
"""


class CommandType(Enum):
    ACTION = 'action'
    ADDITIONAL = 'additional'
    ALWAYS = 'always'


class Game(Base):
    _first: int
    _turn: int
    _round: int
    _phase: int
    _players: List[Player]
    _actions: List[Action]
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

    # TODO: initialize 실행 시 플레이어에 대한 정보를 어느정도 넣어줄지에 대해서 수정하기
    @classmethod
    async def initialize(cls, players: List[str]) -> 'Game':
        redis = connection()
        cards_v = redis.hvals('cards')
        print(cards_v)
        cards = redis.hkeys('cards')
        t_card = redis.hget('cards', "JOB_01")
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
            player.set("cards", player_cards)

        instance.set("players", players_instance)
        instance.increment_resource()

        return instance

    @staticmethod
    def parse_command(command_str: dict) -> tuple[CommandType, str, int]:
        command: CommandType = command_str.get('command', CommandType.ACTION)
        card_number: str = command_str.get('card_number', None)
        player: int = command_str.get('player', NO_USER)
        return command, card_number, player

    def play(self, command: dict) -> dict:
        # 기본 값 설정
        is_done: bool = False
        command, card_number, player = self.parse_command(command)
        command = CommandType(command)

        if command == CommandType.ACTION and self._turn == int(player):
            # 플레이어의 종료 여부 확인
            is_done = self.player_action(card_number=card_number)

        elif command == CommandType.ADDITIONAL and self._turn == int(player):
            pass

        elif command == CommandType.ALWAYS:
            pass

        # 게임의 정보를 바탕으로 게임의 턴을 변경
        self.change_turn_and_round_and_phase(is_done=is_done)

        # 만약 선을 번경하는 카드를 낸 경우 게임의 선을 변경
        if card_number == FIRST_CHANGE_CARD_NUMBER:
            self._first = self._turn

        return self.to_dict()

    def player_action(self, card_number: str) -> bool:
        redis = connection()
        print(card_number)
        command = redis.hget("commands", card_number)
        print(command)
        # is_done = self._players[self._turn].action(card_number=card_number)
        #
        # # TODO: is_kid 처리 -> Player 정보 중 자식이 있으며, 자식이 움직이는 턴인지 확인
        # self._action_on_round.append(
        #     Action(
        #         card_number=card_number,
        #         player=self._players[self._turn].get('name'),
        #         is_kid=False
        #     )
        # )
        # return is_done
        return False

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
        if not is_done:
            return

        if self._turn == LAST_TURN:
            self._turn = 0
            self._round += 1
            return

    @staticmethod
    @sync_to_async
    def get_cards(card_type: str):
        from cards.models import Card
        return list(Card.objects.filter(card_type=card_type).values_list('card_number', flat=True))
