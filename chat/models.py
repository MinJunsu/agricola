from core.models import Base


class ChatMessage(Base):
    _index: int
    _message: str
    _user_id: int
    _timestamp: str

    def __init__(
            self,
            index: int,
            message: str,
            user_id: int,
            timestamp: str
    ):
        self._index = index
        self._message = message
        self._user_id = user_id
        self._timestamp = timestamp
