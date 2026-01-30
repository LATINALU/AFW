from .base_agent import BaseAgent
from ...domain.entities.a2a_types import AgentCapability

class ReasoningAgent(BaseAgent):
    """
    Agente de Razonamiento Lógico.
    """
    def __init__(self, model: str = None, api_config: dict = None):
        super().__init__(
            agent_id="reasoning",
            name="Reasoning Agent",
            primary_capability=AgentCapability.REASONING,
            specialization="Logic and deduction",
            description="Agente especializado en razonamiento lógico paso a paso.",
            model_name=model or "groq-llama",
            level=1
        )
        if api_config:
            # Configure adapter if needed
            pass

    def get_system_prompt(self) -> str:
        return "Eres Razonamiento (Nivel 1). Analiza el problema con lógica deductiva: Premisas -> Inferencias -> Conclusiones. Sé breve y directo."
