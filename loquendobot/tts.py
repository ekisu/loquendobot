from gtts import gTTS
from io import BytesIO
from pydub import AudioSegment
from tempfile import NamedTemporaryFile
from .utils import overlay_sound_perfect_loop

LOQUENDO_OVERLAY_PATH = 'loquendo.mp3'

def tts(text: str, lang: str) -> AudioSegment:
    bytes_io = BytesIO()
    tts_object = gTTS(text, lang=lang)
    tts_object.write_to_fp(bytes_io)

    bytes_io.seek(0)
    return AudioSegment.from_file(bytes_io)

def loquendo_tts(text: str, lang: str) -> AudioSegment:
    overlaid_audio = AudioSegment.from_file(LOQUENDO_OVERLAY_PATH)
    return overlay_sound_perfect_loop(tts(text, lang), overlaid_audio)
