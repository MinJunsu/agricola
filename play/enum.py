from enum import Enum


class FieldType(Enum):
    ROOM = "room"
    FARM = "farm"
    CAGE = "cage"


class HouseType(Enum):
    WOOD_HOUSE = "wood"
    CLAY_HOUSE = "clay"
    STONE_HOUSE = "stone"


class CommandType(Enum):
    ACTION = 'action'
    ADDITIONAL = 'additional'
    ALWAYS = 'always'
