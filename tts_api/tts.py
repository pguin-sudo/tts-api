import glob
import os
import warnings
from datetime import datetime
from io import BytesIO

import torch
import torchaudio
from TTS.api import TTS

from tts_api.config import THREADS

warnings.filterwarnings("ignore")

torchaudio.set_audio_backend("sox")
torch.set_num_threads(THREADS)

cuda_available = torch.cuda.is_available()
print("Starting with cuda") if cuda_available else print("Cuda is not available")

dyn_voices = os.getcwd() + "/speakers"
tts = TTS("tts_models/multilingual/multi-dataset/xtts_v2", gpu=cuda_available)


def process_tts(text: str, speaker_wav: str, output: str or BytesIO) -> str:
    return tts.tts_to_file(text=text, speaker_wav=speaker_wav, language="ru", file_path=output)


example_text = "ГОЙ ДА! С В О! ГОЙ ДА! С В О!"


def warm_up():
    print("WarmUp!")
    for speaker in glob.glob(dyn_voices + "\\*.wav"):
        start_time = datetime.now()
        process_tts(text=example_text, speaker_wav=speaker, output=f"{speaker}.test.wav")
        end_time = datetime.now()
        print(f"Speaker: {speaker} {end_time - start_time}")

# warm_up()
