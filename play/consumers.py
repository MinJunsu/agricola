from channels.generic.websocket import AsyncJsonWebsocketConsumer
from deepdiff import DeepDiff

from core.redis import connection
from core.response import socket_response
from play.exception import IsNotPlayerTurnException, CantUseCardException
from play.models.game import Game


class GameConsumer(AsyncJsonWebsocketConsumer):
    id: int
    group_name: str

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.redis = connection()

    async def connect(self):
        self.id = self.scope['url_route']['kwargs']['pk']
        self.group_name = f"game_{self.id}"

        await self.channel_layer.group_add(
            self.group_name,
            self.channel_name
        )

        data = self.redis.get(f"game_{self.id}")

        await self.accept()

        await self.send_json(socket_response(
            is_success=True,
            data={
                "type": "sync",
                "result": eval(data)
            }
        ))

    async def disconnect(self, code):
        await self.channel_layer.group_discard(
            self.group_name,
            self.channel_name
        )

    async def receive_json(self, content, **kwargs):
        data = self.redis.get(f"game_{self.id}")

        game = Game.from_dict(**eval(data))
        try:
            played_data = game.play(content)

        except IsNotPlayerTurnException as e:
            return await self.send_json(socket_response(
                is_success=False,
                error=str(e)
            ))

        except CantUseCardException as e:
            return await self.send_json(socket_response(
                is_success=False,
                error=str(e)
            ))
        except Exception as e:
            return await self.send_json(socket_response(
                is_success=False,
                error=str(e)
            ))

        change = []

        # 이전 데이터와 달라진 데이터를 조회하기 위한 처리 (DeepDiff)
        deep_diff = DeepDiff(eval(data), played_data)
        values = deep_diff.get("values_changed", {})
        types = deep_diff.get("type_changes", {})

        # 이전 데이터와 변화된 데이터가 있다면 change에 추가
        if values or types:
            for key, value in [*values.items(), *types.items()]:
                key = key.replace("root", "")
                change.append({
                    "key": key,
                    "value": value['new_value'],
                    "prev": value['old_value']
                })

        self.redis.set(f"game_{self.id}", str(played_data))

        return await self.channel_layer.group_send(
            self.group_name,
            {
                'type': 'game_message',
                'message': socket_response(
                    is_success=True,
                    data={
                        "type": "change",
                        "result": change
                    }
                )
            }
        )

    async def game_message(self, event):
        await self.send_json(event['message'])
