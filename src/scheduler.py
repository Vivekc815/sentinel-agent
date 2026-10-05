from apscheduler.schedulers.background import BackgroundScheduler
from src.agent.graph import build_graph
import logging

logger = logging.getLogger(__name__)

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

    logger.info(f"Drift score : {result['drift_score']}")
    logger.info(f"Action taken: {result['action_taken']}")
    logger.info(f"Diagnosis : {result['diagnosis'][:100]}...")

def start_scheduler():
    scheduler = BackgroundScheduler()
    scheduler.add_job(run_sentinel, "interval", minutes = 30)
    scheduler.start()
    logger.info("Sentinel scheduler started - running every 30 minutes")
    return scheduler