"""
AFW v0.5.0 - Agents For Works
Sistema de Categorías de Agentes Profesionales
120 Agentes Especializados en 12 Categorías
"""

from .software_development import *
from .marketing import *
from .finance import *
from .legal import *
from .human_resources import *
from .sales import *
from .operations import *
from .education import *
from .creative import *
from .project_management import *
from .mercadolibre import *
from .youtube import *

# Categorías disponibles
AGENT_CATEGORIES = [
    "software_development",
    "marketing", 
    "finance",
    "legal",
    "human_resources",
    "sales",
    "operations",
    "education",
    "creative",
    "project_management",
    "mercadolibre",
    "youtube"
]

# Mapeo de categorías a nombres legibles
CATEGORY_NAMES = {
    "software_development": "Desarrollo de Software",
    "marketing": "Marketing Digital",
    "finance": "Finanzas y Contabilidad",
    "legal": "Legal y Compliance",
    "human_resources": "Recursos Humanos",
    "sales": "Ventas y Comercial",
    "operations": "Operaciones y Logística",
    "education": "Educación y Capacitación",
    "creative": "Creatividad y Diseño",
    "project_management": "Gestión de Proyectos",
    "mercadolibre": "Mercado Libre",
    "youtube": "YouTube"
}
