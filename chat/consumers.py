import logging
from datetime import datetime

from channels.generic.websocket import AsyncJsonWebsocketConsumer
from redis.client import Redis

from chat.models import ChatMessage
from core.redis import connection


class ChatConsumer(AsyncJsonWebsocketConsumer):
    redis: Redis
    logger: logging.Logger
    pk: int
    # user를 사용한 코드 인증 방식으로 구현
    group_name: str

    def __init__(self):
        super().__init__()
        self.logger = logging.getLogger(__name__)
        self.redis = connection()

    @property
    def logger_basic_format(self):
        return f"[socket: CHAT] CHAT: {self.pk} | "

    async def connect(self):
        self.pk = self.scope['url_route']['kwargs']['pk']
        self.group_name = f"chat_{self.pk}"

        self.logger.info(self.logger_basic_format + "new connecting to chat")

        await self.channel_layer.group_add(
            self.group_name,
            self.channel_name
        )

        await self.accept()

    async def disconnect(self, code):
        self.logger.info(self.logger_basic_format + "disconnect from chat")
        # TODO: 모두 채팅방에서 나갈 경우 채팅방 기록 및 redis 에서 해당 채팅방 삭제
        # self.redis.delete(self.group_name)
        await self.channel_layer.group_discard(
            self.group_name,
            self.channel_name
        )

    async def receive_json(self, content, **kwargs):
        # message 파싱 작업
        command, user_id, receive_message = await self.parse_command(content)
        self.logger.info(
            self.logger_basic_format +
            f"receive from message user_id={user_id} command={command}, message={receive_message}"
        )

        if command == "message":
            index = self.redis.scard(self.group_name)
            # 형식에 맞추어 메시지 생성
            message = ChatMessage(
                index=index + 1,
                message=receive_message,
                user_id=user_id,
                timestamp=datetime.now().strftime("%Y-%m-%d %H:%M:%S")
            )

            # redis 에 새롭게 생성한 메시지 저장
            self.redis.sadd(self.group_name, str(message.to_dict()))

            return await self.channel_layer.group_send(
                self.group_name,
                {
                    "type": "message",
                    "message": message.to_dict()
                }
            )

        elif command == "sync":
            # redis 로부터 전체 채팅방 메시지 불러오기
            messages = str([eval(message) for message in self.redis.smembers(self.group_name)])

            return await self.send(messages)

        return await self.send("invalid command")

    @staticmethod
    async def parse_command(commands: dict) -> tuple[str, int, str]:
        command: str = commands.get('command', 'sync')
        user_id: int = commands.get('user_id', -1)
        message: str = commands.get('message', None)
        return command, user_id, message

    async def message(self, event):
        await self.send_json(event['message'])
