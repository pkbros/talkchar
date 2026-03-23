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
    stream = client.chat.completions.create(
        model="llama-3.3-70b-versatile",
        messages=[
            {"role": "system", "content": SYSTEM_PROMPT},
            {"role": "user", "content": user_message},
        ],
        stream=True,
        temperature=0.7,
    )

    buffer = ""

    for chunk in stream:
        delta = chunk.choices[0].delta.content
        if delta is None:
            continue

        buffer += delta

        # Only split on newline when we have a complete JSON object
        while "\n" in buffer:
            line, buffer = buffer.split("\n", 1)
            line = line.strip()

            if not line:
                continue

            # Skip anything that doesn't look like JSON
            if not line.startswith("{"):
                continue

            try:
                sentence = json.loads(line)
                if "text" in sentence and "emotion" in sentence and "pose" in sentence:
                    yield sentence
            except json.JSONDecodeError:
                pass
