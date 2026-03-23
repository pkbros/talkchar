# below is the boilerplate to resolve any path issues on relative import
import sys
from pathlib import Path

# Walk up from this file until we find path_setup.py
current = Path(__file__).resolve().parent
while not (current / "path_setup.py").exists():
    current = current.parent
sys.path.append(str(current))
import path_setup

# ----------------------

import asyncio
import websockets
import json
import base64


async def test():
    uri = "ws://localhost:8000/ws"

    async with websockets.connect(uri) as ws:
        print("Connected to WebSocket!\n")

        # send a message
        await ws.send("who are you?")
        print("Message sent, waiting for response...\n")

        # keep recieving until connection closes
        while True:
            try:
                data = await ws.recv()
                payload = json.loads(data)
                print(f"TEXT: {payload['text']}")
                print(f"EMOTION: {payload['emotion']}")
                print(f"POSE: {payload['pose']}")
                # Audio
                audio_bytes = base64.b64decode(payload["audio"])
                print(f"AUDIO:   {len(audio_bytes)} bytes")

                # Visemes
                print(f"VISEMES: {len(payload['visemes'])} events")
                for v in payload["visemes"][:3]:  # show first 3 only
                    print(
                        f"         shape {v['visemeId']:2d} at {v['offset'] / 10000:.0f}ms"
                    )

                print("---")


            except websockets.exceptions.ConnectionClosed:
                print("Connection closed.")
                break


asyncio.run(test())
