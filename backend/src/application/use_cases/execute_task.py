from typing import List
from src.domain.ports.input.agent_use_cases import ExecuteTaskUseCasePort, ExecuteTaskInputDTO, AgentResultDTO
from src.domain.ports.output.agent_repository import AgentRepositoryPort
from src.domain.ports.output.llm_provider import LLMProviderPort, LLMProviderFactoryPort
from src.domain.ports.output.workflow_port import GraphWorkflowPort
from src.domain.entities.agent import Agent

class ExecuteTaskUseCase(ExecuteTaskUseCasePort):
    def __init__(
        self, 
        agent_repo: AgentRepositoryPort, 
        default_llm_provider: LLMProviderPort,
        workflow_orchestrator: GraphWorkflowPort,
        llm_factory: LLMProviderFactoryPort
    ):
        self.agent_repo = agent_repo
        self.default_llm_provider = default_llm_provider
        self.workflow_orchestrator = workflow_orchestrator
        self.llm_factory = llm_factory

    async def execute(self, input: ExecuteTaskInputDTO) -> List[AgentResultDTO]:
        # Determinar qué proveedor usar
        llm_provider = self.default_llm_provider
        if input.api_config and (input.api_config.get("api_key") or input.api_config.get("apiKey")):
            llm_provider = self.llm_factory.create(input.api_config)

        # Preparar instancias de agentes (entidades de dominio)
        agents = []
        for agent_id in input.selected_agents:
            profile = self.agent_repo.get_by_id(agent_id)
            if profile:
                agents.append(Agent(profile, llm_provider))
        
        if not agents:
            return []

        # Ejecutar via Orquestador de Grafos (LangGraph)
        workflow_result = await self.workflow_orchestrator.run_workflow(
            task=input.task,
            agents=agents,
            context=input.context
        )
        
        # Mapear a DTOs de salida
        return [
            AgentResultDTO(
                agent_id=r["agent_id"] if isinstance(r, dict) else getattr(r, "agent_id", ""),
                agent_name=r["agent_name"] if isinstance(r, dict) else getattr(r, "agent_name", ""),
                content=r["content"] if isinstance(r, dict) else getattr(r, "content", ""),
                status=r["status"] if isinstance(r, dict) else getattr(r, "status", "completed")
            ) for r in workflow_result.get("agent_responses", [])
        ]
