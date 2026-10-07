from sqlalchemy import Column, String, Float, DateTime, Text
from sqlalchemy.orm import declarative_base
from datetime import datetime
import uuid

Base = declarative_base()

class SentinelRun(Base):
    __tablename__ = "sentinel_runs"

    id = Column(String, primary_key= True, default = lambda: str(uuid.uuid4()))
    drift_score = Column(Float)
    diagnosis = Column(Text)
    action_taken = Column(String)
    ran_at = Column(DateTime, default = datetime.utcnow)