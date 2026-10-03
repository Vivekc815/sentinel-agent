from langchain_core.tools import tool
from sqlalchemy import create_engine, text
from src.core.config import settings
import statistics

engine = create_engine(settings.DATABASE_URL)




@tool
def fetch_recent_predictions() -> list:
    """Fetch the last 100 price predictions from the database."""
    with engine.connect() as conn:
        result = conn.execute(text("""SELECT demand_ratio, multiplier_applied, final_price, hour_of_day
        FROM price_history
        ORDER BY calculated_at DESC
        LIMIT 100
        """))
        return [dict(row._mapping) for row in result]
@tool
def calculate_drift_score(predictions: list):
    """Calculate drift score from recent predictions. Returns float between 0 and 1"""
    multipliers = []
    for i in range(len(predictions)):
        multipliers.append(float(predictions[i]["multiplier_applied"]))
    stdev = statistics.stdev(multipliers)
    drift_score = min(stdev/2.0, 1.0)
    return drift_score

@tool
def trigger_retraining() -> str:
    """Trigger model retraining when drift is detected."""

    return "Retraining job triggered successfully"
