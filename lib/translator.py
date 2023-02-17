import requests


def translate(msg, lang):
    payload = {
        "q": msg,
        "source": "auto",
        "target": lang,
        "format": "text",
    }
    try:
        r = requests.post("https://libretranslate.de/translate", data=payload)
        return r.json()["translatedText"]
    except:
        return "Translator loaded, please try again."
