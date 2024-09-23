import base64
import io
import os

import torchaudio
from fastapi import FastAPI, HTTPException, Request
from starlette.responses import JSONResponse

from tts_api.config import API_TOKEN
from tts_api.tts import dyn_voices, process_tts

app = FastAPI()


@app.get("/health")
def health_route():
    return "OK"


@app.post("/tts")
async def tts_route(request: Request):
    req = await request.json()
    if req["api_token"] != API_TOKEN:
        raise HTTPException(status_code=403, detail="Forbidden")

    speaker = req["speaker"]
    voice_file = os.path.join(dyn_voices, f"{speaker}.wav")
    if not os.path.exists(voice_file):
        raise HTTPException(status_code=404, detail="Speaker not found")

    audio = io.BytesIO()
    audio = process_tts(text=req["text"], speaker_wav=voice_file, output=audio)

    waveform, sample_rate = torchaudio.load(audio)
    buffer_ = io.BytesIO()
    torchaudio.save(buffer_, waveform, req["sample_rate"], format="ogg")
    buffer_.seek(0)

    return JSONResponse({"results": [{"audio": base64.b64encode(buffer_.getvalue()).decode()}]})
