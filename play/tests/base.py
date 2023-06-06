import asyncio
import json
import os

from asgiref.sync import sync_to_async
from django.test import LiveServerTestCase

from cards.models import Card
from core.redis import connection
from play.models.game import Game


class BaseTestCase(LiveServerTestCase):
    def setUp(self):
        asyncio.run(self.main())
        pass

    async def main(self):
        os.environ["DJANGO_ALLOW_ASYNC_UNSAFE"] = 'true'
        self.redis = connection()
        cards = map(lambda x: x['fields'], json.load(open("./cards.json", "r")))
        # redis DB 전체 초기화
        self.redis.flushdb()

        for card in cards:
            self.redis.hset('commands', card['card_number'], card['command'])
            self.redis.hset('cards', card['card_number'], str({
                'card_number': card['card_number'],
                'name': card['name'],
                'score': card['score']
            }))
        # ! 임시 코드 작성 끝

        self.game = await Game.initialize(["1", "2", "3", "4"])
        self.redis.set("game_3", str(self.game.to_dict()))

    @sync_to_async
    def get_cards(self, option):
        return Card.objects.all().values(*option)
