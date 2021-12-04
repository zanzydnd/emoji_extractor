from tortoise import Tortoise, run_async

from core.config import Config
from models.Comment import Emotion


async def fill():
    config = Config()
    await Tortoise.init(
        db_url=str(config.DATABASE_URL()),
        modules={'models': ['models.Comment']}
    )

    await Emotion.create(name='negative')
    await Emotion.create(name='positive')
    await Emotion.create(name='neutral')


run_async(fill())
