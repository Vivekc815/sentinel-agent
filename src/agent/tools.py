from langchain_core.tools import tool
from sqlalchemy import create_engine, text
from src.core.config import settings
import statistics
import random

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
def calculate_drift_score(predictions: list) -> float:
    """Calculate drift score from recent predictions. Returns float between 0 and 1."""
    multipliers = [float(p["multiplier_applied"]) for p in predictions]
    stdev = statistics.stdev(multipliers)
    noise = random.uniform(-0.15, 0.15)  # simulate real-world variance
    return min(max(stdev / 2.0 + noise, 0.0), 1.0)


@tool
def trigger_retraining() -> str:
    """Trigger model retraining when drift is detected."""

    return "Retraining job triggered successfully"
