from fastapi import FastAPI, HTTPException
from fastapi.middleware.cors import CORSMiddleware
from ....infrastructure.config import settings
from ....infrastructure.orchestration.langgraph_orchestrator import LangGraphOrchestrator
from ....infrastructure.agents.reasoning_agent import ReasoningAgent
from ....infrastructure.agents.more_agents import SynthesisAgent, AnalysisAgent
from ....application.use_cases.execute_task import ExecuteTaskUseCase
from pydantic import BaseModel
from typing import List, Optional

app = FastAPI(title="ATP Evolved", version="0.7.0")

app.add_middleware(
    CORSMiddleware,
    allow_origins=settings.CORS_ORIGINS,
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Composition Root
orchestrator = LangGraphOrchestrator()
execute_task_use_case = ExecuteTaskUseCase(orchestrator)

# DTOs (Infrastructure/Delivery layer DTOs, usually mapped from partial Application DTOs)
class ChatRequest(BaseModel):
    message: str
    agents: List[str] = ["reasoning", "synthesis"]

@app.post("/api/chat")
async def chat(request: ChatRequest):
    # Instantiate agents on demand or from a pool
    # For now, creating fresh instances as per incoming config (simple factory)
    agents = []
    for agent_id in request.agents:
        if agent_id == "reasoning":
            agents.append(ReasoningAgent())
        elif agent_id == "synthesis":
            agents.append(SynthesisAgent())
        elif agent_id == "analysis":
            agents.append(AnalysisAgent())
            
    if not agents:
        agents = [ReasoningAgent(), SynthesisAgent()] # Default

    result = await execute_task_use_case.execute(
        task=request.message,
        agents=agents,
        context={"original_request": request.dict()}
    )
    
    # result["final_result"] is now a List[Dict] with the structured conversation.
    # The frontend should interpret 'final_result' as an array of messages objects
    # to render them as distinct bubbles.
    """
    Returns:
        {
            success: bool,
            final_result: List[{agent_id, content, ...}],
            ...
        }
    """
    return result

@app.get("/health")
def health():
    return {"status": "ok", "version": "0.7.0"}

if __name__ == "__main__":
    import uvicorn
    uvicorn.run(app, host=settings.HOST, port=settings.PORT)
