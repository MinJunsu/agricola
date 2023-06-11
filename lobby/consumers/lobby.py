from enum import Enum
from typing import List

from core.redis import connection
from core.response import socket_response
from lobby.consumers.base import BaseLobbyConsumer
from lobby.models import Room
from play.models.game import Game

LOBBY = "lobby"

DEFAULT_ROOM_OPTIONS = {
    "title": "Untitled",
    "is_chat": False,
    "mode": "public",
    "password": "",
    "time_limit": 30,
}


class RoomCommand(Enum):
    CREATE = "create"
    WATCH = "watch"
    ENTER = "enter"
    EXIT = "exit"


class LobbyConsumer(BaseLobbyConsumer):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.redis = connection()

    async def connect(self):
        await self.channel_layer.group_add(
            LOBBY,
            self.channel_name
        )

        await self.accept()
        await self.send_json(socket_response(
            is_success=True,
            data={
                "type": "lobby",
                "result": self.rooms_with_participant,
            }
        ))

    async def disconnect(self, code):
        await self.channel_layer.group_discard(
            LOBBY,
            self.channel_name
        )

    async def receive_json(self, content, **kwargs):
        command, user_id, room_id, options = await self.parse_command(content)
        user: str = str(user_id)
        room: Room | None = None
        is_start: bool = False

        # 유저 정보가 잘못 될 경우 처리
        if user == "-1":
            return await self.send_json(socket_response(
                is_success=False,
                error="INVALID USER ID"
            ))

        # 방 정보가 잘못될 경우 처리
        if command != RoomCommand.CREATE and room_id == "-1":
            return await self.send_json(socket_response(
                is_success=False,
                error="INVALID ROOM ID"
            ))

        if command == RoomCommand.ENTER and str(room_id) in self.redis.hkeys("rooms") is None:
            return await self.send_json(socket_response(
                is_success=False,
                error="INVALID ROOM ID"
            ))

        # 방 생성 정보가 잘못될 경우
        if command == RoomCommand.CREATE:
            if user in self.redis.hkeys("rooms:participants"):
                return await self.send_json(socket_response(
                    is_success=False,
                    error="ALREADY CREATED"
                ))

            new_room = Room.create_room(
                host=user_id,
                options=options,
            )

            await self.channel_layer.group_add(
                f"room_{new_room.get('room_id')}",
                self.channel_name,
            )

        elif command == RoomCommand.WATCH:
            # 만약 이미 시청중인 방이 있다면, 해당 방에서 나가고 새로운 방으로 이동
            if str(user_id) in self.redis.hkeys("lobby:watch:participants"):
                already_watching_room_id = self.redis.hget("lobby:watch:participants", user_id)
                self.redis.hdel("lobby:watch:participants", user_id)
                self.redis.hset("lobby:watch:participants", user_id, room_id)
                await self.channel_layer.group_discard(
                    f"room_{already_watching_room_id}",
                    self.channel_name,
                )

            room: Room = Room.from_dict(**eval(self.redis.hget("rooms", str(room_id))))
            await self.send_json(socket_response(
                is_success=True,
                data={
                    "type": "room",
                    "result": room.to_dict(),
                },
            ))

            return await self.channel_layer.group_add(
                f"room_{room_id}",
                self.channel_name,
            )

        elif command == RoomCommand.ENTER:
            if str(user_id) in self.redis.hkeys("rooms:participants"):
                return await self.send_json(socket_response(
                    is_success=False,
                    error="ALREADY ENTERED"
                ))

            await self.channel_layer.group_add(
                f"room_{room_id}",
                self.channel_name,
            )

            room: Room = Room.from_dict(**eval(self.redis.hget("rooms", room_id)))
            room.enter(user_id)

            self.redis.hset("rooms:participants", user_id, room_id)
            self.redis.hset("rooms", room_id, str(room.to_dict()))

            if len(room.get('participants')) == 4:
                new_game = await Game.initialize(room.get('participants'))
                self.redis.set(f"game:{room.get('room_id')}", str(new_game.to_dict()))
                is_start = True

        elif command == RoomCommand.EXIT:
            if str(user_id) not in self.redis.hkeys(f"rooms:participants"):
                return await self.send_json(socket_response(
                    is_success=False,
                    error="NOT ENTERED"
                ))

            room: Room = Room.from_dict(**eval(self.redis.hget("rooms", room_id)))
            room.exit(user_id)

            self.redis.hdel(f"rooms:participants", user_id)
            self.redis.hset("rooms", room_id, str(room.to_dict()))

            if len(room.get('participants')) == 0:
                self.redis.hdel("rooms", room_id)

            if self.redis.hget("rooms", room_id) is None:
                await self.channel_layer.group_discard(
                    f"room_{room_id}",
                    self.channel_name,
                )

        else:
            return await self.send_json(socket_response(
                is_success=False,
                error="INVALID COMMAND"
            ))

        if command == RoomCommand.CREATE or command == RoomCommand.ENTER or command == RoomCommand.EXIT:
            await self.send_message_to_lobby()

        if command == RoomCommand.ENTER or command == RoomCommand.EXIT:
            await self.send_message_to_room(room_id)

        if is_start:
            await self.send_message_to_gamestart(room)

            # 게임과 관련된 모든 정보 삭제
            self.redis.hdel("rooms", room_id)
            [self.redis.hdel("rooms:participants", particitant) for particitant in room.get('participants')]
            [self.redis.hdel("lobby:watch:participants", particitant) for particitant in room.get('participants')]

    @staticmethod
    async def parse_command(content: dict) -> tuple[RoomCommand, int, int, dict]:
        command_str: str = content.get("command", "enter")
        command: RoomCommand = RoomCommand(command_str)
        user_id: int = content.get("user_id", -1)
        room_id: int = content.get("room_id", -1)
        create_options: dict = content.get("options", {})
        for key, value in DEFAULT_ROOM_OPTIONS.items():
            if key not in create_options:
                create_options[key] = value
        return command, user_id, room_id, create_options

    @property
    def rooms_with_participant(self) -> List[dict]:
        return list(map(self.room_in_participant, self.redis.hvals("rooms")))

    @staticmethod
    def room_in_participant(room_data: str) -> dict:
        room: Room = Room.from_dict(**eval(room_data))
        return {
            **room.to_lobby_dict(),
            "participant": len(room.get("participants"))
        }

    async def send_message_to_lobby(self):
        return await self.channel_layer.group_send(
            "lobby",
            {
                "type": "message",
                "message": socket_response(
                    is_success=True,
                    data={
                        "type": "lobby",
                        "result": self.rooms_with_participant,
                    },
                )
            }
        )

    async def send_message_to_gamestart(self, room: Room):
        return await self.channel_layer.group_send(
            f"room_{room.get('room_id')}",
            {
                "type": "message",
                "message": socket_response(
                    is_success=True,
                    data={
                        "type": "start",
                        "result": {
                            "participants": room.get('participants'),
                        }
                    }
                ),
            }
        )

    async def send_message_to_room(self, room_id: int):
        room: Room = Room.from_dict(**eval(self.redis.hget("rooms", room_id)))
        return await self.channel_layer.group_send(
            f"room_{room_id}",
            {
                "type": "message",
                "message": socket_response(
                    is_success=True,
                    data={
                        "type": "room",
                        "result": room.to_dict(),
                    },
                )
            }
        )

    async def message(self, event):
        await self.send_json(event['message'])
