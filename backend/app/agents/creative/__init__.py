"""
AFW v0.5.0 - Categoría: Creatividad y Diseño
10 Agentes Especializados en Creatividad
"""

from .graphic_designer import GraphicDesignerAgent
from .ux_designer import UXDesignerAgent
from .ui_designer import UIDesignerAgent
from .video_producer import VideoProducerAgent
from .animator import AnimatorAgent
from .illustrator import IllustratorAgent
from .brand_designer import BrandDesignerAgent
from .motion_designer import MotionDesignerAgent
from .three_d_artist import ThreeDimensionalArtistAgent
from .creative_director import CreativeDirectorAgent

CREATIVE_AGENTS = [
    GraphicDesignerAgent, UXDesignerAgent, UIDesignerAgent,
    VideoProducerAgent, AnimatorAgent, IllustratorAgent,
    BrandDesignerAgent, MotionDesignerAgent, ThreeDimensionalArtistAgent,
    CreativeDirectorAgent
]

__all__ = [
    "GraphicDesignerAgent", "UXDesignerAgent", "UIDesignerAgent",
    "VideoProducerAgent", "AnimatorAgent", "IllustratorAgent",
    "BrandDesignerAgent", "MotionDesignerAgent", "ThreeDimensionalArtistAgent",
    "CreativeDirectorAgent", "CREATIVE_AGENTS"
]
