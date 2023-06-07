import asyncio
import json
from unittest import TestCase

from core.redis import connection
from play.models.game import Game


class BaseTestCase(TestCase):
    def setUp(self):
        asyncio.run(self.main())
        pass

    async def main(self):
        self.redis = connection()
        with open("./cards.json", "r") as f:
            cards = map(lambda x: x['fields'], json.load(f))
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
