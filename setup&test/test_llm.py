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


from llm_stream import stream_llm_response #type:ignore ignoring as it will be handled by path_setup
import sys
import asyncio

async def main():
    user_input = "what's the meaning of life?"

    print("---LLM Response___")

    async for sentence in stream_llm_response(user_input):
        print(f"TEXT: {sentence['text']}")
        print(f"EMOTION: {sentence['emotion']}")
        print(f"POSE: {sentence['pose']}")
        print("---")

asyncio.run(main())