from typing import List

from core.const import RESOURCE_CONVERT_FUNCTION
from core.models import Base
from core.redis import connection
from play.enum import CommandType
from play.models.player import Player
from play.models.resource import Resource
from play.models.round_card import RoundCard


class Action(Base):
    redis = connection()

    @classmethod
    def run(
            cls,
            command: CommandType,
            card_number: str,
            players: List[Player],
            round_card: RoundCard,
            turn: int,
            common_resource: Resource
    ):
        player: Player = players[turn]
        # card_command = cls.get_command(card_number)
        card_command = cls.convert_resource(player, command, card_number, common_resource, resources)
        if command == CommandType.ACTION:
            return eval(card_command)
        elif command == CommandType.ADDITIONAL:
            pass
        return eval(card_command)

    # 카드를 낼 때 필요한 자원을 가져간다. -> 필요한 자원을 내는 것 뿐이므로 턴이 유지되는 것은 아님
    @staticmethod
    def require(
            player: Player,
            resource: str,
            amount: int
    ) -> bool:
        if player.get("resources").get(resource) < amount:
            raise Exception("자원이 부족합니다.")
        player.get("resources").set(resource, player.get("resources").get(resource) - amount)
        return True

    # 플레이어에게 행동칸에 존재하는 자원을 추가한다.
    @staticmethod
    def plus(
            player: Player,
            resource: str,
            amount: int
    ) -> bool:
        player.get("resource").set(resource, player.get("resource").get(resource) + amount)
        return True

    # 플레이어가 이동한 행동칸에 존재하는 자원을 제거한다.
    @classmethod
    def use_round_card_resources(
            cls,
            player: Player,
            round_card: RoundCard
    ) -> bool:
        is_dones = []
        for resource, amount in round_card.get("resource").items():
            is_dones.append(cls.plus(player, resource, amount))
            round_card.get("resource")[resource] = 0
        return all(is_dones)

    # 플레이어가 직업 카드 혹은 보조 설비 카드를 제출? 선택? 한다.
    @classmethod
    def submit_card(
            cls,
            player: Player,
            round_card: RoundCard
    ) -> bool:
        # 1. 플레이어가 현재 몇장의 카드를 가지고 있는지 확인한다.
        # 2. 플레이어가 가지고 있는 카드의 수가 7장 이상이라면 카드를 제출할 수 없다. (예외 처리)
        # 3. 플레이어가 선택한 행동 칸이 몇개의 자원을 소모하는지 확인한다.
        # 4. 플레이어가 직업 혹은 보조설비 카드를 내기 위해 소모되는 자원이 있는지 확인한다. (require)
        # 5. 플레이어에 선택한 직업 카드의 is_use 속성을 True로 변경한다.
        return True

    @classmethod
    def get_command(cls, card_number: str) -> str:
        return cls.redis.hget("commands", card_number)

    @classmethod
    def convert_resource(
            cls,
            player: Player,
            command: str,
            card_number: str,
            common_resource: Resource,
            resources: dict
    ):
        redis = cls.redis
        TARGET = "food"
        player_resources = player.get("resources")
        for resource, count in resources.items():
            ratio = RESOURCE_CONVERT_FUNCTION[card_number][command][resource]
            count = count * ratio
            # TODO: 1. validate 처리 (플레이어가 자원을 가져갈 수 있는지)
            cls.require(player, resource, count)
            if common_resource.get(TARGET) < count:
                raise Exception("공용 자원이 부족합니다.")

            # TODO: 2 자원 변경 처리
            cls.plus(player, player_resources, count)

        return True
