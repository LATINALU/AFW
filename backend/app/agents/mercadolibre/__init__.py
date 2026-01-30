"""
AFW v0.5.0 - Categoría: Mercado Libre
10 Agentes Especializados en el Marketplace #1 de Latinoamérica
"""

from .mercadolibre_product_specialist import MercadoLibreProductSpecialistAgent
from .mercadolibre_sales_optimizer import MercadoLibreSalesOptimizerAgent
from .ml_listing_optimizer import MLListingOptimizerAgent
from .ml_ads_specialist import MLAdsSpecialistAgent
from .ml_reputation_manager import MLReputationManagerAgent
from .ml_pricing_strategist import MLPricingStrategistAgent
from .ml_customer_service import MLCustomerServiceAgent
from .ml_logistics_expert import MLLogisticsExpertAgent
from .ml_catalog_manager import MLCatalogManagerAgent
from .ml_analytics_expert import MLAnalyticsExpertAgent

MERCADOLIBRE_AGENTS = [
    MercadoLibreProductSpecialistAgent,
    MercadoLibreSalesOptimizerAgent,
    MLListingOptimizerAgent,
    MLAdsSpecialistAgent,
    MLReputationManagerAgent,
    MLPricingStrategistAgent,
    MLCustomerServiceAgent,
    MLLogisticsExpertAgent,
    MLCatalogManagerAgent,
    MLAnalyticsExpertAgent
]

__all__ = [
    "MercadoLibreProductSpecialistAgent",
    "MercadoLibreSalesOptimizerAgent",
    "MLListingOptimizerAgent",
    "MLAdsSpecialistAgent",
    "MLReputationManagerAgent",
    "MLPricingStrategistAgent",
    "MLCustomerServiceAgent",
    "MLLogisticsExpertAgent",
    "MLCatalogManagerAgent",
    "MLAnalyticsExpertAgent",
    "MERCADOLIBRE_AGENTS"
]
