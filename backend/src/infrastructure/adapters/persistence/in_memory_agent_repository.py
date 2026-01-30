from typing import List, Optional, Dict
from src.domain.entities.agent import AgentProfile
from src.domain.ports.output.agent_repository import AgentRepositoryPort

class InMemoryAgentRepository(AgentRepositoryPort):
    def __init__(self):
        # En una versión real, esto podría venir de un JSON o base de datos
        self._agents = {
            "reasoning": AgentProfile(
                agent_id="reasoning",
                name="Reasoning Agent",
                description="Razonamiento lógico multi-paradigma",
                level=1,
                specialization="Logical Analysis",
                backstory="Expert in structured reasoning...",
                model="gpt-4",
                system_prompt="You are a reasoning expert...",
                capabilities=["reasoning", "logic"]
            ),
            # ... Aquí se incluirían los 30 agentes
        }
        
        # Helper para poblar rápidamente (basado en las definiciones previas)
        from app.agents.registry import AGENT_DEFINITIONS
        for agent_id, agent_info in AGENT_DEFINITIONS.items():
            if agent_id not in self._agents:
                self._agents[agent_id] = AgentProfile(
                    agent_id=agent_id,
                    name=agent_info["name"],
                    description=agent_info["description"],
                    level=1,  # Default level for all agents
                    specialization=agent_info["specialization"],
                    backstory=f"I am the {agent_info['name']}. expert in {agent_info['description']}",
                    model="gpt-4o-mini",
                    system_prompt=f"You are the {agent_info['name']}. Mission: {agent_info['description']}",
                    capabilities=agent_info["capabilities"]
                )

    def get_by_id(self, agent_id: str) -> Optional[AgentProfile]:
        return self._agents.get(agent_id)

    def get_all(self) -> List[AgentProfile]:
        return list(self._agents.values())
