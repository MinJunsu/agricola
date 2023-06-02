from core.models import Base


class RoundCard(Base):
    _card_number: str
    _is_stacked: bool
    _resource: dict
    _additional_action: dict

    def __init__(
            self,
            card_number: str,
            is_stacked: bool = False,
            resource: dict = None,
            additional_action: dict = None,
    ):
        self._card_number = card_number
        self._is_stacked = is_stacked
        self._resource = resource
        self._additional_action = additional_action
