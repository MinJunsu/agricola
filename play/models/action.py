from typing import List

from core.models import Base
from core.redis import connection
from play.models.card import Card
from play.models.player import Player
from play.models.resource import Resource


class Action(Base):
    _card_number: str
    _turn: int
    _player: Player
    _players: List[Player]

    def __init__(
            self,
            card_number: str,
            turn: int,
    ):
        self._card = card_number
        self._turn = turn

    def run(self, players: List[Player], round_card):
        redis = connection()
        player = players[self._turn]
        self._player = player
        self._players = players
        command = redis.hget("commands", self._card_number)
        self.use_round_card_resources(round_card)
        print(self._player)
        print(round_card)
        is_done = all(eval(command))
        return is_done

    # 카드를 낼 때 필요한 자원을 가져간다. -> 필요한 자원을 내는 것 뿐이므로 턴이 유지되는 것은 아님
    def require(self, player, resource: str, amount: int) -> bool:
        if player.get("resources").get(resource) < amount:
            raise Exception("자원이 부족합니다.")
        player.get("resources").set(resource, player.get("resources").get(resource) - amount)
        return True

    # 플레이어에게 행동칸에 존재하는 자원을 추가한다.
    def plus(self, player, resource: str, amount: int) -> bool:
        player.get("resource").set(resource, player.get("resource").get(resource) + amount)
        return True

    # 플레이어가 이동한 행동칸에 존재하는 자원을 제거한다.
    def use_round_card_resources(self, round_card):
        for resource, amount in round_card.get("resource").items():
            self.plus(self._player, resource, amount)
            round_card.get("resource")[resource] = 0
        return True
