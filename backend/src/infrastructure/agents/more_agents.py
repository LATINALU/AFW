from .base_agent import BaseAgent
from ...domain.entities.a2a_types import AgentCapability

class SynthesisAgent(BaseAgent):
    def __init__(self, model: str = None, api_config: dict = None):
        super().__init__(
            agent_id="synthesis",
            name="Synthesis Agent",
            primary_capability=AgentCapability.SYNTHESIS,
            specialization="Integration of information",
            description="Combina múltiples fuentes de información en una respuesta coherente.",
            model_name=model or "groq-llama",
            level=5
        )

    def get_system_prompt(self) -> str:
        return "Eres Síntesis (Nivel 5). Tu objetivo es integrar los hallazgos previos en una respuesta final coherente, profesional y clara. No repitas el proceso, da la solución."

class AnalysisAgent(BaseAgent):
    def __init__(self, model: str = None, api_config: dict = None):
        super().__init__(
            agent_id="analysis",
            name="Analysis Agent",
            primary_capability=AgentCapability.ANALYSIS,
            specialization="Problem decomposition",
            description="Descompone problemas complejos en partes manejables.",
            model_name=model or "groq-llama",
            level=1
        )

    def get_system_prompt(self) -> str:
        return "Eres un Agente de Análisis. Descompone el problema en componentes fundamentales."
