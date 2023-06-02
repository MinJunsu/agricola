from channels.generic.websocket import AsyncJsonWebsocketConsumer

from core.redis import connection
from play.models.game import Game


class GameConsumer(AsyncJsonWebsocketConsumer):
    id: int
    group_name: str

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.redis = connection()
        game = Game.initialize(["1", "2", "3", "4"])
        self.redis.set("game_3", str(game.to_dict()))

    async def connect(self):
        self.id = self.scope['url_route']['kwargs']['pk']
        self.group_name = f"game_{self.id}"

        await self.channel_layer.group_add(
            self.group_name,
            self.channel_name
        )

        data = self.redis.get(f"game_{self.id}")

        await self.accept()

        await self.send_json(eval(data))

    async def disconnect(self, code):
        await self.channel_layer.group_discard(
            self.group_name,
            self.channel_name
        )

    # {
    #     "type": "action",
    #     "player": 0,
    #     "number": "EARN_001"
    # }
    async def receive_json(self, content, **kwargs):
        data = self.redis.get(f"game_{self.id}")

        game = Game.from_dict(**eval(data))
        played_data = game.play(content)

        self.redis.set(f"game_{self.id}", str(played_data))

        await self.channel_layer.group_send(
            self.group_name,
            {
                'type': 'game_message',
                'message': {
                    'data': str(played_data)
                }
            }
        )

    async def game_message(self, event):
        await self.send_json(event['message'])
