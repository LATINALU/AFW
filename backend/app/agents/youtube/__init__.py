"""
AFW v0.5.0 - Categoría: YouTube
10 Agentes Especializados en Creación y Crecimiento en YouTube
"""

from .yt_content_strategist import YTContentStrategistAgent
from .yt_seo_specialist import YTSEOSpecialistAgent
from .yt_script_writer import YTScriptWriterAgent
from .yt_thumbnail_designer import YTThumbnailDesignerAgent
from .yt_analytics_expert import YTAnalyticsExpertAgent
from .yt_monetization_expert import YTMonetizationExpertAgent
from .yt_shorts_specialist import YTShortsSpecialistAgent
from .yt_community_manager import YTCommunityManagerAgent
from .yt_video_editor_advisor import YTVideoEditorAdvisorAgent
from .yt_growth_strategist import YTGrowthStrategistAgent

YOUTUBE_AGENTS = [
    YTContentStrategistAgent,
    YTSEOSpecialistAgent,
    YTScriptWriterAgent,
    YTThumbnailDesignerAgent,
    YTAnalyticsExpertAgent,
    YTMonetizationExpertAgent,
    YTShortsSpecialistAgent,
    YTCommunityManagerAgent,
    YTVideoEditorAdvisorAgent,
    YTGrowthStrategistAgent
]

__all__ = [
    "YTContentStrategistAgent",
    "YTSEOSpecialistAgent",
    "YTScriptWriterAgent",
    "YTThumbnailDesignerAgent",
    "YTAnalyticsExpertAgent",
    "YTMonetizationExpertAgent",
    "YTShortsSpecialistAgent",
    "YTCommunityManagerAgent",
    "YTVideoEditorAdvisorAgent",
    "YTGrowthStrategistAgent",
    "YOUTUBE_AGENTS"
]
