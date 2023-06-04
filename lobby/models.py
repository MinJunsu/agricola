from typing import List

from core.models import Base
from core.redis import connection


class RoomOption(Base):
    _title: str
    _is_chat: bool
    _mode: str
    _time_limit: int
    _password: str

    def __init__(
            self,
            title: str,
            is_chat: bool,
            mode: str,
            password: str,
            time_limit: int,

    ):
        self._title = title
        self._is_chat = is_chat
        self._mode = mode
        self._time_limit = time_limit
        self._password = password


class Room(Base):
    _room_id: int
    _host: int
    _options: RoomOption
    _participants: List[int]

    def __init__(
            self,
            room_id: int,
            host: int,
            options: dict,
            participants: List[int] = None,
    ):
        self._room_id = room_id
        self._host = host
        self._options = RoomOption.from_dict(**options)
        self._participants = participants or []

    # 기존의 로비 데이터들을 불러와 Room 객체로 변환
    @classmethod
    def create_room(cls, host: int, options: dict) -> 'Room':
        redis = connection()

        # Cache에 저장된 room_number 들을 불러와 중복되지 않은 room_number를 생성
        room_numbers = list(map(int, redis.smembers('rooms:number')))
        room_id = cls.generate_room_number(room_numbers)

        # 생성한 room_number를 Cache에 저장
        redis.sadd('rooms:number', room_id)

        # 새로운 방 생성 후, 유저 추가
        room = cls(
            room_id=room_id,
            host=host,
            options=options,
        )
        room.enter(host)

        redis.hset("rooms:participants", host, room_id)
        redis.hset("lobby:watch:participants", host, room_id)
        redis.hset("rooms", room_id, str(room.to_dict()))

        return room

    @staticmethod
    def generate_room_number(numbers: List[int]) -> int:
        return 1 if len(numbers) == 0 else max(numbers) + 1

    def to_lobby_dict(self) -> dict:
        return {
            'room_id': self._room_id,
            'host': self._host,
            'options': {
                'title': self._options.get('title'),
                'mode': self._options.get('mode'),
                'password': self._options.get('password'),
            },
        }

    def enter(self, user_id: int) -> None:
        self._participants.append(user_id)

    def exit(self, user_id: int) -> None:
        self._participants.remove(user_id)
