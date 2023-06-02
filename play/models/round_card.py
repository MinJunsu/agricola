from typing import List

from core.const import INITIAL_BASE_CARDS
from core.models import Base


class RoundCard(Base):
    _card_number: str
    _is_stacked: bool
    _count: int
    _resource: dict
    _additional_action: dict

    def __init__(
            self,
            card_number: str,
            is_stacked: bool = False,
            count: int = 0,
            resource: dict = None,
            additional_action: dict = None,
    ):
        self._card_number = card_number
        self._is_stacked = is_stacked
        self._count = count
        self._resource = resource
        self._additional_action = additional_action

    @classmethod
    def initialize_base_cards(cls) -> List['RoundCard']:
        return [cls(**card) for card in INITIAL_BASE_CARDS]
