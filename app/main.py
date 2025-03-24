import os

import uvicorn
from fastapi import FastAPI

app = FastAPI(title="Health API")


@app.get("/")
def root():
    return {"message": "Health API is up"}


def main():
    host = os.getenv("API_HOST", "0.0.0.0")
    port = int(os.getenv("API_PORT", 8000))
    uvicorn.run("app.main:app", host=host, port=port, reload=True)
