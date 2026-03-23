# below is the boilerplate to resolve any path issues on relative import 
import sys
from pathlib import Path
# Walk up from this file until we find path_setup.py
current = Path(__file__).resolve().parent
while not (current / "path_setup.py").exists():
    current = current.parent
sys.path.append(str(current))
import path_setup
#----------------------

import base64
from tts_stream import process_sentence #type: ignore will be handled by 

text = "Hello! I am your friendly AI assistant."

print(f"Testing TTS for: '{text}'\n")

result = process_sentence(text)

# Check audio
audio_bytes = base64.b64decode(result["audio"])
print(f"✅ Audio received: {len(audio_bytes)} bytes")

# Check visemes
print(f"✅ Visemes received: {len(result['visemes'])} events")
print("\nViseme list:")
for v in result["visemes"]:
    print(f"  mouth shape {v['visemeId']:2d}  at offset {v['offset']}")

# Save audio to file so we can listen to it
output_path = Path(__file__).parent / "test_output.mp3"
with open(output_path, "wb") as f:
    f.write(audio_bytes)
print(f"\n✅ Audio saved to: {output_path}")
print("Open test_output.mp3 to hear the voice!")