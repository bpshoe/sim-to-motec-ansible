import sys
import os

sys.path.append(os.path.join(os.path.dirname(__file__), "third_party"))

from fastapi import FastAPI

app = FastAPI()

@app.get("/health")
def read_root():
    return {"status": "ok"}