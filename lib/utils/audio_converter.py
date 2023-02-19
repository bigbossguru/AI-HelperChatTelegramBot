import pathlib
from pydub import AudioSegment


def oga2wav(audio) -> str:
    wav_audio_path = pathlib.Path(str(audio).replace(".oga", ".wav"))
    oga_audio = AudioSegment.from_file(audio)
    oga_audio.export(wav_audio_path, format="wav")
    return wav_audio_path
