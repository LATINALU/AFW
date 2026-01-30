from abc import ABC, abstractmethod
from typing import List, Dict, Any, Optional

class OrchestratorPort(ABC):
    """
    Puerto para el orquestador de agentes.
    Define cómo se ejecutan las tareas compuestas por múltiples agentes.
    """
    
    @abstractmethod
    async def execute_task(
        self,
        task: str,
        agents: List[Any],
        context: Optional[Dict[str, Any]] = None
    ) -> Dict[str, Any]:
        """
        Ejecuta una tarea coordinando los agentes especificados.
        """
        pass
