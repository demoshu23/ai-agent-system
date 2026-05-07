from fastapi import FastAPI
from pydantic import BaseModel
from .graph import run_workflow

app = FastAPI()


class RunRequest(BaseModel):
    session_id: str
    goal: str


@app.post("/run")
async def run(req: RunRequest):
    state = await run_workflow(req.session_id, req.goal)
    return {
        "session_id": req.session_id,
        "goal": state.get("goal"),
        "plan": state.get("plan"),
        "research": state.get("research"),
        "result": state.get("result"),
    }
