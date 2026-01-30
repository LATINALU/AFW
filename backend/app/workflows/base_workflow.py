"""
AFW v0.5.0 - Base Workflow Classes
Clases base para el sistema de workflows pre-programados
"""

from typing import Dict, Any, List, Optional
from dataclasses import dataclass, field
from enum import Enum
from datetime import datetime
import uuid


class WorkflowComplexity(Enum):
    """Niveles de complejidad de workflows"""
    LOW = "low"
    MEDIUM = "medium"
    HIGH = "high"
    EXPERT = "expert"


class WorkflowStatus(Enum):
    """Estados de ejecución de workflows"""
    PENDING = "pending"
    RUNNING = "running"
    COMPLETED = "completed"
    FAILED = "failed"
    CANCELLED = "cancelled"


@dataclass
class WorkflowStep:
    """Representa un paso individual en un workflow"""
    step_id: str
    name: str
    description: str
    agent_id: str
    prompt_template: str
    order: int
    depends_on: List[str] = field(default_factory=list)
    optional: bool = False
    timeout_seconds: int = 300
    
    def get_prompt(self, context: Dict[str, Any]) -> str:
        """Genera el prompt con el contexto proporcionado"""
        prompt = self.prompt_template
        for key, value in context.items():
            prompt = prompt.replace(f"{{{key}}}", str(value))
        return prompt


@dataclass
class WorkflowTemplate:
    """Template de workflow pre-programado"""
    workflow_id: str
    name: str
    description: str
    category: str
    complexity: WorkflowComplexity
    estimated_time_minutes: int
    required_agents: List[str]
    steps: List[WorkflowStep]
    tags: List[str] = field(default_factory=list)
    inputs: List[str] = field(default_factory=list)
    outputs: List[str] = field(default_factory=list)
    
    def validate(self) -> tuple[bool, str]:
        """Valida que el workflow esté correctamente configurado"""
        if not self.steps:
            return False, "Workflow must have at least one step"
        
        if len(self.required_agents) > 10:
            return False, "Workflow cannot require more than 10 agents"
        
        step_ids = {step.step_id for step in self.steps}
        for step in self.steps:
            for dep in step.depends_on:
                if dep not in step_ids:
                    return False, f"Step {step.step_id} depends on non-existent step {dep}"
        
        return True, "Valid"
    
    def to_dict(self) -> Dict[str, Any]:
        """Convierte el workflow a diccionario"""
        return {
            "workflow_id": self.workflow_id,
            "name": self.name,
            "description": self.description,
            "category": self.category,
            "complexity": self.complexity.value,
            "estimated_time_minutes": self.estimated_time_minutes,
            "required_agents": self.required_agents,
            "steps_count": len(self.steps),
            "tags": self.tags,
            "inputs": self.inputs,
            "outputs": self.outputs
        }


@dataclass
class WorkflowExecution:
    """Representa una ejecución de workflow"""
    execution_id: str
    workflow_id: str
    user_id: str
    status: WorkflowStatus
    started_at: datetime
    completed_at: Optional[datetime] = None
    current_step: int = 0
    results: Dict[str, Any] = field(default_factory=dict)
    errors: List[str] = field(default_factory=list)
    
    @classmethod
    def create(cls, workflow_id: str, user_id: str) -> "WorkflowExecution":
        """Crea una nueva ejecución de workflow"""
        return cls(
            execution_id=str(uuid.uuid4()),
            workflow_id=workflow_id,
            user_id=user_id,
            status=WorkflowStatus.PENDING,
            started_at=datetime.now()
        )


class WorkflowExecutor:
    """Ejecutor de workflows"""
    
    def __init__(self, agent_registry=None):
        self.agent_registry = agent_registry
        self.executions: Dict[str, WorkflowExecution] = {}
    
    async def execute(
        self, 
        workflow: WorkflowTemplate, 
        user_id: str,
        context: Dict[str, Any]
    ) -> WorkflowExecution:
        """Ejecuta un workflow completo"""
        execution = WorkflowExecution.create(workflow.workflow_id, user_id)
        execution.status = WorkflowStatus.RUNNING
        self.executions[execution.execution_id] = execution
        
        try:
            sorted_steps = sorted(workflow.steps, key=lambda s: s.order)
            
            for step in sorted_steps:
                execution.current_step = step.order
                
                # Check dependencies
                for dep in step.depends_on:
                    if dep not in execution.results:
                        if not step.optional:
                            raise Exception(f"Dependency {dep} not completed")
                
                # Execute step
                prompt = step.get_prompt({**context, **execution.results})
                
                # Here we would call the agent
                # For now, we'll simulate the response
                result = {
                    "step_id": step.step_id,
                    "agent_id": step.agent_id,
                    "output": f"Output for step {step.name}",
                    "completed_at": datetime.now().isoformat()
                }
                
                execution.results[step.step_id] = result
            
            execution.status = WorkflowStatus.COMPLETED
            execution.completed_at = datetime.now()
            
        except Exception as e:
            execution.status = WorkflowStatus.FAILED
            execution.errors.append(str(e))
            execution.completed_at = datetime.now()
        
        return execution
    
    def get_execution(self, execution_id: str) -> Optional[WorkflowExecution]:
        """Obtiene una ejecución por ID"""
        return self.executions.get(execution_id)
    
    def cancel_execution(self, execution_id: str) -> bool:
        """Cancela una ejecución en progreso"""
        execution = self.executions.get(execution_id)
        if execution and execution.status == WorkflowStatus.RUNNING:
            execution.status = WorkflowStatus.CANCELLED
            execution.completed_at = datetime.now()
            return True
        return False
