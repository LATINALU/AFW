"""
AFW v0.5.0 - Categoría: Marketing Digital
10 Agentes Especializados en Marketing y Publicidad
"""

from .seo_specialist import SEOSpecialistAgent
from .content_strategist import ContentStrategistAgent
from .social_media_manager import SocialMediaManagerAgent
from .email_marketer import EmailMarketerAgent
from .ppc_specialist import PPCSpecialistAgent
from .brand_strategist import BrandStrategistAgent
from .copywriter import CopywriterAgent
from .analytics_expert import AnalyticsExpertAgent
from .influencer_coordinator import InfluencerCoordinatorAgent
from .growth_hacker import GrowthHackerAgent

MARKETING_AGENTS = [
    SEOSpecialistAgent,
    ContentStrategistAgent,
    SocialMediaManagerAgent,
    EmailMarketerAgent,
    PPCSpecialistAgent,
    BrandStrategistAgent,
    CopywriterAgent,
    AnalyticsExpertAgent,
    InfluencerCoordinatorAgent,
    GrowthHackerAgent
]

__all__ = [
    "SEOSpecialistAgent",
    "ContentStrategistAgent",
    "SocialMediaManagerAgent",
    "EmailMarketerAgent",
    "PPCSpecialistAgent",
    "BrandStrategistAgent",
    "CopywriterAgent",
    "AnalyticsExpertAgent",
    "InfluencerCoordinatorAgent",
    "GrowthHackerAgent",
    "MARKETING_AGENTS"
]
