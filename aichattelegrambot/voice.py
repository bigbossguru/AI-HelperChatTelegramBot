import os
import pathlib
import openai

from .utils.audio_converter import oga2format


def voice_recognition(audio: pathlib.Path) -> str:
    """
    The function which provides speech recognition for all languages

    :param str audio: absolute path where store audio file
    :return str: return transcript text
    """

    mp3_audio_path = oga2format(audio)
    with open(mp3_audio_path, "rb") as mp3_audio:
        transcript = openai.Audio.transcribe("whisper-1", mp3_audio)

    # After reading remove all audio files
    os.remove(audio)
    os.remove(mp3_audio_path)
    return transcript.text
