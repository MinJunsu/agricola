from typing import List

from core.const import FIRST_CHANGE_CARD_NUMBER, LAST_TURN
from core.models import Base
from play.models.action import Action
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
            RoundCard.from_dict(**base_card) for base_card in
            base_cards] if base_cards else RoundCard.initialize_base_cards()
        self._round_cards = [RoundCard.from_dict(**round_card) for round_card in round_cards] if round_cards else []
        self._common_resources = Resource.from_dict(
            **common_resources) if common_resources else Resource.initialize_common_resource()

    # TODO: initialize 실행 시 플레이어에 대한 정보를 어느정도 넣어줄지에 대해서 수정하기
    @classmethod
    def initialize(cls, players: List[str]) -> 'Game':
        instance = cls()
        players_instance = [Player(name=player) for player in players]
        instance.set("players", players_instance)
        instance.increment_resource()
        return instance

    @staticmethod
    def parse_command(command: dict) -> tuple[str, str, int]:
        action: str = command['action']
        card_number: str = command['number']
        player: int = command['player']
        return action, card_number, player

    def play(self, command: dict) -> dict:
        # 기본 값 설정
        is_done: bool = False
        action, card_number, player = self.parse_command(command)

        if action == 'action' and self._turn == int(player):
            # 플레이어의 종료 여부 확인
            is_done = self.player_action(card_number=card_number)

        # 게임의 정보를 바탕으로 게임의 턴을 변경
        self.change_turn_and_round_and_phase(is_done=is_done)

        # 만약 선을 번경하는 카드를 낸 경우 게임의 선을 변경
        if card_number == FIRST_CHANGE_CARD_NUMBER:
            self._first = self._turn
        return self.to_dict()

    def player_action(self, card_number: str) -> bool:
        is_done = self._players[self._turn].action(card_number=card_number)

        # TODO: is_kid 처리 -> Player 정보 중 자식이 있으며, 자식이 움직이는 턴인지 확인
        self._action_on_round.append(
            Action(
                card_number=card_number,
                player=self._players[self._turn].get('name'),
                is_kid=False
            )
        )
        return is_done

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
