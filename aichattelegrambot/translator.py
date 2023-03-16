import aiohttp


async def translate(msg: str, lang: str) -> str:
    """
    The function which provides translate all kinds of languages

    :param str msg: the user text
    :param str lang: the king of lang e.g 'en'
    :return str: translated text
    """
    payload = {
        "q": msg,
        "source": "auto",
        "target": lang,
        "format": "text",
    }
    try:
        async with aiohttp.ClientSession() as session:
            async with session.post("https://libretranslate.de/translate", data=payload) as resp:
                data = await resp.json()
                return data["translatedText"]
    except Exception:
        return "Translator is loaded, please try again"
