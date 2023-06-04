from channels.generic.websocket import AsyncJsonWebsocketConsumer

from core.redis import connection


class BaseLobbyConsumer(AsyncJsonWebsocketConsumer):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.redis = connection()
