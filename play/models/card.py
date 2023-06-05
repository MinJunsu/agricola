from core.models import Base
from play.models.round_card import RoundCard


class Card(Base):
    _card_number: str
    _name: str
    _score: int
    _is_used: bool

    def __init__(
            self,
            card_number: str,
            name: str,
            score: int,
            is_use: bool = False
    ):
        self._card_number = card_number
        self._name = name
        self._score = score
        self._is_use = is_use

    # 플레이어가 들고 있는 카드를 사용함과 동시에 라운드 카드에 특정한 이펙트를 추가해준다.
    def use(self, round_card: RoundCard):
        self._is_use = True
