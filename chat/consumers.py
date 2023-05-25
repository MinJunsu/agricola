import logging

from asgiref.sync import async_to_sync
from channels.generic.websocket import WebsocketConsumer


class ChatConsumer(WebsocketConsumer):
    logger: logging.Logger

    def __init__(self):
        super().__init__()
        self.logger = logging.getLogger(__name__)

    async def connect(self):
        async_to_sync(self.channel_layer.group_add)(

        )
        await self.accept()

    def disconnect(self, close_code):
        pass

    def receive(self, text_data=None, bytes_data=None):
        self.send(text_data=text_data)
