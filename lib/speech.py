import os
import speech_recognition as sr
from .utils.audio_converter import oga2wav


def voice_recognition(voice) -> str:
    wav_audio_path = oga2wav(voice)
    r = sr.Recognizer()
    with sr.AudioFile(str(wav_audio_path)) as source:
        audio = r.record(source)

    os.remove(voice)
    os.remove(wav_audio_path)

    try:
        return r.recognize_google(audio, language="ru-RU", show_all=True)["alternative"][0]["transcript"]
    except sr.UnknownValueError:
        return "Speech Recognition could not understand audio"
    except sr.RequestError as e:
        return "Something went wrong, please try again"
