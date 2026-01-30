"""
LangGraph Orchestrator Adapter - ATP v0.8.1
Implementation of GraphWorkflowPort using LangGraph and A2A Protocol.
Enhanced with specialized response formats.
"""
from typing import Dict, Any, List, Optional, TypedDict
from langgraph.graph import StateGraph, END
from datetime import datetime
import uuid

from src.domain.ports.output.workflow_port import GraphWorkflowPort
from src.domain.entities.agent import Agent
from src.shared.a2a_protocol import (
    A2AMessage,
    A2AResponse,
    AgentCapability,
    AgentProfile,
    MessageType,
    Priority,
    a2a_protocol,
    AgentStatus,
)

# === SISTEMA DE FORMATOS ESPECIALIZADOS ===
try:
    from app.agents.enhanced_registry import (
        build_agent_prompt,
        get_specialized_system_prompt,
        ENHANCED_AGENT_DEFINITIONS
    )
    from app.agents.response_formats import CATEGORY_FORMAT_MAPPING
    SPECIALIZED_FORMATS_AVAILABLE = True
except ImportError:
    SPECIALIZED_FORMATS_AVAILABLE = False
    ENHANCED_AGENT_DEFINITIONS = {}
    CATEGORY_FORMAT_MAPPING = {}

class AgentState(TypedDict):
    """Estado compartido en el grafo de LangGraph"""
    user_query: str
    context: Dict[str, Any]
    a2a_messages: List[A2AMessage]
    a2a_responses: List[A2AResponse]
    current_step: str
    next_agent: Optional[str]
    agents_to_execute: List[str]
    agents_completed: List[str]
    intermediate_results: Dict[str, Any]
    final_result: Optional[str]
    conversation_id: str
    start_time: datetime
    is_complete: bool
    error: Optional[str]

class LangGraphOrchestratorAdapter(GraphWorkflowPort):
    def __init__(self):
        self.agents_map: Dict[str, Agent] = {}
        self.protocol = a2a_protocol
        self._register_orchestrator_agent()
        self.graph = None

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
            model="orchestrator",
            system_prompt="You are a LangGraph orchestrator agent responsible for coordinating workflows and routing messages between agents.",
            level=1
        )
        self.protocol.register_agent(orchestrator_profile)

    def _sort_agents(self, agents: List[Agent]) -> List[Agent]:
        # Limit to 5 agents as per previous business logic
        if len(agents) > 5:
            agents = agents[:5]
        # Sort by level
        return sorted(agents, key=lambda a: a.profile.level)

    async def run_workflow(
        self, 
        task: str, 
        agents: List[Agent], 
        context: Optional[Dict[str, Any]] = None
    ) -> Dict[str, Any]:
        
        sorted_agents = self._sort_agents(agents)
        self.agents_map = {a.profile.agent_id: a for a in sorted_agents}
        
        # Register in protocol
        for agent in sorted_agents:
            self.protocol.register_agent(agent.profile)

        # Build graph
        self.graph = self._build_graph()
        
        # Start state
        initial_state: AgentState = {
            "user_query": task,
            "context": context or {},
            "a2a_messages": [],
            "a2a_responses": [],
            "current_step": "init",
            "next_agent": None,
            "agents_to_execute": [a.profile.agent_id for a in sorted_agents],
            "agents_completed": [],
            "intermediate_results": {},
            "final_result": None,
            "conversation_id": str(uuid.uuid4()),
            "start_time": datetime.utcnow(),
            "is_complete": False,
            "error": None
        }

        final_state = await self.graph.ainvoke(initial_state)
        
        agent_responses = []
        for agent_id in final_state["agents_completed"]:
            agent = self.agents_map.get(agent_id)
            if agent:
                agent_responses.append({
                    "agent_id": agent_id,
                    "agent_name": agent.profile.name,
                    "content": final_state["intermediate_results"].get(agent_id, ""),
                    "status": "completed"
                })

        return {
            "final_result": final_state["final_result"],
            "agent_responses": agent_responses,
            "conversation_id": final_state["conversation_id"]
        }

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

    async def _analyze_query(self, state: AgentState) -> AgentState:
        initial_message = self.protocol.create_message(
            sender_id="orchestrator",
            sender_capability=AgentCapability.REASONING,
            subject="User Query Processing",
            payload={"query": state["user_query"], "context": state["context"]},
            message_type=MessageType.BROADCAST,
            conversation_id=state["conversation_id"]
        )
        state.setdefault("a2a_messages", []).append(initial_message)
        state["current_step"] = "analyzed"
        return state

    async def _execute_agents(self, state: AgentState) -> AgentState:
        pending = [aid for aid in state["agents_to_execute"] if aid not in state["agents_completed"]]
        if not pending:
            state["current_step"] = "all_agents_completed"
            return state
        
        agent_id = pending[0]
        agent = self.agents_map.get(agent_id)
        if not agent:
            state["error"] = f"Agent {agent_id} not found"
            return state

        # Sequential context from previous agents
        previous_context = ""
        if state["agents_completed"]:
            last_id = state["agents_completed"][-1]
            last_result = state["intermediate_results"].get(last_id, "")
            previous_context = f"\n\nContext from previous expert ({last_id}):\n{last_result}"

        try:
            # === USAR PROMPT ESPECIALIZADO SI ESTÁ DISPONIBLE ===
            enhanced_task = state["user_query"]
            
            if SPECIALIZED_FORMATS_AVAILABLE:
                agent_data = ENHANCED_AGENT_DEFINITIONS.get(agent_id, {})
                if agent_data:
                    try:
                        # Construir prompt especializado con formato definido
                        enhanced_task = build_agent_prompt(agent_id, agent_data, state["user_query"])
                        
                        # Agregar contexto previo si existe
                        if previous_context:
                            enhanced_task += f"\n\n---\n## CONTEXTO DE EXPERTOS ANTERIORES\n{previous_context}\n---\n"
                    except Exception as e:
                        print(f"⚠️ Error building specialized prompt: {e}")
                        enhanced_task = state["user_query"]
            
            # Create A2A message
            msg = self.protocol.create_message(
                sender_id="orchestrator",
                sender_capability=AgentCapability.REASONING,
                subject=f"Process task: {agent_id}",
                payload={"task": enhanced_task, "previous_context": previous_context},
                message_type=MessageType.REQUEST,
                recipient_id=agent_id,
                conversation_id=state["conversation_id"]
            )
            
            # Execute agent with enhanced task
            result = await agent.process_task(enhanced_task, {"previous_context": previous_context})
            
            # Store result with category metadata
            content = result.get("content", "")
            state["intermediate_results"][agent_id] = {
                "content": content,
                "category": agent_data.get("category", "analysis") if SPECIALIZED_FORMATS_AVAILABLE else "analysis",
                "format_type": CATEGORY_FORMAT_MAPPING.get(agent_data.get("category", "analysis"), "analysis") if SPECIALIZED_FORMATS_AVAILABLE else "analysis"
            }
            state["agents_completed"].append(agent_id)
            state["current_step"] = f"executed_{agent_id}"
        except Exception as e:
            state["error"] = str(e)
            
        return state

    def _should_continue(self, state: AgentState) -> str:
        pending = [aid for aid in state["agents_to_execute"] if aid not in state["agents_completed"]]
        if pending and not state.get("error"):
            return "continue"
        return "synthesize"

    async def _synthesize_results(self, state: AgentState) -> AgentState:
        results = ["# 🎯 Multi-Expert Analysis\n"]
        for agent_id in state["agents_completed"]:
            result_data = state["intermediate_results"].get(agent_id)
            agent = self.agents_map.get(agent_id)
            
            if agent and result_data:
                # Handle both old format (string) and new format (dict with metadata)
                if isinstance(result_data, dict):
                    content = result_data.get("content", "")
                    category = result_data.get("category", "analysis")
                    format_type = result_data.get("format_type", "analysis")
                else:
                    content = result_data
                    category = "analysis"
                    format_type = "analysis"
                
                # Build section with category indicator
                results.append(f"\n### {agent.profile.name} (Level {agent.profile.level}) | 📁 {category}\n")
                results.append(f"*{agent.profile.description}*\n\n")
                results.append(f"{content}\n")
        
        state["final_result"] = "".join(results)
        state["current_step"] = "synthesized"
        return state

    async def _finalize_result(self, state: AgentState) -> AgentState:
        state["is_complete"] = True
        state["current_step"] = "finalized"
        return state
