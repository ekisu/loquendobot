from gtts import gTTS
from pydub import AudioSegment
from tempfile import NamedTemporaryFile
from .utils import overlay_sound_perfect_loop

def tts(text: str, lang: str) -> AudioSegment:
    with NamedTemporaryFile(delete=False) as f:
        tts_object = gTTS(text, lang=lang)
        tts_object.write_to_fp(f)
        
        f.seek(0)
        return AudioSegment.from_file(f)

def loquendo_tts(text: str, lang: str, overlaid_audio_path = "loquendo.mp3") -> AudioSegment:
    overlaid_audio = AudioSegment.from_file(overlaid_audio_path)
    return overlay_sound_perfect_loop(tts(text, lang), overlaid_audio)
