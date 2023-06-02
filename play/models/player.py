from typing import List

from core.models import Base
from play.models.card import Card
from play.models.field import Field, FieldType
from play.models.resource import Resource

FIELD_SCORE_BOARD = {
    'farm': {
        0: -1,
        1: -1,
        2: 1,
        3: 2,
        4: 3,
        5: 4,
    },
    'cage': {
        0: -1,
        1: 1,
        2: 2,
        3: 3,
        4: 4,
        5: 4,
    },
}
class Player(Base):
    _name: str
    _resource: Resource
    _card: List[Card]
    _effects: List[None]
    _fields: List[Field]
    _roomtype: str

    def __init__(
            self,
            name: str = "",
            resource: dict = None,
            fields: List[dict] = None,
    ):
        self._name = name
        self._resource = Resource.from_dict(**resource) if resource else Resource()
        self._fields = [Field.from_dict(**field) for field in fields] if fields else Field.initialize()

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

    def create_farm(self, position: List[int]) -> bool:
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

    def calculate_card_score(self) -> int:
        score = 0
        for card in self._card:
            score += card.score
        return score
    
    def calculate_field_score(self) -> int:
        score = 0
        farm = 0
        cage = 0
        
        for field in self._fields:
            if field.field_type == FieldType.ROOM:
                if self._roomtype == "clay":
                    score += 1
                elif self._roomtype == "stone":
                    score += 2
            elif field.field_type == FieldType.EMPTY:
                if "cowshed" not in field.is_in:
                    score -= 1
            elif field.field_type == FieldType.CAGE:
                if "cowshed" in field.is_in:
                    score += 1
                    cage += 1
            elif field.field_type == FieldType.FARM:
                    farm += 1        
                    
        keys = FIELD_SCORE_BOARD.keys()
        for key in keys:
            score += FIELD_SCORE_BOARD[key][min(self.get(key), 5)]
            
        return score

    def calculate_score(self) -> int:
            card_score = self.calculate_card_score()
            field_score = self.calculate_field_score()
            resource_score = self._resource.calculate_score()

            total_score = card_score + field_score + resource_score
            return total_score