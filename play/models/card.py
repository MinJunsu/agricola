from core.models import Base


class Card(Base):
    _card_number: str
    _name: str
    _score: int
    _is_used: bool

    def __init__(
            self,
            card_number: str,
            card_type: str,
            name: str,
            image: str,
            cost: dict,
            score: int,
            condition: str,
            command: str,
            description: str,
            is_use: bool = False
    ):
        self._card_number = card_number
        self._card_type = card_type
        self._name = name
        self._image = image
        self._cost = cost
        self._score = score
        self._condition = condition
        self._command = command
        self._description = description
        self._is_use = is_use

    # card 데이터베이스로부터 카드 정보를 가져온다.
    @classmethod
    def get_card_by_card_number(cls, card_number: str) -> 'Card':
        return cls()
