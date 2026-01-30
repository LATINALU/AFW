from typing import List, Dict, Any, Optional, TypedDict
from langgraph.graph import StateGraph, END
from src.domain.ports.output.workflow_port import GraphWorkflowPort
from src.domain.entities.agent import Agent
from datetime import datetime

class AgentState(TypedDict):
    task: str
    context: Dict[str, Any]
    agents: List[Agent]
    agents_to_run: List[str]
    completed_agents: List[str]
    results: Dict[str, Any]
    final_result: Optional[str]

class LangGraphWorkflowAdapter(GraphWorkflowPort):
    def __init__(self):
        # No guardamos el grafo compilado porque depende de los agentes específicos de cada tarea
        pass

    async def run_workflow(
        self, 
        task: str, 
        agents: List[Agent], 
        context: Optional[Dict[str, Any]] = None
    ) -> Dict[str, Any]:
        
        # 1. Ordenar agentes por nivel (si es necesario)
        # Por ahora asumimos que vienen en el orden deseado o los ordenamos aquí
        agents_map = {a.profile.agent_id: a for a in agents}
        
        # 2. Definir el grafo
        workflow = StateGraph(AgentState)
        
        workflow.add_node("execute_node", self._execute_node)
        workflow.add_node("finalize", self._finalize)
        
        workflow.set_entry_point("execute_node")
        
        workflow.add_conditional_edges(
            "execute_node",
            self._should_continue,
            {
                "continue": "execute_node",
                "end": "finalize"
            }
        )
        
        workflow.add_edge("finalize", END)
        
        app = workflow.compile()
        
        # 3. Estado inicial
        initial_state: AgentState = {
            "task": task,
            "context": context or {},
            "agents": agents,
            "agents_to_run": [a.profile.agent_id for a in agents],
            "completed_agents": [],
            "results": {},
            "final_result": None
        }
        
        # 4. Ejecutar
        final_state = await app.ainvoke(initial_state)
        
        return {
            "final_result": final_state["final_result"],
            "agent_responses": [
                {
                    "agent_id": aid,
                    "agent_name": agents_map[aid].profile.name,
                    "content": final_state["results"][aid],
                    "status": "completed"
                } for aid in final_state["completed_agents"]
            ]
        }

    async def _execute_node(self, state: AgentState) -> AgentState:
        # Obtener siguiente agente
        agent_id = state["agents_to_run"][0]
        agents_dict = {a.profile.agent_id: a for a in state["agents"]}
        agent = agents_dict[agent_id]
        
        # Construir contexto enriquecido (resultados previos)
        current_context = state["context"].copy()
        current_context["previous_results"] = state["results"]
        
        # Ejecutar agente
        result = await agent.process_task(state["task"], current_context)
        
        # Actualizar estado
        state["results"][agent_id] = result["content"]
        state["completed_agents"].append(agent_id)
        state["agents_to_run"].pop(0)
        
        return state

    def _should_continue(self, state: AgentState) -> str:
        if state["agents_to_run"]:
            return "continue"
        return "end"

    async def _finalize(self, state: AgentState) -> AgentState:
        # Síntesis básica
        summary = "### Resumen de Ejecución\n\n"
        for aid in state["completed_agents"]:
            summary += f"**{aid}**: {state['results'][aid][:200]}...\n\n"
        
        state["final_result"] = summary
        return state
