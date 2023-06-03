import os

import django

os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'agricola.settings')
os.environ["DJANGO_ALLOW_ASYNC_UNSAFE"] = 'true'
django.setup()


async def main():
    from core.redis import connection
    from play.models.game import Game

    redis = connection()
    game = await Game.initialize(["1", "2", "3", "4"])
    redis.set("game_3", str(game.to_dict()))


if __name__ == '__main__':
    import asyncio

    asyncio.run(main())
