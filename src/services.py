import operator
from typing import Tuple
from collections import defaultdict
import emoji
from profanity_filter import ProfanityFilter
from textblob import TextBlob
from dostoevsky.tokenization import RegexTokenizer
from dostoevsky.models import FastTextSocialNetworkModel
from nltk.sentiment import SentimentIntensityAnalyzer

from profanity_helper import PymorphyProc


async def get_language(text: str) -> str:
    b = TextBlob(text)
    return b.detect_language()


async def rm_all_emojis_and_get_their_nums(text) -> Tuple[str, dict]:
    return_text = ''
    emojies = defaultdict(int)
    for symb in text:
        if symb in emoji.UNICODE_EMOJI['en']:
            emojies[symb] += 1
        else:
            return_text += symb

    return return_text, dict(emojies)


async def does_contain_profanity(text) -> bool:
    b = TextBlob(text)
    lang = b.detect_language()
    pf = ProfanityFilter(languages=['en', 'ru'])
    if lang == 'en':
        return pf.is_profane(text)
    elif lang == 'rus':
        return True if PymorphyProc.test(text) == 1 else False


async def get_tone_of_rus_text(text) -> str:
    tokenizer = RegexTokenizer()
    model = FastTextSocialNetworkModel(tokenizer=tokenizer)
    result = model.predict(text, k=1)[0]
    return max(result.items(), key=operator.itemgetter(1))[0]


async def get_tone_of_en_text(text) -> str:
    sia = SentimentIntensityAnalyzer()
    result = sia.polarity_scores(text)
    result.pop('compound')
    return max(result.items(), key=operator.itemgetter(1))[0]


FUNC_DICT = {'en': get_tone_of_en_text, 'ru': get_tone_of_rus_text}
TONE_DICT = {'negative': 'negative', 'neg': 'negative', 'positive': 'positive', 'pos': 'positive', 'neu': 'neutral',
             'skip': 'neutral', 'neutral': 'neutral'}


async def get_tone_of_text(text: str) -> str:
    return TONE_DICT.get(await FUNC_DICT[await get_language(text)](text))
