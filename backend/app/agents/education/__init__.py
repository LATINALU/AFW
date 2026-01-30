"""
AFW v0.5.0 - Categoría: Educación y Capacitación
10 Agentes Especializados en Educación
"""

from .instructional_designer import InstructionalDesignerAgent
from .curriculum_developer import CurriculumDeveloperAgent
from .elearning_specialist import ElearningSpecialistAgent
from .training_facilitator import TrainingFacilitatorAgent
from .educational_technologist import EducationalTechnologistAgent
from .assessment_specialist import AssessmentSpecialistAgent
from .academic_advisor import AcademicAdvisorAgent
from .learning_analyst import LearningAnalystAgent
from .content_curator import ContentCuratorAgent
from .tutor_specialist import TutorSpecialistAgent

EDUCATION_AGENTS = [
    InstructionalDesignerAgent, CurriculumDeveloperAgent, ElearningSpecialistAgent,
    TrainingFacilitatorAgent, EducationalTechnologistAgent, AssessmentSpecialistAgent,
    AcademicAdvisorAgent, LearningAnalystAgent, ContentCuratorAgent, TutorSpecialistAgent
]

__all__ = [
    "InstructionalDesignerAgent", "CurriculumDeveloperAgent", "ElearningSpecialistAgent",
    "TrainingFacilitatorAgent", "EducationalTechnologistAgent", "AssessmentSpecialistAgent",
    "AcademicAdvisorAgent", "LearningAnalystAgent", "ContentCuratorAgent",
    "TutorSpecialistAgent", "EDUCATION_AGENTS"
]
