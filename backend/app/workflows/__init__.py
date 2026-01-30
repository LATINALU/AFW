"""
AFW v0.5.0 - Workflows System
Sistema de 50 tareas pre-programadas para productividad profesional
"""

from .base_workflow import WorkflowTemplate, WorkflowStep, WorkflowExecutor
from .workflow_registry import workflow_registry, get_workflow, get_workflows_by_category

__all__ = [
    "WorkflowTemplate",
    "WorkflowStep", 
    "WorkflowExecutor",
    "workflow_registry",
    "get_workflow",
    "get_workflows_by_category"
]
