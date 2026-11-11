"""FastAPI Server Entrypoint for CSIP Live Inference & Drift Observatory.

Run directly via:
    python app/api_server.py
Or via Uvicorn CLI:
    uvicorn app.api_server:app --host 127.0.0.1 --port 8000
"""

import uvicorn
from csip.api.server import app

if __name__ == "__main__":
    uvicorn.run("csip.api.server:app", host="127.0.0.1", port=8000, reload=False)
