from langchain_openai import ChatOpenAI
from src.agent.tools import fetch_recent_predictions, calculate_drift_score, trigger_retraining
from src.agent.state import SentinelState
from src.core.config import settings
from langchain_core.messages import HumanMessage, SystemMessage

llm = ChatOpenAI(model = "gpt-4o-mini", api_key= settings.OPENAI_API_KEY)
tools = [fetch_recent_predictions, calculate_drift_score, trigger_retraining]
llm_with_tools = llm.bind_tools(tools)

def monitor_node(state: SentinelState) -> SentinelState:
    messages = [
        SystemMessage(content= "You are Sentinel, an autonomous ML monitoring agent"),
        HumanMessage(content="Check the pricing model for drift and take action if needed.")
    ]
    response = llm_with_tools.invoke(messages)
    return {"diagnosis":response.content, "action_taken": "completed"}





