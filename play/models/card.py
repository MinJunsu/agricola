from play.models.base import Base


class Card(Base):
    _card_number: str
    _name: str
    _image: str
    _is_use: bool

    def __init__(
            self,
            card_number: str,
            name: str,
            image: str,
            is_use: bool = False
    ):
        self._card_number = card_number
        self._name = name
        self._image = image
        self._is_use = is_use

    # card 데이터베이스로부터 카드 정보를 가져온다.
    @classmethod
    def get_card_by_card_number(cls, card_number: str) -> 'Card':
        return cls()
