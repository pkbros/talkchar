from fastapi import FastAPI, WebSocket
from fastapi.middleware.cors import CORSMiddleware
from llm_stream import stream_llm_response
from tts_stream import process_sentence

app = FastAPI()

# Allow React forntent to talk to this backend
app.add_middleware(
    CORSMiddleware,
    allow_origins = ["*"],
    allow_methods = ["*"],
    allow_headers = ["*"],
)
@app.get("/")
def health_check():
    return {"stauts": "TalkChar backend is running"}

@app.websocket("/ws")
async def websocket_endpoint(websocket: WebSocket):
    await websocket.accept()
    print("Client connected!")

    try:
        while True:
            # Waiting for message from frontend (the user input)
            user_message = await websocket.receive_text()
            print(f"Received: {user_message}")

            # Stream LLM response sentence by sentence
            async for sentence in stream_llm_response(user_message):
                tts_result = process_sentence(sentence["text"])

                # comibne everything into one payload
                payload = {
                    "text" : sentence['text'],
                    "emotion" : sentence['emotion'],
                    "pose" : sentence['pose'],
                    "audio" : tts_result['audio'],
                    "visemes" : tts_result['visemes']
                }

                await websocket.send_json(payload)
                print(f"Sent sentence: {sentence['text'][:40]}...")

    except Exception as e:
        print(f"Client disconnected: {e}")