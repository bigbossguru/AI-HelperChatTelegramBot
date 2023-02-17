import os
import openai
import requests

from dotenv import load_dotenv

load_dotenv()

openai.organization = os.environ.get("OPENAI_ORG")
openai.api_key = os.environ.get("OPENAI_TOKEN")


def answer(msg: str):
    response = openai.Completion.create(
        model="text-davinci-003",
        prompt=msg,
        temperature=0.9,
        max_tokens=150,
        top_p=1,
        frequency_penalty=0.0,
        presence_penalty=0.6,
        stop=[" Human:", " AI:"],
    )

    return response["choices"][0]["text"]


def genrandimage(msg: str = None):
    msg = msg or answer("describe a random image")
    response = openai.Image.create(prompt=msg, n=1, size="512x512")
    image_url = response["data"][0]["url"]
    return requests.get(image_url).content, msg
