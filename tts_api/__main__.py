import os

import uvicorn

from tts_api.routes import app

print("API init!")
uvicorn.run(app, host="0.0.0.0", port=int(os.environ.get("PORT", "5000")))
print("API is running!")
