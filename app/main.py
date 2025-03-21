import uvicorn
from fastapi import FastAPI

app = FastAPI(title="Health API")


@app.get("/")
def root():
    return {"message": "Health API is up"}


def main():
    uvicorn.run("app.main:app", host="127.0.0.1", port=8000, reload=True)
