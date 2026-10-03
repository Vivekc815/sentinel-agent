from fastapi import FastAPI
from src.api.routes import sentinel
app = FastAPI(title = "Sentinel Agent")
app.include_router(sentinel.router)


@app.get("/")
def root():
    return {"message": "Sentinel is watching"}