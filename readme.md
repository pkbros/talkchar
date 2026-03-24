# TalkChar

A real-time talking 2D character powered by LLM with emotions, poses, and lip sync.

## What it does

TalkChar lets you have a live voice conversation with an animated 2D character. The character listens to you, thinks, speaks back with a real voice, and physically reacts — changing facial expressions, body poses, and mouth movements in sync with what it says.

## Stack

| Layer | Tool |
|---|---|
| LLM | Groq API (llama-3.3-70b-versatile) |
| TTS + Lip sync | Azure Cognitive Services (JennyNeural) |
| Character | PixiJS + DragonBones 2D |
| Frontend | React |
| Backend | FastAPI + Python |
| Realtime | WebSockets |

## Project Structure

```
TalkChar/
├── path_setup.py           # Root marker + shared path manager
├── .env                    # API keys (never commit this)
├── backend/
│   ├── main.py             # FastAPI app + WebSocket endpoint
│   ├── llm_prompt.py       # Emotions, poses, and system prompt
│   ├── llm_stream.py       # Groq LLM response parser
│   └── tts_stream.py       # Azure TTS + viseme extractor
├── frontend/               # React + PixiJS app (coming soon)
└── setup&test/
    ├── path_setup.py       # Import this at top of every test
    ├── test_llm.py         # Test LLM streaming
    ├── test_tts.py         # Test Azure TTS + visemes
    ├── test_websocket.py   # Test full WebSocket pipeline
    ├── azure_setup.py      # Azure credentials check
    └── groq_setup.py       # Groq credentials check
```

## How it works

```
User speaks or types
        ↓
WebSocket → FastAPI backend
        ↓
Groq LLM → streams sentences as JSON
{ "text": "...", "emotion": "happy", "pose": "wave" }
        ↓
Azure TTS → audio (MP3) + viseme timing map
        ↓
Combined payload sent to frontend
        ↓
React plays audio + PixiJS animates character
```

## Setup

**1. Clone and create conda environment**
```bash
conda create -p D:\conda_envs\talkchar python=3.10
conda activate talkchar
```

**2. Install dependencies**
```bash
pip install fastapi uvicorn websockets groq azure-cognitiveservices-speech python-dotenv
```

**3. Add API keys to `.env`**
```
GROQ_API_KEY=your_groq_key
AZURE_SPEECH_KEY=your_azure_key
AZURE_SPEECH_REGION=your_azure_region
```

**4. Run the backend**
```bash
cd backend
uvicorn main:app --reload
```

## Character Emotions

`neutral` `happy` `excited` `sad` `confused` `thinking` `surprised` `angry`

## Character Poses

`idle` `wave` `nod` `shrug` `think` `point` `clap` `bow`

## Status

- [x] LLM JSON structure
- [x] Groq streaming
- [x] FastAPI WebSocket backend
- [x] Azure TTS + visemes
- [ ] React + PixiJS frontend
- [ ] Voice input (Web Speech API)
- [ ] Full pipeline end-to-end
