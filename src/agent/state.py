from typing import TypedDict, Optional, List, Annotated
from langgraph.graph.message import add_messages

class SentinelState(TypedDict):
    predictions: list
    drift_score: float
    diagnosis: str
    action_taken: str
    error: Optional[str]
    messages: Annotated[list, add_messages]