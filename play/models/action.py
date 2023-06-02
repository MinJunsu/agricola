from typing import List

from core.models import Base
from play.models.card import Card
from play.models.player import Player
from play.models.resource import Resource


class Action(Base):
    _card_number: str
    _turn: int

    def __init__(
            self,
            card_number: str,
            turn: int,
    ):
        self._card = card_number
        self._turn = turn

    def run(self, players, round_card):
        player = players[self._turn]

        command = """
            add("resource", "amount")
        """
        command.replace("resource", round_card.get("resource"))
        command.replace("amount", round_card.get("count"))

        is_done = all(eval(command))

        pass

    # 카드를 낼 때 필요한 자원을 가져간다. -> 필요한 자원을 내는 것 뿐이므로 턴이 유지되는 것은 아님
    def require(self, player, resource: str, amount: int) -> bool:
        if player.get("resources").get(resource) < amount:
            raise Exception("자원이 부족합니다.")
        player.get("resources").set(resource, player.get("resources").get(resource) - amount)
        return True

    # add
    # 자원을 추가한다.
    def add(self, player, resource: str, amount: int) -> bool:
        player.get("resources").set(resource, player.get("resources").get(resource) + amount)
        return True

