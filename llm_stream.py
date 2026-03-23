# llm_stream.py
# Handles streaming responses from Groq LLM

import json
from groq import Groq
from dotenv import load_dotenv
import os
from llm_prompts import SYSTEM_PROMPT

# Load your API key from .env file
load_dotenv()
client = Groq(api_key=os.getenv("GROQ_API_KEY"))


# --- STREAMING FUNCTION ---
async def stream_llm_response(user_message: str):
    """
    Sends user message to Groq and streams back
    parsed sentences one by one.
    Each yielded item is a dict: {text, emotion, pose}
    """

    stream = client.chat.completions.create(
        model="llama-3.3-70b-versatile",
        messages=[
            {"role": "system", "content": SYSTEM_PROMPT},
            {"role": "user", "content": user_message},
        ],
        stream=True,
        temperature=0.7,
    )

    # Buffer to collect characters until we get a full JSON line
    buffer = ""

    for chunk in stream:
        # Extract the new text fragment from this chunk
        delta = chunk.choices[0].delta.content
        if delta is None:
            continue

        buffer += delta

        # Check if buffer contains a complete JSON line
        while "\n" in buffer:
            line, buffer = buffer.split("\n", 1)
            line = line.strip()

            if not line:
                continue

            # Try to parse the line as JSON
            try:
                sentence = json.loads(line)

                # Validate it has the keys we expect
                if "text" in sentence and "emotion" in sentence and "pose" in sentence:
                    yield sentence

            except json.JSONDecodeError:
                # LLM sent something that isn't valid JSON, skip it
                pass
