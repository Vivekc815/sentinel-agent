from fastapi import FastAPI
from src.api.routes import sentinel
from src.scheduler import start_scheduler
import logging
logging.basicConfig(level = logging.INFO)


app = FastAPI(title = "Sentinel Agent")
app.include_router(sentinel.router)

@app.on_event("startup")
def startup():
    start_scheduler()

@app.get("/")
def root():
    return {"message": "Sentinel is watching"}