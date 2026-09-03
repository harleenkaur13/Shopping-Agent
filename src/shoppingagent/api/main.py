from fastapi import FastAPI
from pydantic import BaseModel
from langgraph.types import Command
import uuid

from shoppingagent.agent.agent import agent

app = FastAPI()


# --- Request/response shapes, defined with Pydantic ---

class ChatRequest(BaseModel):
    thread_id: str
    message: str

class ChatResponse(BaseModel):
    thread_id: str
    reply: str
    needs_approval: bool = False
    pending_action: dict | None = None

class ResumeRequest(BaseModel):
    thread_id: str
    approve: bool


# --- Endpoint 1: start a new conversation ---

@app.post("/chat/start")
def start_chat():
    """Creates a brand new conversation and returns its thread_id."""
    new_thread_id = str(uuid.uuid4())
    return {"thread_id": new_thread_id}


# --- Endpoint 2: send a message in an existing conversation ---

@app.post("/chat", response_model=ChatResponse)
def chat(request: ChatRequest):
    config = {"configurable": {"thread_id": request.thread_id}}

    result = agent.invoke(
        {"messages": [{"role": "user", "content": request.message}]},
        config=config,
    )

    return _build_response(request.thread_id, result)


# --- Endpoint 3: resume a paused conversation (approve/reject checkout) ---

@app.post("/chat/resume", response_model=ChatResponse)
def resume_chat(request: ResumeRequest):
    config = {"configurable": {"thread_id": request.thread_id}}

    decision = {"type": "approve"} if request.approve else {"type": "reject", "message": "User declined checkout."}

    result = agent.invoke(
        Command(resume={"decisions": [decision]}),
        config=config,
    )

    return _build_response(request.thread_id, result)


# --- Shared helper: turns the agent's raw result into our clean response shape ---

def _build_response(thread_id: str, result: dict) -> dict:
    if "__interrupt__" in result:
        action = result["__interrupt__"][0].value["action_requests"][0]
        return {
            "thread_id": thread_id,
            "reply": "This action needs your approval before it can proceed.",
            "needs_approval": True,
            "pending_action": {"name": action["name"], "args": action["args"]},
        }

    return {
        "thread_id": thread_id,
        "reply": result["messages"][-1].content,
        "needs_approval": False,
        "pending_action": None,
    }