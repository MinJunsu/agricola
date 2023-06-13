from typing import List

from core.const import INITIAL_PRI_CARDS
from core.models import Base


class PrimaryCard(Base):
    _card_number: str
    _owner: int

    def __init__(
            self,
            card_number: str,
            owner: int | None = None,
    ):
        self._card_number = card_number
        self._owner = owner

    @classmethod
    def initialize_primary_cards(cls) -> List['PrimaryCard']:
        return [cls(**card) for card in INITIAL_PRI_CARDS]

    pass
