from typing import List, Any

from core.const import RESOURCE_CONVERT_FUNCTION
from core.functions import find_object_or_raise_exception
from core.models import Base
from core.redis import connection
from play.enum import CommandType
from play.exception import CantUseCardException
from play.models.card import Card
from play.models.field import Field
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
            round_cards: List[RoundCard],
            turn: int,
            common_resource: Resource,
            additional: Any = None,
    ):
        player: Player = players[turn]
        # 데이터 저장을 위해 라운드 카드를 사용한 경우 라운드 카드 변수를 저장한다.
        round_card: RoundCard | None = None
        if "BASE" in card_number or "ROUND" in card_number:
            round_card = find_object_or_raise_exception(round_cards, "card_number", card_number)

            if round_card.get("player") is not None:
                raise CantUseCardException
        cls.require(), cls.condition_check(), cls.submit_card()
        card_command = cls.get_command(card_number)
        
        # 플레이어가 라운드 카드를 선택한 경우 라운드 카드에 플레이어에 대한 정보를 넣어준다.
        if round_card:
            round_card.set("player", turn)

        return eval(card_command)

    # 카드를 낼 때 필요한 자원을 가져간다. -> 필요한 자원을 내는 것 뿐이므로 턴이 유지되는 것은 아님
    @staticmethod
    def require(
            player: Player,
            resource: str,
            amount: int
    ) -> bool:
        if player.get("resource").get(resource) < amount:
            raise Exception("자원이 부족합니다.")
        player.get("resource").set(resource, player.get("resource").get(resource) - amount)
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

    # 플레이어가 직업 카드를 제출? 선택? 한다.
    @classmethod
    def submit_card(
            cls,
            player: Player,
            round_card: RoundCard,
            card_type: str,
            card_number: str
    ) -> bool:
        # card_type = "JOB" | "SUB"
        # Additional Type
        # additional: "JOB_05"
        if card_type == "JOB":
            # 1. 특정한 직업 카드를 가져온다.
            card: Card = find_object_or_raise_exception(array=player.get("cards"), key="card_number", value=card_number)

            # 2. 플레이어가 현재 몇장의 카드를 가지고 있는지 확인한다.
            card_count = len(list(filter(
                lambda c: "JOB" in c.get("card_number") and c.get("is_use"),
                player.get("cards")
            )))

            # 3. 플레이어가 가지고 있는 카드의 수가 7장 이상이라면 카드를 제출할 수 없다. (예외 처리)
            if card_count > 7:
                raise Exception("더 이상 활성화할 수 있는 직업 카드가 없습니다.")

            # 4. 플레이어가 선택한 행동 칸이 몇개의 자원을 소모하는지 확인한다.
            # BASE_05 -> 2 / BASE_11 -> 1 / card_count 0 -> 0
            cost = 0 if card_count == 0 else 1 if round_card.get('card_number') == 'BASE_11' else 2

            # 5. 플레이어가 직업 카드를 내기 위해 소모되는 자원이 있는지 확인한다. (require)
            cls.require(player=player, resource='food', amount=cost)

            # 6. 플레이어에 선택한 직업 카드의 is_use 속성을 True로 변경하고, 카드 효과를 실행한다.
            return card.use(round_card=round_card)

        elif card_type == "SUB":
            # 1. 특정한 보조설비 카드를 가져온다.
            card: Card = find_object_or_raise_exception(array=player.get("cards"), key="card_number", value=card_number)
            
            # 2. 보조설비의 조건을 확인한다.
            card_condition = cls.get_condition(card_number)
            
            # 3. 플레이어가 조건을 만족하는 지 확인한다.
            if eval(card_condition):
            
            # 4. 보조설비의 비용을 확인한다.
                eval(cls.redis.hget("cost", card_number))
            
            # 5. 플레이어가 보조설비를 내기 위해 소모되는 자원이 있는 지 확인한다. (require)
            "위에서 처리된다"
            
            #6. 플레이어가 선택한 보조 설비 카드의 is_use 속성을 True로 변경하고, 카드 효과를 실행한다.
            return card.use(round_card=round_card)
            
        return False

    @classmethod
    def get_command(cls, card_number: str) -> str:
        return cls.redis.hget("commands", card_number)
    
    @classmethod
    def get_condition(cls, card_number: str) -> str:
        return cls.redis.hget("condition", card_number)

    @classmethod
    def convert_resource(
            cls,
            player: Player,
            command: CommandType,
            card_number: str,
            common_resource: Resource,
            resources: dict
    ):
        # TODO: 플레이어가 card_number에 해당하는 카드를 들고 있는지 확인
        TARGET = "food"
        for resource, count in resources.items():
            ratio = RESOURCE_CONVERT_FUNCTION[card_number][command.value][resource]
            # 1. validate 처리 (플레이어가 자원을 가져갈 수 있는지)
            cls.require(player, resource, count)
            if common_resource.get(TARGET) < count * ratio:
                raise Exception("공용 자원이 부족합니다.")
            # 2. 자원 변경 처리
            cls.plus(player, TARGET, count * ratio)
        return True

    # fileds 중 arrival의 position과 자원을 입력받아 새로 선택한 departures의 position에 옮기는 함수
    # client 입력값 (arrival, departures, count)
    @classmethod
    def move_animal(
            cls,
            player: Player,
            additional: dict,
    ):
        # Additional Type
        # {
        #     'animal': 'sheep',
        #     'count': 1,
        #     'departure': 1,
        #     'arrival': 3
        # }
        fields: List[Field] = player.get("fields")

        # TODO: 예외 처리 추가
        # TODO: 동물이 아닌 자원을 이동시킬 수는 없다.

        # 아래 4가지 변수들의 input 값이 정상적인지 확인
        animal = additional.get("animal", None)
        count = additional.get("count", None)
        departure = additional.get("departure", None)
        arrival = additional.get("arrival", None)

        departure_field: Field = find_object_or_raise_exception(array=fields, key="position", value=departure)
        arrival_field: Field = find_object_or_raise_exception(array=fields, key="position", value=arrival)

        departure_field.move(arrival=arrival_field, animal=animal, count=count)
        return False