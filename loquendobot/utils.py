from io import BytesIO
from pydub import AudioSegment
import math

def overlay_sound_perfect_loop(base: AudioSegment, overlay: AudioSegment) -> AudioSegment:
    duration_base = len(base)
    duration_overlay = len(overlay)
    times_looped = math.ceil(duration_base / duration_overlay)
    silence_time_needed = duration_overlay * times_looped - duration_base

    if silence_time_needed > 0:
        base = base.append(
            AudioSegment.silent(duration=max(silence_time_needed, 100)),
            crossfade = 100
        )
    
    return base.overlay(overlay, times = times_looped)

def audio_segment_to_voice(segment: AudioSegment) -> BytesIO:
    b = BytesIO()
    segment.export(b, format = "ogg", codec = "libopus")
    return b
