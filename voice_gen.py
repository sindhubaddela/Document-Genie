# voice_gen.py

from gtts import gTTS
import io
import re

def synthesize_dual_voice(script, progress_callback=None):
    """
    Converts a podcast script with markdown and varied speaker formats into alternating voice audio.
    """
    cleaned = re.sub(r'[*_]{1,2}(\s*\w+\s*):[*_]{1,2}', r'\1:', script)
    cleaned = re.sub(r'\b(Alex|Ben)\s*:\s*', r'\1:', cleaned)
    pattern = r'^(Alex|Ben):(.*)$'
    dialogue_lines = re.findall(pattern, cleaned, flags=re.MULTILINE)

    if not dialogue_lines:
        raise ValueError("No valid dialogue lines found. Format as 'Alex: your line'.")

    final_audio = bytearray()
    total = len(dialogue_lines)

    for idx, (speaker, text) in enumerate(dialogue_lines):
        tld = 'co.uk' if speaker == "Alex" else 'com'
        line = text.strip().replace('\n', ' ')
        if not line:
            continue

        if speaker == "Alex":
            line = f"{line}"
        else:
            if line and line[0].islower():
                line = f"Well, {line}"

        tts = gTTS(text=line, lang='en', tld=tld)
        mp3_buf = io.BytesIO()
        tts.write_to_fp(mp3_buf)
        mp3_buf.seek(0)
        final_audio += mp3_buf.read()

        if progress_callback:
            progress_callback((idx + 1) / total)

    return io.BytesIO(final_audio)