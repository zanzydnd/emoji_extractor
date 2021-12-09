from tortoise import Tortoise, run_async

from core.config import Config
from models.Comment import Comment, Emotion
from services import rm_all_emojis_and_get_their_nums, get_tone_of_text, does_contain_profanity


async def start():
    config = Config()
    await Tortoise.init(
        db_url=str(config.DATABASE_URL()),
        modules={'models': ['models.Comment', 'models.slang']}
    )

    comments = await Comment.filter(is_done=False).limit(1000)

    for comment in comments:
        proceed_text, emojies = await rm_all_emojis_and_get_their_nums(comment.text)

        tone = await Emotion.filter(name=await get_tone_of_text(proceed_text)).first()

        comment.emoji = emojies
        comment.emotion_text_type_id = tone.id
        comment.is_done = True
        comment.is_contain_profanity = await does_contain_profanity(proceed_text)

        await comment.save()


run_async(start())
