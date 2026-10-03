from langgraph.prebuilt import create_react_agent
from langchain_core.messages import SystemMessage
from src.agent.tools import fetch_recent_predictions, calculate_drift_score, trigger_retraining
from src.agent.nodes import llm


tools = [fetch_recent_predictions, calculate_drift_score, trigger_retraining]

system_prompt = SystemMessage(content="You are Sentinel, an autonomous ML monitoring agent. Fetch recent predictions, calculate drift score, and trigger retraining if drift score is above 0.3.")


def build_graph():
    return create_react_agent(llm, tools=tools, prompt=system_prompt)