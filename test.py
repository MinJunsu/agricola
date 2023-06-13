import json
import os

import django

os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'agricola.settings')
os.environ["DJANGO_ALLOW_ASYNC_UNSAFE"] = 'true'
django.setup()


async def main():
    from play.models.game import Game
    from core.redis import connection
    redis = connection()

    with open("./test.json", "r") as f:
        data = json.loads(f.read())
        test = Game.from_dict(**data)
        redis.set("game:999", str(test.to_dict()))


if __name__ == '__main__':
    import asyncio

    asyncio.run(main())
