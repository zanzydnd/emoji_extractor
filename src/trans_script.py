from deep_translator import GoogleTranslator


def translate(text: str) -> str:
    return GoogleTranslator(source='en', target='ru').translate(text)


print(translate("True story!"))
