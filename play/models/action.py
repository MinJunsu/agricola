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

    # "
    def run(self, players: List[Player], common_resources: Resource, turn: int, card_number: str):
        # command: str = self._card.get("command")
        # command = """
        #     require("wood", 1), require("clay", 1), add_effect(["self.action == CARD_005"], ["player.get('resources').set('vegetable', player.get('resources').get('vegetable') + 1)"])
        # """

        # 누적 행동칸: 양시장, 소시장, 서부 채석장 등등...
        command = """
            add("cattle", common_resources.get('cattle'))
        """

        # 노누적 행동칸: 채소종자
        command = """
            add("vegetable", 1)
        """

        # 추가 행동이 필요한 행동칸: 울타리치기, 주요설비
        command = """
            False
        """

        # 추가 행동이 필요한 행동칸 + 뭔가의 행동이 추가: 밭 일구기 + 씨 뿌리기,
        command = """
            self._player.create_farm(position)
        """
        command.replace('position', "[0, 0]")

        # 추가 행동이 필요 없는 칸인데, return True인 행동을 사용하는 경우: 단순 밭 일구기
        command = """
            self._player.create_farm(position), False
        """
        command.replace('position', "[0, 0]")

        # 씨 뿌리기
        command = """
            require(resource, count), self._player.change_field_is_in(position, resource, count)
        """
        command.replace('resource', 'grain')
        command.replace('count', '1')
        command.replace('position', "[0, 0]")

        # 농장 확장
        command = """
        """

        # 집 개조, 농장 개조
        command = """
            require(resource, count), require(resource, count), self._player.remodeling(self._player)
        """
        command.replace('resource', 'reed')
        command.replace('count', '1')
        if self._player.get("_room_type") == "WOOD":
            command.replace('resource', 'wood')
            command.replace('count', 'self._field.get')

        is_done = all(eval(command))

        pass

    # 카드를 낼 때 필요한 자원을 가져간다. -> 필요한 자원을 내는 것 뿐이므로 턴이 유지되는 것은 아님

    def require(self, resource: str, value: int) -> bool:
        if self._player.get("resources").get(resource) < value:
            raise Exception("자원이 부족합니다.")
        self._player.get("resources").set(resource, self._player.get("resources").get(resource) - value)
        return True

    def add(self, resource: str, value: int) -> bool:
        self._player.get("resources").set(resource, self._player.get("resources").get(resource) + value)
        return True
