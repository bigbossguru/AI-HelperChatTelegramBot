import openai


def gpt_response(msg: str, length: int = 2048, temperature: float = 0.5) -> str:
    """
    The function which provides connection with GPTChat and send back response

    :param str msg: your question
    :param int length: length of response gptchat, defaults to 2048
    :return str: response from gptchat
    """
    try:
        response = openai.Completion.create(
            model="text-davinci-003",
            prompt=msg,
            temperature=temperature,
            max_tokens=length,
        )

        return response["choices"][0]["text"]
    except Exception as e:
        return str(e)
