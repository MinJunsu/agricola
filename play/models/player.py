from typing import List

from core.models import Base
from play.models.card import Card
from play.models.field import Field, FieldType
from play.models.resource import Resource


class Player(Base):
    _name: str
    _resource: Resource
    _cards: List[Card]
    _fields: List[Field]

    def __init__(
            self,
            name: str = "",
            resource: dict = None,
            fields: List[dict] = None,
            cards: List[dict] = None,
    ):
        self._name = name
        self._resource = Resource.from_dict(**resource) if resource else Resource.initialize_player_resource()
        self._fields = [Field.from_dict(**field) for field in fields] if fields else Field.initialize()
        self._cards = [Card.from_dict(**card) for card in cards] if cards else []

    # 플레이어 행동 처리 (카드 드로우, 카드 사용, 자원 사용 등)
    # 만약 행동이 종료될 경우 True, 종료되지 않을 경우 False를 반환한다. (카드의 속성에 따라 다르게 처리)
    def action(self, card_number: str) -> bool:
        done = True
        not_done = False
        if card_number == "EARN_001":
            self._resource.set("food", self._resource.get("food") + 1)
            return done
        return not_done

    def harvest(self):
        pass

    def create_farm(self, position: int) -> bool:
        farm = Field(filed_type=FieldType.FARM, position=position, is_in={})
        self._fields.append(farm)
        return True

    def change_field_is_in(self, position: List[int], resource: str, count: int) -> bool:
        field = list(filter(lambda x: x.position == position, self._fields))[-1]
        if field.get("field_type") == FieldType.FARM:
            if resource != "vegetable" and resource != "grain":
                raise Exception("씨 뿌리기는 밭에만 가능합니다.")

            if resource == "grain":
                field.get("is_in").set("grain", count)

            elif resource == "vegetable":
                field.get("is_in").set("vegetable", count)
            return True

        # elif field.get("field_type") == FieldType.CAGE:
