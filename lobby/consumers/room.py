# from core.redis import connection
# from lobby.consumers.base import BaseLobbyConsumer
# from lobby.models import Room
#
#
# class RoomConsumer(BaseLobbyConsumer):
#     room_id: int
#     room: str
#
#     def __init__(self):
#         super().__init__()
#         self.redis = connection()
#
#     async def connect(self):
#         self.room_id = self.scope['url_route']['kwargs']['pk']
#         self.room = f"room_{self.room_id}"
#
#         self.channel_layer.group_add(
#             self.room,
#             self.channel_name
#         )
#
#         await self.accept()
#
#         if str(self.room_id) not in self.redis.hkeys("rooms"):
#             await self.send("INVALID ROOM ID")
#             return await self.close()
#
#         room: Room = Room.from_dict(**eval(self.redis.hget("rooms", self.room_id)))
#         return await self.send_json(room.to_dict())
#
#     async def disconnect(self, code):
#         return await self.channel_layer.group_discard(
#             self.room,
#             self.channel_name
#         )
#
#     async def receive_json(self, content, **kwargs):
#         command, user_id = await self.parse_command(content)
#
#         # 사용자가 방에 입장한 경우
#         if command == RoomCommand.ENTER:
#             if str(user_id) in self.redis.hkeys(f"rooms:participants"):
#                 await self.send("ALREADY ENTERED")
#                 return await self.close()
#
#             room: Room = Room.from_dict(**eval(self.redis.hget("rooms", self.room_id)))
#             room.enter(user_id)
#
#             self.redis.hset(f"rooms:participants", user_id, self.room_id)
#             self.redis.hset("rooms", self.room_id, str(room.to_dict()))
#
#         elif command == RoomCommand.EXIT:
#             if str(user_id) not in self.redis.hkeys(f"rooms:participants"):
#                 await self.send("NOT ENTERED")
#                 return await self.close()
#
#             room: Room = Room.from_dict(**eval(self.redis.hget("rooms", self.room_id)))
#             room.exit(user_id)
#
#             self.redis.hdel(f"rooms:participants", user_id)
#             self.redis.hset("rooms", self.room_id, str(room.to_dict()))
#
#             if len(room.get('participants')) == 0:
#                 self.redis.hdel("rooms", self.room_id)
#
#         else:
#             await self.send("UNDEFINED COMMAND")
#             return await self.close()
#
#         await self.send_message_to_lobby()
#
#         if self.redis.hget("rooms", self.room_id) is None:
#             await self.send("ROOM DELETED")
#             return await self.close()
#
#         return await self.channel_layer.group_send(
#             self.room,
#             {
#                 'type': 'message',
#                 'message': room.to_dict()
#             }
#         )
#
#     async def message(self, event) -> None:
#         return await self.send_json(event['message'])
#
#     @staticmethod
#     async def parse_command(content: dict) -> tuple[RoomCommand, int]:
#         command_str: str = content.get("command", None)
#         command: RoomCommand = RoomCommand(command_str) if command_str else RoomCommand.ENTER
#         user_id: int = content.get("user_id", None)
#         return command, user_id
