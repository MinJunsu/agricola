from core.models import Base


class FieldResource(Base):
    _family: int
    _sheep: int
    _boar: int
    _cattle: int
    _grain: int
    _vegetable: int

    def __init__(
            self,
            family: int = 0,
            sheep: int = 0,
            boar: int = 0,
            cattle: int = 0,
            grain: int = 0,
            vegetable: int = 0,
    ):
        self._family = family
        self._sheep = sheep
        self._boar = boar
        self._cattle = cattle
        self._grain = grain
        self._vegetable = vegetable

    @classmethod
    def initialize_player(cls) -> 'FieldResource':
        return cls(family=1)
