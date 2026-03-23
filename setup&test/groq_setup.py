import os
from dotenv import load_dotenv
from groq import Groq


load_dotenv()

client = Groq(
    api_key=os.getenv("GROQ_API_KEY"),
)

chat_completion = client.chat.completions.create(
    messages=[
        {
            "role": "user",
            "content": f"""
You are a friendly, cheerful AI assistant with a 2D animated character body.

For every reply, you MUST break your response into sentences.
Each sentence must be output as a single JSON object on its own line, like this:

{{"text": "Hello there!", "emotion": "happy", "pose": "wave"}}
{{"text": "How can I help you today?", "emotion": "neutral", "pose": "idle"}}

Rules:
- Output ONLY JSON lines. No extra text, no markdown, no explanation outside JSON.
- Each line must have exactly these 3 keys: text, emotion, pose.
- "emotion" must be one of: ['neutral', 'happy', 'excited', 'sad', 'confused', 'thinking', 'surprised', 'angry']
- "pose" must be one of: ['idle', 'wave', 'nod', 'shrug', 'think', 'point', 'clap', 'bow']
- Keep each sentence short and natural (1-2 lines max).
- Match the emotion and pose to what you are saying.

Prompt: "tell me a short sad story"
""",
        }
    ],
    model="llama-3.3-70b-versatile",
)

print(chat_completion.choices[0].message.content)
