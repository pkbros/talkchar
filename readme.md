TalkChar is a next-generation real-time conversational avatar system that transforms plain text into a living 2D character.

It combines LLM intelligence + emotional expression + lip-synced speech to create highly immersive, human-like interactions.

💡 Imagine ChatGPT… but it talks, reacts, and feels.
**Architecture: Sentence Level Streaming**
```
User Input
    ↓
Groq API (LLM) → streams sentence by sentence
    ↓
Each sentence has JSON tag (text + emotion + pose)
    ↓                        ↓
Azure TTS (audio)      Pose/Expression
+ viseme events        on character
    ↓                        ↓
         React + PixiJS
    Lip sync via visemes + animation clips
```

---

**Final Stack**
| Layer | Tool |
|---|---|
| LLM | Groq API |
| TTS + Visemes | Azure TTS (Student account) |
| Character | PixiJS + DragonBones 2D |
| Frontend | React |
| Backend | FastAPI + Python |
| Realtime | WebSockets |

---

**Environment**
| Item | Location |
|---|---|
| Project code | D:\projects\TalkChar |
| Conda env | D:\conda_envs\talkchar |
| Python | 3.10 |

---

**Installed Packages**
- fastapi 0.135.1
- uvicorn 0.42.0
- websockets 16.0
- groq 1.1.1
- azure-cognitiveservices-speech 1.48.2
- python-dotenv 1.2.2

---

**What's Pending**
1. Test Azure TTS via azure_setup.py (done)
2. Design LLM JSON tag structure
3. Build FastAPI WebSocket backend
4. Build React + PixiJS frontend
5. Connect full pipeline end to end

---
