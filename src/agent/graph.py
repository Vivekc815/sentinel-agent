from langgraph.graph import StateGraph, END
from src.agent.nodes import monitor_node, diagnose_node, remediate_node
from src.agent.state import SentinelState


def should_remediate(state:SentinelState) -> str:
    if state["drift_score"]>0.3:
        return "diagnose"
    return END

def build_graph():
    graph = StateGraph(SentinelState)

    graph.add_node("monitor", monitor_node)
    graph.add_node("diagnose", diagnose_node)
    graph.add_node("remediate", remediate_node)

    graph.set_entry_point("monitor")
    graph.add_conditional_edges("monitor", should_remediate)
    graph.add_edge("diagnose", "remediate")
    graph.add_edge("remediate", END)

    return graph.compile()
