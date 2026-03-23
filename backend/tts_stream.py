# Handles Azure TTS audio generation and viseme extraction

import azure.cognitiveservices.speech as speechsdk
import os
from dotenv import load_dotenv
import base64

load_dotenv()

AZURE_KEY = os.getenv("AZURE_SPEECH_KEY")
AZURE_REGION = os.getenv("AZURE_SPEECH_REGION")

def create_speech_config():
    """
    Creates and returns Azure speech config
    """
    speech_config = speechsdk.SpeechConfig(
        subscription=AZURE_KEY,
        region=AZURE_REGION
    )

    # Voice selection
    speech_config.speech_synthesis_voice_name = "en-US-JennyNeural"

    # Output as MP3 for browser playback
    speech_config.set_speech_synthesis_output_format(
        speechsdk.SpeechSynthesisOutputFormat.Audio16Khz32KBitRateMonoMp3
    )

    return speech_config

def synthesize_speech(text: str):
    """
    Takes a sentence, returns audio bytes and viseme list.
    """

    speech_config = create_speech_config()
    visemes = []

    # No audio output config needed — we capture via stream after
    synthesizer = speechsdk.SpeechSynthesizer(
        speech_config=speech_config,
        audio_config=None        # ← None means don't play or save yet
    )

    # Hook into viseme events
    synthesizer.viseme_received.connect(
        lambda evt: visemes.append({
            "visemeId": evt.viseme_id,
            "offset":   evt.audio_offset
        })
    )

    # Run synthesis
    result = synthesizer.speak_text_async(text).get()

    if result.reason == speechsdk.ResultReason.SynthesizingAudioCompleted:
        # Capture audio from result directly
        stream = speechsdk.AudioDataStream(result)
        
        # Read all audio bytes into buffer
        buffer = bytes(32000)
        audio_bytes = b""
        while True:
            filled = stream.read_data(buffer)
            if filled == 0:
                break
            audio_bytes += buffer[:filled]

        return audio_bytes, visemes
    else:
        raise Exception(f"TTS failed: {result.reason}")
    

def process_sentence(text: str):
    """
    Calls Azure TTS and return everything frontend needs.

    Returns a dict:
    {
        'audio': base64 encoded MP3 string,
        'visemes': [{"visemesId": int, "offset": int}, ...]
    }
    """

    audio_bytes, visemes = synthesize_speech(text)

    # convert raw bytes to base64 string so it can travel in JSON
    audio_base64 = base64.b64encode(audio_bytes).decode("utf-8")

    return {
        "audio" : audio_base64,
        "visemes" : visemes
    }