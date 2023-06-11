from functools import reduce
from typing import List

from core.const import FIELD_SCORE_BOARD
from core.models import Base
from play.enum import HouseType
from play.models.card import Card
from play.models.field import Field, FieldType
from play.models.resource import Resource


class Player(Base):
    _name: str
    _resource: Resource
    _cards: List[Card]
    _effects: List[None]
    _fields: List[Field]
    _house_type: HouseType
    _fences: dict | None

    def __init__(
            self,
            name: str = "",
            resource: dict = None,
            fields: List[dict] = None,
            house_type: HouseType = HouseType.WOOD_HOUSE,
            fences: dict = None,
            cards: List[dict] = None,
    ):
        self._name = name
        self._resource = Resource.from_dict(**resource) if resource else Resource.initialize_player_resource()
        self._fields = [Field.from_dict(**field) for field in fields] if fields else Field.initialize()
        self._house_type = HouseType.CLAY_HOUSE
        self._fences = fences if fences else None
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

    # 수확단계 수행
    def harvest(self):
        pass

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

    def calculate_card_score(self) -> dict:
        dictionary = dict()
        for card in self._cards:
            if card.get("score") != 0 and card.get("is_used"):
                dictionary[card.get("card_number")] = card.get("score")
        return dictionary

    def inform_player_field(self) -> dict:
        farm = 0
        cage = 0
        clay_room = 0
        stone_room = 0
        cage_barn = 0
        empty = 0

        for field in self._fields:
            if field.field_type == FieldType.EMPTY:
                if not field.get("is_barn"):
                    empty += 1
            elif field.field_type == FieldType.CAGE:
                cage += 1
                if field.get("is_barn"):
                    cage_barn += 1
            elif field.field_type == FieldType.FARM:
                farm += 1
            elif field.field_type == FieldType.ROOM:
                if self._house_type == HouseType.CLAY_HOUSE:
                    clay_room += 1
                elif self._house_type == HouseType.STONE_HOUSE:
                    stone_room += 1

        dictionary = {'farm': farm, 'cage': cage, 'clay_room': clay_room, 'stone_room': stone_room,
                      'cage_barn': cage_barn, 'empty': empty}
        return dictionary

    def calculate_field_score(self) -> dict:

        dictionary = dict()
        key_dic = self.inform_player_field()
        keys = FIELD_SCORE_BOARD.keys()
        for key in keys:
            dictionary[key] = FIELD_SCORE_BOARD[key][key_dic.get(key)]

        return dictionary

    def calculate_score(self) -> dict:
        card_score = self.calculate_card_score()
        field_score = self.calculate_field_score()
        resource_score = self.get("resource").calculate_score()

        sum_score = dict(**card_score, **field_score, **resource_score)

        # 점수 계산 로직
        score = reduce(lambda acc, x: acc + x[1], sum_score.items(), 0)
        result = {**sum_score, 'sum': score}
        return result

    def to_dict(self) -> dict:
        dictionary = super().to_dict()
        dictionary["house_type"] = self._house_type.value
        return dictionary

    @classmethod
    def from_dict(cls, **kwargs):
        house_type = kwargs.pop("house_type")
        kwargs["house_type"] = HouseType(house_type)
        return super().from_dict(**kwargs)
