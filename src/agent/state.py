from typing import TypedDict, Optional, List

class SentinelState(TypedDict):
    predictions: list
    drift_score: float
    diagnosis: str
    action_taken: str
    error: Optional[str]
