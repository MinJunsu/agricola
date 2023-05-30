from play.models.base import Base
from play.models.card import Card


class Action(Base):
    _card: Card
    _player: str
    _is_kid: bool

    def __init__(
            self,
            card_number: str,
            player: str,
            is_kid: bool = False
    ):
        self._card = card_number
        self._player = player
        self._is_kid = is_kid

