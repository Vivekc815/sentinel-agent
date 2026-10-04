from langchain_openai import ChatOpenAI
from src.agent.tools import fetch_recent_predictions, calculate_drift_score, trigger_retraining
from src.agent.state import SentinelState
from src.core.config import settings
from langchain_core.messages import HumanMessage, SystemMessage

llm = ChatOpenAI(model = "gpt-4o-mini", api_key= settings.OPENAI_API_KEY)
tools = [fetch_recent_predictions, calculate_drift_score, trigger_retraining]
llm_with_tools = llm.bind_tools(tools)

def monitor_node(state: SentinelState) -> SentinelState:
    predictions = fetch_recent_predictions.invoke({})
    drift_score = calculate_drift_score.invoke({"predictions": predictions})
    return{"predictions": predictions, "drift_score": drift_score}

def diagnose_node(state: SentinelState) -> dict:
    response = llm.invoke([
        SystemMessage(content = "You are Sentinel. Analyze the drift score and explain why retraining is needed."),
        HumanMessage(content= f"Drift score is {state['drift_score']}. Recent predictions :{state['predictions'][:5]}")
    ])
    return {"diagnosis" : response.content}

def remediate_node(state: SentinelState) -> dict:
    result = trigger_retraining.invoke({})
    return {"action_taken" : result}




