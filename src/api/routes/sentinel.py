from fastapi import APIRouter, HTTPException
from src.agent.graph import build_graph
from src.models import SentinelRun
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from src.core.config import settings

engine = create_engine(settings.DATABASE_URL)
SessionLocal = sessionmaker(bind=engine)

router = APIRouter(prefix="/sentinel", tags=["sentinel"])

@router.post("/run")
def run_sentinel():
    try:
        graph = build_graph()
        result = graph.invoke({
            "predictions": [],
            "drift_score": 0.0,
            "diagnosis": "",
            "action_taken": "",
            "error": None,
            "messages": []
        })
        session = SessionLocal()
        try:
            run = SentinelRun(
                drift_score=result["drift_score"],
                diagnosis=result["diagnosis"],
                action_taken=result["action_taken"]
            )
            session.add(run)
            session.commit()
        finally:
            session.close()
        return {"status": "completed", "diagnosis": result["diagnosis"], "action_taken": result["action_taken"]}
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))