from fastapi import APIRouter, HTTPException
from src.agent.graph import build_graph

router = APIRouter(prefix= "/sentinel", tags= ["sentinel"])

@router.post("/run")
def run_sentinel():
    try:
        graph = build_graph()
        result = graph.invoke({
            "predictions": [],
            "drift_score": 0.0,
            "diagnosis": "",
            "action_taken": "",
            "error": None,
            "messages": []
        })
        return {"status": "completed", "diagnosis": result["diagnosis"], "action_taken": result["action_taken"]}
    except Exception as e:
        raise HTTPException(status_code= 500, detail = str(e))