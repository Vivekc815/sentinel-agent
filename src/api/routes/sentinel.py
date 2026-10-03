from fastapi import APIRouter, HTTPException
from src.agent.graph import build_graph

router = APIRouter(prefix= "/sentinel", tags= ["sentinel"])

@router.post("/run")
def run_sentinel():
    try:
        graph = build_graph()
        result = graph.invoke({"messages": []})
        final_message = result["messages"][-1].content
        return {"status": "completed", "diagnosis": final_message}

    except Exception as e:
        raise HTTPException(status_code= 500, detail = str(e))