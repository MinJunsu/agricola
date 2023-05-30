from enum import Enum
from typing import List

from core.models import Base


class FieldType(Enum):
    ROOM = "room"
    FARM = "farm"
    CAGE = "cage"
    EMPTY = "empty"


class Field(Base):
    filed_type: FieldType
    position: List[int]
    is_in: dict

    def __init__(
            self,
            filed_type: FieldType,
            position: List[int],
            is_in: dict,
    ):
        self.filed_type = filed_type
        self.position = position
        self.is_in = is_in

    @classmethod
    def initialize(cls) -> 'List[Field]':
        room1 = cls(
            filed_type=FieldType.ROOM,
            position=[0, 1],
            is_in={
                "familly": 1,
            }
        )
        room2 = cls(
            filed_type=FieldType.ROOM,
            position=[0, 2],
            is_in={
                "familly": 1,
            }
        )
        return [room1, room2]

