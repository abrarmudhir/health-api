import os

import uvicorn
from fastapi import FastAPI

from app.routes import create_medication, read_medication, update_medication_request

app = FastAPI(title="Health API")


app.include_router(create_medication.router)
app.include_router(read_medication.router)
app.include_router(update_medication_request.router)


def main():
    host = os.getenv("API_HOST", "0.0.0.0")
    port = int(os.getenv("API_PORT", 8000))
    uvicorn.run("app.main:app", host=host, port=port, reload=True)
