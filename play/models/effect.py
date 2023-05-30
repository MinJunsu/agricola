from typing import List

from core.models import Base
from play.models.player import Player


class Effect(Base):
    _commands: List[str]
    _effects: List[str]
    _init_round: int

    def __init__(
        self,
        commands: List[str],
        effects: List[str],
        init_round: int = 0,
    ):
        self._commands = commands
        self._effects = effects
        self._init_round = init_round

    def check_effect(
            self,
            player: Player,
            action: str,
            round: int,
    ) -> None:
        pass

