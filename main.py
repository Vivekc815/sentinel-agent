from fastapi import FastAPI
from src.api.routes import sentinel
from src.scheduler import start_scheduler
from src.models import Base
from sqlalchemy import create_engine
from src.core.config import settings
import logging
logging.basicConfig(level = logging.INFO)


engine = create_engine(settings.DATABASE_URL)
Base.metadata.create_all(engine)

app = FastAPI(title = "Sentinel Agent")
app.include_router(sentinel.router)

@app.on_event("startup")
def startup():
    start_scheduler()

@app.get("/")
def root():
    return {"message": "Sentinel is watching"}