from typing import Dict, Any, List, Optional, TypedDict
from datetime import datetime
import uuid
import traceback

# External Frameworks (Infrastructure)
try:
    from langgraph.graph import StateGraph, END
except ImportError:
    pass

from ...domain.ports.output.orchestrator_port import OrchestratorPort
from ...domain.ports.input.agent_port import AgentPort
from ...domain.entities.a2a_types import (
    A2AMessage, A2AResponse, AgentCapability, AgentProfile,
    MessageType, Priority, AgentStatus
)
from ...domain.services.a2a_service import a2a_service

class AgentState(TypedDict):
    user_query: str
    context: Dict[str, Any]
    a2a_messages: List[A2AMessage]
    a2a_responses: List[A2AResponse]
    current_step: str
    next_agent: Optional[str]
    agents_to_execute: List[str]
    agents_completed: List[str]
    intermediate_results: Dict[str, Any]
    final_result: Any # Changed from Optional[str] to allow List[Dict]
    conversation_id: str
    start_time: datetime
    is_complete: bool
    error: Optional[str]

class LangGraphOrchestrator(OrchestratorPort):
    def __init__(self):
        self.agents: Dict[str, AgentPort] = {}
        self.protocol = a2a_service
        self._register_orchestrator_agent()
        self.graph = None
        self.stats = {
            "total_queries": 0,
            "successful_queries": 0,
            "failed_queries": 0,
            "total_a2a_messages": 0,
            "average_response_time_ms": 0.0
        }

    def _register_orchestrator_agent(self) -> None:
        orchestrator_id = "orchestrator"
        if orchestrator_id in self.protocol.agent_registry:
            return

        orchestrator_profile = AgentProfile(
            agent_id=orchestrator_id,
            name="LangGraph Orchestrator",
            primary_capability=AgentCapability.REASONING,
            specialization="Workflow coordination and messaging",
            description="Nodo central que coordina el flujo LangGraph y enruta mensajes A2A.",
            backstory="Entidad de orquestación encargada de mantener la integridad del pipeline.",
            model_name="orchestrator",
            temperature=0.0,
            max_tokens=1,
        )
        self.protocol.register_agent(orchestrator_profile)

    def register_agents(self, agents: List[AgentPort]) -> None:
        self.agents = {}
        for agent in agents:
            if hasattr(agent, 'profile'):
                agent_id = agent.profile.agent_id
                self.agents[agent_id] = agent
                self.protocol.register_agent(agent.profile)
        self.graph = self._build_graph()

    def _build_graph(self) -> StateGraph:
        workflow = StateGraph(AgentState)
        workflow.add_node("analyze_query", self._analyze_query)
        workflow.add_node("execute_agents", self._execute_agents)
        workflow.add_node("synthesize", self._synthesize_results)
        workflow.add_node("finalize", self._finalize_result)
        workflow.set_entry_point("analyze_query")
        workflow.add_edge("analyze_query", "execute_agents")
        workflow.add_conditional_edges(
            "execute_agents",
            self._should_continue,
            {
                "continue": "execute_agents",
                "synthesize": "synthesize"
            }
        )
        workflow.add_edge("synthesize", "finalize")
        workflow.add_edge("finalize", END)
        return workflow.compile()

    async def execute_task(
        self,
        task: str,
        agents: List[AgentPort],
        context: Optional[Dict[str, Any]] = None
    ) -> Dict[str, Any]:
        try:
            # Sort agents by level
            sorted_agents = sorted(agents, key=lambda a: getattr(a.profile, "level", 1))
            
            # Validation: Max 1 agent per level
            levels_seen = set()
            validated_agents = []
            for agent in sorted_agents:
                level = getattr(agent.profile, "level", 1)
                if level in levels_seen:
                    # Skip or Error? User said "SOLO SE PODRA USAR 1". 
                    # We will enforce strictly by skipping duplicates or taking the first one.
                    # Let's take the first one (already sorted effectively by original order if stable sort, 
                    # but here we just want unique levels).
                    continue
                levels_seen.add(level)
                validated_agents.append(agent)

            self.register_agents(validated_agents)
            
            conversation_id = str(uuid.uuid4())
            start_time = datetime.utcnow()
            
            agent_ids = [a.profile.agent_id for a in validated_agents]

            initial_state: AgentState = {
                "user_query": task,
                "context": context or {},
                "a2a_messages": [],
                "a2a_responses": [],
                "current_step": "init",
                "next_agent": None,
                "agents_to_execute": agent_ids,
                "agents_completed": [],
                "intermediate_results": {},
                "final_result": None,
                "conversation_id": conversation_id,
                "start_time": start_time,
                "is_complete": False,
                "error": None
            }
            final_state = await self.graph.ainvoke(initial_state)
            processing_time = (datetime.utcnow() - start_time).total_seconds() * 1000
            self.stats["total_queries"] += 1
            self.stats["successful_queries"] += 1
            return {
                "success": True,
                "final_result": final_state["final_result"],
                "conversation_id": conversation_id,
                "agents_used": final_state["agents_completed"],
                "processing_time_ms": processing_time,
                "intermediate_results": final_state["intermediate_results"]
            }
        except Exception as e:
            self.stats["total_queries"] += 1
            self.stats["failed_queries"] += 1
            print(f"Orchestrator Error: {str(e)}")
            traceback.print_exc()
            return {
                "success": False,
                "error": str(e),
                "final_result": None
            }

    async def _analyze_query(self, state: AgentState) -> AgentState:
        initial_message = self.protocol.create_message(
            sender_id="orchestrator",
            sender_capability=AgentCapability.REASONING,
            subject="User Query Processing",
            payload={
                "query": state["user_query"],
                "context": state["context"],
                "task_type": "analysis"
            },
            message_type=MessageType.BROADCAST,
            priority=Priority.NORMAL,
            conversation_id=state["conversation_id"]
        )
        state.setdefault("a2a_messages", []).append(initial_message)
        state["current_step"] = "analyzed"
        return state

    async def _execute_agents(self, state: AgentState) -> AgentState:
        pending_agents = [
            agent_id for agent_id in state["agents_to_execute"]
            if agent_id not in state["agents_completed"]
        ]
        if not pending_agents:
            state["current_step"] = "all_agents_completed"
            return state
            
        agent_id = pending_agents[0]
        agent = self.agents.get(agent_id)
        if not agent:
            state["error"] = f"Agent {agent_id} not found"
            return state
            
        # Context building: Inject previous result
        # Since agents are executed sequentially (0 -> 1 -> 2), the "previous" is the one just completed.
        previous_result = ""
        context_data = state["context"].copy()
        
        if state["agents_completed"]:
            last_agent_id = state["agents_completed"][-1]
            if last_agent_id in state["intermediate_results"]:
                prev_res = state["intermediate_results"][last_agent_id]
                previous_result = f"Resultado del Agente Previo ({last_agent_id}):\n{prev_res}\n\nUsa esto como base para tu respuesta."
                context_data["previous_agent_output"] = prev_res

        task_content = state["user_query"]
        if previous_result:
            task_content = f"{previous_result}\n\nTarea Original: {state['user_query']}"

        agent_message = self.protocol.create_message(
                sender_id="orchestrator",
                sender_capability=AgentCapability.REASONING,
                subject=f"Task Execution Request for {agent_id}",
                payload={"task": task_content, "context": context_data},
                message_type=MessageType.REQUEST,
                recipient_id=agent_id,
                conversation_id=state["conversation_id"]
        )
        response = await agent.handle_message(agent_message)
        if response.success:
            result = response.result
            if isinstance(result, dict): result = str(result)
            state["intermediate_results"][agent_id] = result
            state["agents_completed"].append(agent_id)
        else:
            state["error"] = f"Agent {agent_id} failed: {response.error_message}"
        return state

    def _should_continue(self, state: AgentState) -> str:
        pending = [
            id for id in state["agents_to_execute"]
            if id not in state["agents_completed"]
        ]
        if pending and not state.get("error"):
            return "continue"
        return "synthesize"

    async def _synthesize_results(self, state: AgentState) -> AgentState:
        # Instead of joining into a string, we simply pass the list of structured responses
        # The API layer will need to handle this.
        # But wait, StateGraph expects state updates. 
        # We will create a special key "structured_conversation"
        
        conversation_sequence = []
        for agent_id, result in state["intermediate_results"].items():
            agent = self.agents.get(agent_id)
            name = agent.profile.name if agent else agent_id
            spec = agent.profile.specialization if agent else ""
            level = getattr(agent.profile, "level", 1)
            
            conversation_sequence.append({
                "agent_id": agent_id,
                "agent_name": name,
                "specialization": spec,
                "level": level,
                "content": result,
                "type": "response"
            })
            
        # We store the objects in final_result as well, but wrapped or as is?
        # If we change final_result to a list, we must ensure TypeDict allows it.
        # AgentState keys are strong typed? TypedDict in Python < 3.11 is just a suggestion usually, 
        # but better be safe.
        # Ideally we'd update AgentState to Optional[Union[str, List[Dict]]] but we can't easily change the TypedDict definition 
        # without rewriting the class.
        # Let's stringify it for safety in 'final_result' BUT use a new key if possible or just use a json string.
        # Wait, the user wants "SEPARADO DE CADA AGENTE".
        # Let's assume 'final_result' can be Any.
        
        state["final_result"] = conversation_sequence 
        return state

    async def _finalize_result(self, state: AgentState) -> AgentState:
        state["is_complete"] = True
        return state
