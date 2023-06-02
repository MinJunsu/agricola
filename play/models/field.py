from enum import Enum
from typing import List

from core.models import Base


class FieldType(Enum):
    ROOM = "room"
    FARM = "farm"
    CAGE = "cage"


# position 의 경우 1 ~ 15 까지의 숫자로 이루어진 좌표의 index 값을 사용한다.
# Position index 값 배치도
# 1 2 3 4 5
# 6 7 8 9 10
# 11 12 13 14 15
class Field(Base):
    _field_type: FieldType
    _position: int
    _is_in: dict

    def __init__(
            self,
            field_type: FieldType,
            position: int,
            is_in: dict,
    ):
        self._field_type = field_type
        self._position = position
        self._is_in = is_in

    @classmethod
    def initialize(cls) -> 'List[Field]':
        room1 = cls(
            field_type=FieldType.ROOM,
            position=6,
            is_in={
                "familly": 1,
            }
        )
        room2 = cls(
            field_type=FieldType.ROOM,
            position=11,
            is_in={
                "familly": 1,
            }
        )
        return [room1, room2]

    def to_dict(self) -> dict:
        return {
            "field_type": self._field_type.value,
            "position": self._position,
            "is_in": self._is_in,
        }

    @classmethod
    def from_dict(cls, **kwargs):
        field_type = kwargs.pop("field_type")
        kwargs["field_type"] = FieldType(field_type)
        return super().from_dict(**kwargs)
