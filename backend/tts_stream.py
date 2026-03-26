import azure.cognitiveservices.speech as speechsdk
import os
from dotenv import load_dotenv
import base64

load_dotenv()

AZURE_KEY = os.getenv("AZURE_SPEECH_KEY")
AZURE_REGION = os.getenv("AZURE_SPEECH_REGION")

# Map our emotions to Azure Jenny Neural styles
EMOTION_TO_STYLE = {
    "neutral": "friendly",
    "happy": "cheerful",
    "excited": "excited",
    "sad": "sad",
    "confused": "empathetic",
    "thinking": "whispering",
    "surprised": "excited",
    "angry": "angry",
}


def create_speech_config():
    speech_config = speechsdk.SpeechConfig(subscription=AZURE_KEY, region=AZURE_REGION)
    speech_config.set_speech_synthesis_output_format(
        speechsdk.SpeechSynthesisOutputFormat.Audio16Khz32KBitRateMonoMp3
    )
    return speech_config


def build_ssml(text: str, emotion: str) -> str:
    style = EMOTION_TO_STYLE.get(emotion, "friendly")
    return f"""<speak version='1.0' xmlns='http://www.w3.org/2001/10/synthesis'
    xmlns:mstts='http://www.w3.org/2001/mstts'
    xml:lang='en-US'>
    <voice name='en-US-JennyNeural'>
        <mstts:express-as style='{style}' styledegree='1.5'>
            {text}
        </mstts:express-as>
    </voice>
</speak>"""


def synthesize_speech(text: str, emotion: str = "neutral"):
    speech_config = create_speech_config()
    visemes = []

    synthesizer = speechsdk.SpeechSynthesizer(
        speech_config=speech_config, audio_config=None
    )

    synthesizer.viseme_received.connect(
        lambda evt: visemes.append(
            {"visemeId": evt.viseme_id, "offset": evt.audio_offset}
        )
    )

    # Use SSML instead of plain text
    ssml = build_ssml(text, emotion)
    result = synthesizer.speak_ssml_async(ssml).get()

    if result.reason == speechsdk.ResultReason.SynthesizingAudioCompleted:
        stream = speechsdk.AudioDataStream(result)
        buffer = bytes(32000)
        audio_bytes = b""
        while True:
            filled = stream.read_data(buffer)
            if filled == 0:
                break
            audio_bytes += buffer[:filled]
        return audio_bytes, visemes
    else:
        cancellation = result.cancellation_details
        raise Exception(f"TTS failed: {result.reason} — {cancellation.error_details}")


def process_sentence(text: str, emotion: str = "neutral"):
    audio_bytes, visemes = synthesize_speech(text, emotion)
    audio_base64 = base64.b64encode(audio_bytes).decode("utf-8")
    return {"audio": audio_base64, "visemes": visemes}
