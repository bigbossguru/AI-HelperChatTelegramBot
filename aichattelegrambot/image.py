import typing
import openai
import aiohttp

from .chat import gpt_response
from .utils.text_formatting import text_reduce


async def image_generator(msg: typing.Optional[str] = None) -> typing.Tuple[bytes, str]:
    """
    The function which provides connection with DALL-E model for generating image.
    There're two way how to use this function like first random if msg is None or
    if you send msg to generate by your description

    :param typing.Optional[str] msg: the user text, defaults to None
    :return typing.Tuple[bytes, str]: image and message
    """
    msg = msg or gpt_response("describe a random picture", 500)
    msg += " realistic, 4k, high detail, high quilty"
    response = openai.Image.create(prompt=msg, n=1, size="512x512")
    image_url = response["data"][0]["url"]
    async with aiohttp.ClientSession() as session:
        async with session.get(image_url) as resp:
            data = await resp.content.read()
            return data, text_reduce(msg)
