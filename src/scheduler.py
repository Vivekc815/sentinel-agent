from apscheduler.schedulers.background import BackgroundScheduler
from src.agent.graph import build_graph
from src.models import SentinelRun, Base
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from src.core.config import settings
import logging

logger = logging.getLogger(__name__)

engine = create_engine(settings.DATABASE_URL)
SessionLocal = sessionmaker(bind = engine)

def run_sentinel():
    logger.info("Sentinel scheduled run starting...")
    graph = build_graph()
    result = graph.invoke({
        "predictions": [],
        "drift_score" : 0.0,
        "diagnosis" : "",
        "action_taken" : "",
        "error" : None,
        "messages" : []
    })
    session = SessionLocal()
    try:
        run = SentinelRun(
            drift_score = result["drift_score"],
            diagnosis = result["diagnosis"],
            action_taken = result["action_taken"]
        )
        session.add(run)
        session.commit()

        logger.info(f"Drift score : {result['drift_score']}")
        logger.info(f"Action taken: {result['action_taken']}")
        logger.info(f"Diagnosis : {result['diagnosis'][:100]}...")
    except Exception as e:
        logger.error(f"Failed to save run : {e}")
        session.rollback()
    finally:
        session.close()
def start_scheduler():
    scheduler = BackgroundScheduler()
    scheduler.add_job(run_sentinel, "interval", minutes = 30)
    scheduler.start()
    logger.info("Sentinel scheduler started - running every 30 minutes")
    return scheduler