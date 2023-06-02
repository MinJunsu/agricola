from typing import List

from core.const import INITIAL_BASE_CARDS
from core.const import INITIAL_ROUND_CARDS
from core.models import Base
import random

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

    # 각 주기에 알맞는 라운드 카드를 넣은 배열을 리턴한다.
    @classmethod
    def initialize_round_cards(cls) -> List['RoundCard']:
        round_cards = []

        # 각 주기에 대해 순서를 셔플한 카드들을 round_cards 리스트에 추가
        for round_number, cards in INITIAL_ROUND_CARDS.items():
            random.shuffle(cards)
            round_cards.extend([cls(**card) for card in cards])

        return round_cards
