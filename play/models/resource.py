from core.const import RESOURCE_SCORE_BOARD, INITIAL_COMMON_RESOURCE, \
    INITIAL_PLAYER_RESOURCE
from core.models import Base


class Resource(Base):
    _wood: int
    _clay: int
    _reed: int
    _stone: int
    _grain: int
    _vegetable: int
    _sheep: int
    _boar: int
    _cattle: int
    _food: int
    _family: int
    _room: int
    _fence: int
    _barn: int
    _begging: int

    """
    자원 초기화 함수: 자원의 초기 값을 설정 한다.
    """

    def __init__(
            self,
            wood: int = 0,
            clay: int = 0,
            reed: int = 0,
            stone: int = 0,
            grain: int = 0,
            vegetable: int = 0,
            sheep: int = 0,
            boar: int = 0,
            cattle: int = 0,
            food: int = 0,
            family: int = 0,
            room: int = 0,
            fence: int = 0,
            barn: int = 0,
            begging: int = 0,
    ):
        self._wood = wood
        self._clay = clay
        self._reed = reed
        self._stone = stone
        self._grain = grain
        self._vegetable = vegetable
        self._sheep = sheep
        self._boar = boar
        self._cattle = cattle
        self._food = food
        self._family = family
        self._room = room
        self._fence = fence
        self._barn = barn
        self._begging = begging

    @classmethod
    def initialize_common_resource(cls):
        common_resource = cls(**INITIAL_COMMON_RESOURCE)
        return common_resource

    @classmethod
    def initialize_player_resource(cls):
        return cls(**INITIAL_PLAYER_RESOURCE)

    def calculate_score(self) -> dict:
        keys = RESOURCE_SCORE_BOARD.keys()
        dictionary = dict()
        for key in keys:
            dictionary[key] = RESOURCE_SCORE_BOARD[key][min(self.get(key), 8)]
        return dictionary
