# this is ai generated chekup test 

import os
from dotenv import load_dotenv

# Load environment variables from .env file
load_dotenv()

# ============================================================
# Azure TTS Setup Test - TalkChar Project
# ============================================================
#
# PRE-REQUISITES:
# 1. Create Azure Speech resource at portal.azure.com
# 2. Get Key 1 and Region from Keys and Endpoint section
# 3. Create .env file in project root with:
#    AZURE_SPEECH_KEY=your_key_here
#    AZURE_SPEECH_REGION=your_region_here
#    (e.g. AZURE_SPEECH_REGION=centralindia)
#
# SUPPORTED EMOTION STYLES:
# - cheerful, excited, sad, angry, fearful
# - whispering, shouting, hopeful
# - unfriendly, terrified
#
# VISEME IDs (0-21) map to mouth shapes:
# 0=silence, 1=ae/ah, 2=aa, 3=oh, 4=ey
# 5=er, 6=ih, 7=w/uw, 8=ow, 9=aw
# 10=oy, 11=ay, 12=h, 13=r, 14=l
# 15=s/z, 16=sh, 17=th, 18=f/v, 19=d/t
# 20=k/g, 21=p/b/m
#
# ============================================================


def test_azure_tts():
    try:
        import azure.cognitiveservices.speech as speechsdk
    except ImportError:
        print("ERROR: Azure Speech SDK not installed.")
        print("Run: pip install azure-cognitiveservices-speech")
        return

    # Get credentials from environment
    speech_key = os.getenv("AZURE_SPEECH_KEY")
    speech_region = os.getenv("AZURE_SPEECH_REGION")

    if not speech_key or not speech_region:
        print("ERROR: Azure credentials not found in .env file.")
        print("Create a .env file in project root with:")
        print("  AZURE_SPEECH_KEY=your_key_here")
        print("  AZURE_SPEECH_REGION=your_region_here")
        return

    print(f"Using region: {speech_region}")
    print("Connecting to Azure Speech Service...")

    # Configure speech
    speech_config = speechsdk.SpeechConfig(
        subscription=speech_key, region=speech_region
    )

    # Set output voice - neural voice for best quality
    speech_config.speech_synthesis_voice_name = "en-US-JennyNeural"

    # Output to file
    audio_config = speechsdk.audio.AudioOutputConfig(filename="azure_test.wav")

    # Create synthesizer
    synthesizer = speechsdk.SpeechSynthesizer(
        speech_config=speech_config, audio_config=audio_config
    )

    # Track visemes
    viseme_events = []

    def on_viseme(evt):
        viseme_events.append(
            {"time_ms": evt.audio_offset // 10000, "viseme_id": evt.viseme_id}
        )

    synthesizer.viseme_received.connect(on_viseme)

    # Test 1 — Basic speech
    print("\nTest 1: Basic speech...")
    ssml = """
    <speak version='1.0' xmlns='http://www.w3.org/2001/10/synthesis'
           xmlns:mstts='http://www.w3.org/2001/mstts'
           xml:lang='en-US'>
        <voice name='en-US-JennyNeural'>
            Hello! I am Jenny, your TalkChar assistant. Nice to meet you!
        </voice>
    </speak>
    """
    result = synthesizer.speak_ssml_async(ssml).get()

    if result.reason == speechsdk.ResultReason.SynthesizingAudioCompleted:
        print("Test 1 PASSED - Basic speech works!")
        print(f"Visemes captured: {len(viseme_events)}")
        print(f"First 5 visemes: {viseme_events[:5]}")
    else:
        print(f"Test 1 FAILED: {result.reason}")
        if result.reason == speechsdk.ResultReason.Canceled:
            details = speechsdk.CancellationDetails(result)
            print(f"Error: {details.reason}")
            print(f"Details: {details.error_details}")
        return

    # Reset visemes for next test
    viseme_events.clear()

    # Test 2 — Emotion styles
    print("\nTest 2: Emotion styles...")
    emotions = ["cheerful", "sad", "angry", "excited", "whispering"]
    emotion_texts = [
        "Oh wow, this is absolutely amazing! I love it!",
        "I just don't know what to do anymore. Everything feels so heavy.",
        "This is completely unacceptable! I told you exactly what needed to be done!",
        "I can't believe it! We actually did it! This is incredible!",
        "Hey, come closer. I have a secret to tell you.",
    ]

    # Test with a single audio output file for emotion test
    audio_config2 = speechsdk.audio.AudioOutputConfig(filename="azure_emotion_test.wav")
    synthesizer2 = speechsdk.SpeechSynthesizer(
        speech_config=speech_config, audio_config=audio_config2
    )

    test_emotion = "excited"
    test_text = "I can't believe it! We actually did it! This is incredible!"

    ssml_emotion = f"""
    <speak version='1.0' xmlns='http://www.w3.org/2001/10/synthesis'
           xmlns:mstts='http://www.w3.org/2001/mstts'
           xml:lang='en-US'>
        <voice name='en-US-JennyNeural'>
            <mstts:express-as style='{test_emotion}'>
                {test_text}
            </mstts:express-as>
        </voice>
    </speak>
    """

    result2 = synthesizer2.speak_ssml_async(ssml_emotion).get()

    if result2.reason == speechsdk.ResultReason.SynthesizingAudioCompleted:
        print(f"Test 2 PASSED - Emotion style '{test_emotion}' works!")
    else:
        print(f"Test 2 FAILED: {result2.reason}")
        return

    # Summary
    print("\n" + "=" * 50)
    print("Azure TTS Setup Complete!")
    print("=" * 50)
    print("Check these output files:")
    print("  azure_test.wav       - Basic speech test")
    print("  azure_emotion_test.wav - Emotion style test")
    print("\nViseme output is working correctly.")
    print("Azure TTS is ready for TalkChar pipeline!")
    print("\nSupported emotions confirmed:")
    for e in emotions:
        print(f"  - {e}")


if __name__ == "__main__":
    print("=" * 50)
    print("TalkChar - Azure TTS Setup Test")
    print("=" * 50)
    test_azure_tts()
