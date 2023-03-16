import pathlib
from pydub import AudioSegment  # type: ignore


def oga2format(audio: pathlib.Path, audio_format="mp3") -> pathlib.Path:
    audio_path = audio.with_suffix(f".{audio_format}")
    oga_audio = AudioSegment.from_file(audio)
    oga_audio.export(audio_path, format=audio_format)
    return audio_path
