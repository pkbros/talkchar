import sys
from pathlib import Path

current = Path(__file__).resolve().parent
while not (current / "path_setup.py").exists():
    current = current.parent
sys.path.append(str(current))
import path_setup

import asyncio
import websockets
import json
import base64
import shutil

OUTPUT_DIR = Path(__file__).resolve().parent.parent / "mp3output"


def prepare_output_dir():
    if OUTPUT_DIR.exists():
        shutil.rmtree(OUTPUT_DIR)
    OUTPUT_DIR.mkdir(parents=True)
    print(f"Output folder ready: {OUTPUT_DIR}")


async def test():
    prepare_output_dir()

    uri = "ws://localhost:8000/ws"
    sentence_index = 0

    async with websockets.connect(uri) as ws:
        print("Connected to WebSocket!")

        user_input = input("Enter your message: ").strip()
        if not user_input:
            user_input = "What are the biggest threats to humanity?"

        await ws.send(json.dumps({"text": user_input}))
        print(f"Message sent: {user_input}")
        print("Waiting for response...\n")

        async for raw in ws:
            data = json.loads(raw)

            text = data.get("text", "")
            emotion = data.get("emotion", "unknown")
            pose = data.get("pose", "unknown")
            audio = data.get("audio", "")
            visemes = data.get("visemes", [])

            sentence_index += 1

            print(f"--- Sentence {sentence_index} ---")
            print(f"TEXT:    {text}")
            print(f"EMOTION: {emotion}")
            print(f"POSE:    {pose}")
            print(f"VISEMES: {len(visemes)} events")
            if visemes:
                for v in visemes[:3]:
                    ms = v["offset"] / 10000
                    print(f"         shape {v['visemeId']:2d} at {ms:.0f}ms")

            # Save audio
            if audio:
                audio_bytes = base64.b64decode(audio)
                filename = OUTPUT_DIR / f"sentence_{sentence_index:02d}_{emotion}.mp3"
                with open(filename, "wb") as f:
                    f.write(audio_bytes)
                print(f"AUDIO:   saved → {filename.name}  ({len(audio_bytes):,} bytes)")
            else:
                print("AUDIO:   none")

            print()


if __name__ == "__main__":
    asyncio.run(test())
