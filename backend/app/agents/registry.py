"""
AFW v0.5.0 - Agent Registry
Sistema centralizado de registro de 120 agentes en 12 categorías
"""

from typing import Dict, Any, List, Optional
from dataclasses import dataclass

@dataclass
class AgentDefinition:
    """Definición de un agente"""
    id: str
    name: str
    category: str
    description: str
    emoji: str
    capabilities: List[str]
    specialization: str
    complexity: str  # basic, intermediate, advanced, expert

# Definiciones de los 120 agentes organizados por categoría
AGENT_DEFINITIONS: Dict[str, Dict[str, Any]] = {}

# ============================================================================
# CATEGORÍA: SOFTWARE DEVELOPMENT (10 agentes)
# ============================================================================
SOFTWARE_DEVELOPMENT_DEFINITIONS = {
    "fullstack_developer": {
        "name": "Fullstack Developer",
        "category": "software_development",
        "description": "Desarrollador full-stack experto en frontend y backend",
        "emoji": "💻",
        "capabilities": ["frontend", "backend", "databases", "apis", "deployment"],
        "specialization": "Desarrollo Full-Stack",
        "complexity": "advanced"
    },
    "backend_architect": {
        "name": "Backend Architect",
        "category": "software_development",
        "description": "Arquitecto de sistemas backend escalables y microservicios",
        "emoji": "🏗️",
        "capabilities": ["system_design", "microservices", "scalability", "cloud_native"],
        "specialization": "Arquitectura Backend",
        "complexity": "expert"
    },
    "frontend_specialist": {
        "name": "Frontend Specialist",
        "category": "software_development",
        "description": "Especialista en interfaces modernas con React, Vue, Angular",
        "emoji": "🎨",
        "capabilities": ["react", "vue", "angular", "css", "ux_implementation"],
        "specialization": "Frontend Moderno",
        "complexity": "advanced"
    },
    "devops_engineer": {
        "name": "DevOps Engineer",
        "category": "software_development",
        "description": "Ingeniero DevOps experto en CI/CD, containers y cloud",
        "emoji": "⚙️",
        "capabilities": ["ci_cd", "docker", "kubernetes", "aws", "terraform"],
        "specialization": "DevOps y Cloud",
        "complexity": "expert"
    },
    "database_expert": {
        "name": "Database Expert",
        "category": "software_development",
        "description": "Experto en bases de datos SQL y NoSQL, optimización",
        "emoji": "🗄️",
        "capabilities": ["sql", "nosql", "optimization", "migrations", "modeling"],
        "specialization": "Bases de Datos",
        "complexity": "advanced"
    },
    "security_specialist": {
        "name": "Security Specialist",
        "category": "software_development",
        "description": "Especialista en seguridad informática y ethical hacking",
        "emoji": "🔐",
        "capabilities": ["penetration_testing", "security_audit", "cryptography", "compliance"],
        "specialization": "Seguridad Informática",
        "complexity": "expert"
    },
    "mobile_developer": {
        "name": "Mobile Developer",
        "category": "software_development",
        "description": "Desarrollador móvil iOS, Android y cross-platform",
        "emoji": "📱",
        "capabilities": ["ios", "android", "react_native", "flutter", "mobile_ux"],
        "specialization": "Desarrollo Móvil",
        "complexity": "advanced"
    },
    "qa_automation": {
        "name": "QA Automation",
        "category": "software_development",
        "description": "Ingeniero de QA y automatización de pruebas",
        "emoji": "🧪",
        "capabilities": ["test_automation", "selenium", "cypress", "performance_testing"],
        "specialization": "QA y Testing",
        "complexity": "advanced"
    },
    "code_reviewer": {
        "name": "Code Reviewer",
        "category": "software_development",
        "description": "Revisor de código senior con enfoque en calidad y mejores prácticas",
        "emoji": "🔍",
        "capabilities": ["code_review", "best_practices", "refactoring", "mentoring"],
        "specialization": "Revisión de Código",
        "complexity": "advanced"
    },
    "tech_lead": {
        "name": "Tech Lead",
        "category": "software_development",
        "description": "Líder técnico con experiencia en gestión de equipos",
        "emoji": "👨‍💼",
        "capabilities": ["team_leadership", "architecture", "mentoring", "project_management"],
        "specialization": "Liderazgo Técnico",
        "complexity": "expert"
    },
}

# ============================================================================
# CATEGORÍA: MARKETING (10 agentes)
# ============================================================================
MARKETING_DEFINITIONS = {
    "seo_specialist": {
        "name": "SEO Specialist",
        "category": "marketing",
        "description": "Especialista en posicionamiento web y SEO técnico",
        "emoji": "🔍",
        "capabilities": ["seo_technical", "keyword_research", "link_building", "analytics"],
        "specialization": "SEO y Posicionamiento",
        "complexity": "advanced"
    },
    "content_strategist": {
        "name": "Content Strategist",
        "category": "marketing",
        "description": "Estratega de contenidos y marketing de contenidos",
        "emoji": "📝",
        "capabilities": ["content_planning", "editorial_calendar", "brand_voice", "storytelling"],
        "specialization": "Estrategia de Contenidos",
        "complexity": "advanced"
    },
    "social_media_manager": {
        "name": "Social Media Manager",
        "category": "marketing",
        "description": "Gestor de redes sociales y community management",
        "emoji": "📱",
        "capabilities": ["social_strategy", "community_management", "paid_social", "analytics"],
        "specialization": "Redes Sociales",
        "complexity": "intermediate"
    },
    "email_marketer": {
        "name": "Email Marketer",
        "category": "marketing",
        "description": "Especialista en email marketing y automatización",
        "emoji": "📧",
        "capabilities": ["email_campaigns", "automation", "segmentation", "deliverability"],
        "specialization": "Email Marketing",
        "complexity": "intermediate"
    },
    "ppc_specialist": {
        "name": "PPC Specialist",
        "category": "marketing",
        "description": "Especialista en publicidad pagada Google/Meta Ads",
        "emoji": "💰",
        "capabilities": ["google_ads", "meta_ads", "campaign_optimization", "bid_management"],
        "specialization": "Publicidad Pagada",
        "complexity": "advanced"
    },
    "brand_strategist": {
        "name": "Brand Strategist",
        "category": "marketing",
        "description": "Estratega de marca y posicionamiento",
        "emoji": "🎯",
        "capabilities": ["brand_positioning", "brand_identity", "messaging", "research"],
        "specialization": "Estrategia de Marca",
        "complexity": "advanced"
    },
    "copywriter": {
        "name": "Copywriter",
        "category": "marketing",
        "description": "Redactor publicitario y creativo",
        "emoji": "✍️",
        "capabilities": ["copywriting", "persuasion", "headlines", "creative_writing"],
        "specialization": "Copywriting",
        "complexity": "intermediate"
    },
    "analytics_expert": {
        "name": "Analytics Expert",
        "category": "marketing",
        "description": "Experto en análisis de datos de marketing",
        "emoji": "📊",
        "capabilities": ["google_analytics", "data_analysis", "reporting", "attribution"],
        "specialization": "Analytics de Marketing",
        "complexity": "advanced"
    },
    "influencer_coordinator": {
        "name": "Influencer Coordinator",
        "category": "marketing",
        "description": "Coordinador de campañas con influencers",
        "emoji": "🌟",
        "capabilities": ["influencer_outreach", "campaign_management", "contract_negotiation"],
        "specialization": "Marketing de Influencers",
        "complexity": "intermediate"
    },
    "growth_hacker": {
        "name": "Growth Hacker",
        "category": "marketing",
        "description": "Especialista en crecimiento acelerado y growth hacking",
        "emoji": "🚀",
        "capabilities": ["growth_experiments", "viral_loops", "acquisition", "retention"],
        "specialization": "Growth Hacking",
        "complexity": "advanced"
    },
}

# ============================================================================
# CATEGORÍA: FINANCE (10 agentes)
# ============================================================================
FINANCE_DEFINITIONS = {
    "financial_analyst": {
        "name": "Financial Analyst",
        "category": "finance",
        "description": "Analista financiero experto en valoración y proyecciones",
        "emoji": "📈",
        "capabilities": ["financial_modeling", "valuation", "forecasting", "analysis"],
        "specialization": "Análisis Financiero",
        "complexity": "advanced"
    },
    "accountant": {
        "name": "Accountant",
        "category": "finance",
        "description": "Contador experto en contabilidad y normativas",
        "emoji": "🧮",
        "capabilities": ["bookkeeping", "financial_statements", "compliance", "audit"],
        "specialization": "Contabilidad",
        "complexity": "intermediate"
    },
    "tax_specialist": {
        "name": "Tax Specialist",
        "category": "finance",
        "description": "Especialista en impuestos y planificación fiscal",
        "emoji": "💼",
        "capabilities": ["tax_planning", "compliance", "optimization", "international_tax"],
        "specialization": "Fiscalidad",
        "complexity": "advanced"
    },
    "investment_advisor": {
        "name": "Investment Advisor",
        "category": "finance",
        "description": "Asesor de inversiones y gestión de portafolios",
        "emoji": "💹",
        "capabilities": ["portfolio_management", "asset_allocation", "risk_assessment"],
        "specialization": "Inversiones",
        "complexity": "advanced"
    },
    "financial_controller": {
        "name": "Financial Controller",
        "category": "finance",
        "description": "Controller financiero y gestión presupuestaria",
        "emoji": "📋",
        "capabilities": ["budgeting", "cost_control", "reporting", "variance_analysis"],
        "specialization": "Control Financiero",
        "complexity": "advanced"
    },
    "risk_analyst": {
        "name": "Risk Analyst",
        "category": "finance",
        "description": "Analista de riesgos financieros",
        "emoji": "⚠️",
        "capabilities": ["risk_modeling", "stress_testing", "compliance", "mitigation"],
        "specialization": "Análisis de Riesgos",
        "complexity": "advanced"
    },
    "treasury_manager": {
        "name": "Treasury Manager",
        "category": "finance",
        "description": "Gestor de tesorería y liquidez",
        "emoji": "🏦",
        "capabilities": ["cash_management", "liquidity", "banking_relations", "fx_management"],
        "specialization": "Tesorería",
        "complexity": "advanced"
    },
    "budget_planner": {
        "name": "Budget Planner",
        "category": "finance",
        "description": "Planificador de presupuestos empresariales",
        "emoji": "📊",
        "capabilities": ["budget_creation", "forecasting", "cost_analysis", "reporting"],
        "specialization": "Planificación Presupuestaria",
        "complexity": "intermediate"
    },
    "auditor": {
        "name": "Auditor",
        "category": "finance",
        "description": "Auditor interno y externo",
        "emoji": "🔎",
        "capabilities": ["internal_audit", "compliance_audit", "risk_assessment", "controls"],
        "specialization": "Auditoría",
        "complexity": "advanced"
    },
    "payroll_specialist": {
        "name": "Payroll Specialist",
        "category": "finance",
        "description": "Especialista en nóminas y compensaciones",
        "emoji": "💵",
        "capabilities": ["payroll_processing", "benefits", "compliance", "reporting"],
        "specialization": "Nóminas",
        "complexity": "intermediate"
    },
}

# ============================================================================
# CATEGORÍA: LEGAL (10 agentes)
# ============================================================================
LEGAL_DEFINITIONS = {
    "corporate_lawyer": {
        "name": "Corporate Lawyer",
        "category": "legal",
        "description": "Abogado corporativo especializado en derecho empresarial",
        "emoji": "⚖️",
        "capabilities": ["corporate_law", "m&a", "governance", "contracts"],
        "specialization": "Derecho Corporativo",
        "complexity": "expert"
    },
    "contract_specialist": {
        "name": "Contract Specialist",
        "category": "legal",
        "description": "Especialista en redacción y revisión de contratos",
        "emoji": "📄",
        "capabilities": ["contract_drafting", "negotiation", "review", "compliance"],
        "specialization": "Contratos",
        "complexity": "advanced"
    },
    "compliance_officer": {
        "name": "Compliance Officer",
        "category": "legal",
        "description": "Oficial de cumplimiento normativo",
        "emoji": "✅",
        "capabilities": ["regulatory_compliance", "policy_development", "risk_management"],
        "specialization": "Compliance",
        "complexity": "advanced"
    },
    "intellectual_property": {
        "name": "IP Specialist",
        "category": "legal",
        "description": "Especialista en propiedad intelectual",
        "emoji": "💡",
        "capabilities": ["patents", "trademarks", "copyrights", "licensing"],
        "specialization": "Propiedad Intelectual",
        "complexity": "advanced"
    },
    "data_privacy_officer": {
        "name": "Data Privacy Officer",
        "category": "legal",
        "description": "Oficial de protección de datos y privacidad",
        "emoji": "🔒",
        "capabilities": ["gdpr", "data_protection", "privacy_policies", "compliance"],
        "specialization": "Privacidad de Datos",
        "complexity": "advanced"
    },
    "labor_law_expert": {
        "name": "Labor Law Expert",
        "category": "legal",
        "description": "Experto en derecho laboral",
        "emoji": "👷",
        "capabilities": ["employment_law", "labor_relations", "disputes", "compliance"],
        "specialization": "Derecho Laboral",
        "complexity": "advanced"
    },
    "regulatory_advisor": {
        "name": "Regulatory Advisor",
        "category": "legal",
        "description": "Asesor en regulaciones sectoriales",
        "emoji": "📋",
        "capabilities": ["regulatory_analysis", "licensing", "compliance", "advocacy"],
        "specialization": "Regulaciones",
        "complexity": "advanced"
    },
    "litigation_specialist": {
        "name": "Litigation Specialist",
        "category": "legal",
        "description": "Especialista en litigios y resolución de conflictos",
        "emoji": "🏛️",
        "capabilities": ["litigation", "arbitration", "mediation", "dispute_resolution"],
        "specialization": "Litigios",
        "complexity": "expert"
    },
    "legal_researcher": {
        "name": "Legal Researcher",
        "category": "legal",
        "description": "Investigador legal y análisis jurisprudencial",
        "emoji": "🔍",
        "capabilities": ["legal_research", "case_analysis", "precedents", "documentation"],
        "specialization": "Investigación Legal",
        "complexity": "intermediate"
    },
    "paralegal_assistant": {
        "name": "Paralegal Assistant",
        "category": "legal",
        "description": "Asistente legal para preparación de documentos",
        "emoji": "📑",
        "capabilities": ["document_preparation", "filing", "research", "organization"],
        "specialization": "Asistencia Legal",
        "complexity": "intermediate"
    },
}

# ============================================================================
# CATEGORÍA: HUMAN RESOURCES (10 agentes)
# ============================================================================
HUMAN_RESOURCES_DEFINITIONS = {
    "recruiter": {
        "name": "Recruiter",
        "category": "human_resources",
        "description": "Reclutador experto en atracción de talento",
        "emoji": "🎯",
        "capabilities": ["sourcing", "interviewing", "assessment", "employer_branding"],
        "specialization": "Reclutamiento",
        "complexity": "intermediate"
    },
    "talent_development": {
        "name": "Talent Development",
        "category": "human_resources",
        "description": "Especialista en desarrollo de talento",
        "emoji": "📈",
        "capabilities": ["training", "career_development", "succession_planning", "coaching"],
        "specialization": "Desarrollo de Talento",
        "complexity": "advanced"
    },
    "compensation_analyst": {
        "name": "Compensation Analyst",
        "category": "human_resources",
        "description": "Analista de compensaciones y beneficios",
        "emoji": "💰",
        "capabilities": ["salary_benchmarking", "benefits_design", "equity", "analysis"],
        "specialization": "Compensaciones",
        "complexity": "advanced"
    },
    "employee_relations": {
        "name": "Employee Relations",
        "category": "human_resources",
        "description": "Especialista en relaciones laborales",
        "emoji": "🤝",
        "capabilities": ["conflict_resolution", "policy_compliance", "investigations"],
        "specialization": "Relaciones Laborales",
        "complexity": "advanced"
    },
    "hr_analytics": {
        "name": "HR Analytics",
        "category": "human_resources",
        "description": "Analista de datos de recursos humanos",
        "emoji": "📊",
        "capabilities": ["people_analytics", "reporting", "metrics", "workforce_planning"],
        "specialization": "Analytics de RRHH",
        "complexity": "advanced"
    },
    "onboarding_specialist": {
        "name": "Onboarding Specialist",
        "category": "human_resources",
        "description": "Especialista en integración de empleados",
        "emoji": "🚀",
        "capabilities": ["onboarding_programs", "orientation", "integration", "retention"],
        "specialization": "Onboarding",
        "complexity": "intermediate"
    },
    "performance_manager": {
        "name": "Performance Manager",
        "category": "human_resources",
        "description": "Gestor de desempeño y evaluaciones",
        "emoji": "🎯",
        "capabilities": ["performance_reviews", "goal_setting", "feedback", "improvement_plans"],
        "specialization": "Gestión del Desempeño",
        "complexity": "advanced"
    },
    "culture_champion": {
        "name": "Culture Champion",
        "category": "human_resources",
        "description": "Promotor de cultura organizacional",
        "emoji": "🌟",
        "capabilities": ["culture_initiatives", "engagement", "values", "change_management"],
        "specialization": "Cultura Organizacional",
        "complexity": "intermediate"
    },
    "training_coordinator": {
        "name": "Training Coordinator",
        "category": "human_resources",
        "description": "Coordinador de programas de capacitación",
        "emoji": "📚",
        "capabilities": ["training_programs", "lms", "needs_assessment", "evaluation"],
        "specialization": "Capacitación",
        "complexity": "intermediate"
    },
    "benefits_administrator": {
        "name": "Benefits Administrator",
        "category": "human_resources",
        "description": "Administrador de beneficios y prestaciones",
        "emoji": "🏥",
        "capabilities": ["benefits_management", "enrollment", "vendor_relations", "compliance"],
        "specialization": "Administración de Beneficios",
        "complexity": "intermediate"
    },
}

# ============================================================================
# CATEGORÍA: SALES (10 agentes)
# ============================================================================
SALES_DEFINITIONS = {
    "sales_executive": {
        "name": "Sales Executive",
        "category": "sales",
        "description": "Ejecutivo de ventas B2B/B2C",
        "emoji": "💼",
        "capabilities": ["prospecting", "negotiation", "closing", "relationship_building"],
        "specialization": "Ventas",
        "complexity": "intermediate"
    },
    "account_manager": {
        "name": "Account Manager",
        "category": "sales",
        "description": "Gestor de cuentas y relaciones con clientes",
        "emoji": "🤝",
        "capabilities": ["account_management", "upselling", "retention", "client_success"],
        "specialization": "Gestión de Cuentas",
        "complexity": "advanced"
    },
    "business_development": {
        "name": "Business Development",
        "category": "sales",
        "description": "Desarrollo de negocios y partnerships",
        "emoji": "🚀",
        "capabilities": ["lead_generation", "partnerships", "market_expansion", "strategy"],
        "specialization": "Desarrollo de Negocios",
        "complexity": "advanced"
    },
    "sales_analyst": {
        "name": "Sales Analyst",
        "category": "sales",
        "description": "Analista de ventas y forecasting",
        "emoji": "📊",
        "capabilities": ["sales_analytics", "forecasting", "reporting", "pipeline_analysis"],
        "specialization": "Análisis de Ventas",
        "complexity": "intermediate"
    },
    "customer_success": {
        "name": "Customer Success",
        "category": "sales",
        "description": "Especialista en éxito del cliente",
        "emoji": "🌟",
        "capabilities": ["onboarding", "adoption", "retention", "customer_health"],
        "specialization": "Éxito del Cliente",
        "complexity": "intermediate"
    },
    "sales_trainer": {
        "name": "Sales Trainer",
        "category": "sales",
        "description": "Capacitador de equipos de ventas",
        "emoji": "📚",
        "capabilities": ["sales_training", "coaching", "methodology", "skill_development"],
        "specialization": "Capacitación en Ventas",
        "complexity": "advanced"
    },
    "proposal_writer": {
        "name": "Proposal Writer",
        "category": "sales",
        "description": "Redactor de propuestas comerciales",
        "emoji": "📝",
        "capabilities": ["proposal_writing", "rfp_response", "pricing", "presentation"],
        "specialization": "Propuestas Comerciales",
        "complexity": "intermediate"
    },
    "crm_specialist": {
        "name": "CRM Specialist",
        "category": "sales",
        "description": "Especialista en CRM y automatización de ventas",
        "emoji": "🔧",
        "capabilities": ["crm_management", "automation", "data_quality", "integration"],
        "specialization": "CRM",
        "complexity": "intermediate"
    },
    "channel_manager": {
        "name": "Channel Manager",
        "category": "sales",
        "description": "Gestor de canales de distribución",
        "emoji": "🔗",
        "capabilities": ["channel_strategy", "partner_management", "distribution", "pricing"],
        "specialization": "Gestión de Canales",
        "complexity": "advanced"
    },
    "sales_engineer": {
        "name": "Sales Engineer",
        "category": "sales",
        "description": "Ingeniero de ventas técnicas",
        "emoji": "⚙️",
        "capabilities": ["technical_sales", "demos", "solutions", "pre_sales"],
        "specialization": "Ventas Técnicas",
        "complexity": "advanced"
    },
}

# ============================================================================
# CATEGORÍA: OPERATIONS (10 agentes)
# ============================================================================
OPERATIONS_DEFINITIONS = {
    "operations_manager": {
        "name": "Operations Manager",
        "category": "operations",
        "description": "Gerente de operaciones y procesos",
        "emoji": "⚙️",
        "capabilities": ["process_management", "optimization", "resource_allocation", "kpis"],
        "specialization": "Gestión de Operaciones",
        "complexity": "advanced"
    },
    "supply_chain_analyst": {
        "name": "Supply Chain Analyst",
        "category": "operations",
        "description": "Analista de cadena de suministro",
        "emoji": "🔗",
        "capabilities": ["supply_chain", "logistics", "inventory", "demand_planning"],
        "specialization": "Cadena de Suministro",
        "complexity": "advanced"
    },
    "process_optimizer": {
        "name": "Process Optimizer",
        "category": "operations",
        "description": "Optimizador de procesos empresariales",
        "emoji": "📈",
        "capabilities": ["process_improvement", "automation", "efficiency", "lean"],
        "specialization": "Optimización de Procesos",
        "complexity": "advanced"
    },
    "quality_assurance": {
        "name": "Quality Assurance",
        "category": "operations",
        "description": "Aseguramiento de calidad operacional",
        "emoji": "✅",
        "capabilities": ["quality_control", "standards", "audits", "continuous_improvement"],
        "specialization": "Aseguramiento de Calidad",
        "complexity": "intermediate"
    },
    "logistics_coordinator": {
        "name": "Logistics Coordinator",
        "category": "operations",
        "description": "Coordinador de logística y distribución",
        "emoji": "🚚",
        "capabilities": ["logistics", "shipping", "warehousing", "route_optimization"],
        "specialization": "Logística",
        "complexity": "intermediate"
    },
    "inventory_specialist": {
        "name": "Inventory Specialist",
        "category": "operations",
        "description": "Especialista en gestión de inventarios",
        "emoji": "📦",
        "capabilities": ["inventory_management", "forecasting", "stock_control", "optimization"],
        "specialization": "Gestión de Inventarios",
        "complexity": "intermediate"
    },
    "procurement_specialist": {
        "name": "Procurement Specialist",
        "category": "operations",
        "description": "Especialista en compras y adquisiciones",
        "emoji": "🛒",
        "capabilities": ["sourcing", "negotiation", "vendor_management", "cost_reduction"],
        "specialization": "Compras",
        "complexity": "advanced"
    },
    "lean_specialist": {
        "name": "Lean Specialist",
        "category": "operations",
        "description": "Especialista en metodología Lean",
        "emoji": "🎯",
        "capabilities": ["lean", "six_sigma", "waste_reduction", "continuous_improvement"],
        "specialization": "Lean Manufacturing",
        "complexity": "advanced"
    },
    "warehouse_manager": {
        "name": "Warehouse Manager",
        "category": "operations",
        "description": "Gerente de almacén y centros de distribución",
        "emoji": "🏭",
        "capabilities": ["warehouse_management", "wms", "picking", "space_optimization"],
        "specialization": "Gestión de Almacenes",
        "complexity": "intermediate"
    },
    "distribution_planner": {
        "name": "Distribution Planner",
        "category": "operations",
        "description": "Planificador de distribución",
        "emoji": "📋",
        "capabilities": ["distribution_planning", "network_design", "capacity", "scheduling"],
        "specialization": "Planificación de Distribución",
        "complexity": "advanced"
    },
}

# ============================================================================
# CATEGORÍA: EDUCATION (10 agentes)
# ============================================================================
EDUCATION_DEFINITIONS = {
    "instructional_designer": {
        "name": "Instructional Designer",
        "category": "education",
        "description": "Diseñador instruccional de cursos y programas",
        "emoji": "📐",
        "capabilities": ["curriculum_design", "learning_objectives", "assessment", "addie"],
        "specialization": "Diseño Instruccional",
        "complexity": "advanced"
    },
    "curriculum_developer": {
        "name": "Curriculum Developer",
        "category": "education",
        "description": "Desarrollador de currículos educativos",
        "emoji": "📚",
        "capabilities": ["curriculum_development", "standards", "competencies", "evaluation"],
        "specialization": "Desarrollo Curricular",
        "complexity": "advanced"
    },
    "elearning_specialist": {
        "name": "E-Learning Specialist",
        "category": "education",
        "description": "Especialista en educación digital",
        "emoji": "💻",
        "capabilities": ["elearning", "lms", "multimedia", "scorm"],
        "specialization": "E-Learning",
        "complexity": "advanced"
    },
    "training_facilitator": {
        "name": "Training Facilitator",
        "category": "education",
        "description": "Facilitador de sesiones de capacitación",
        "emoji": "🎤",
        "capabilities": ["facilitation", "engagement", "delivery", "virtual_training"],
        "specialization": "Facilitación",
        "complexity": "intermediate"
    },
    "assessment_specialist": {
        "name": "Assessment Specialist",
        "category": "education",
        "description": "Especialista en evaluación educativa",
        "emoji": "📝",
        "capabilities": ["assessment_design", "psychometrics", "rubrics", "analysis"],
        "specialization": "Evaluación Educativa",
        "complexity": "advanced"
    },
    "educational_technologist": {
        "name": "Educational Technologist",
        "category": "education",
        "description": "Tecnólogo educativo",
        "emoji": "🔧",
        "capabilities": ["edtech", "tool_selection", "integration", "innovation"],
        "specialization": "Tecnología Educativa",
        "complexity": "advanced"
    },
    "tutor_specialist": {
        "name": "Tutor Specialist",
        "category": "education",
        "description": "Especialista en tutoría personalizada",
        "emoji": "👨‍🏫",
        "capabilities": ["tutoring", "personalization", "student_support", "motivation"],
        "specialization": "Tutoría",
        "complexity": "intermediate"
    },
    "academic_advisor": {
        "name": "Academic Advisor",
        "category": "education",
        "description": "Asesor académico y de carrera",
        "emoji": "🎓",
        "capabilities": ["academic_advising", "career_guidance", "planning", "support"],
        "specialization": "Asesoría Académica",
        "complexity": "intermediate"
    },
    "content_curator": {
        "name": "Content Curator",
        "category": "education",
        "description": "Curador de contenido educativo",
        "emoji": "📖",
        "capabilities": ["content_curation", "oer", "quality_review", "organization"],
        "specialization": "Curación de Contenido",
        "complexity": "intermediate"
    },
    "learning_analyst": {
        "name": "Learning Analyst",
        "category": "education",
        "description": "Analista de aprendizaje y datos educativos",
        "emoji": "📊",
        "capabilities": ["learning_analytics", "data_analysis", "insights", "improvement"],
        "specialization": "Analytics de Aprendizaje",
        "complexity": "advanced"
    },
}

# ============================================================================
# CATEGORÍA: CREATIVE (10 agentes)
# ============================================================================
CREATIVE_DEFINITIONS = {
    "graphic_designer": {
        "name": "Graphic Designer",
        "category": "creative",
        "description": "Diseñador gráfico y visual",
        "emoji": "🎨",
        "capabilities": ["visual_design", "branding", "print", "digital"],
        "specialization": "Diseño Gráfico",
        "complexity": "intermediate"
    },
    "ui_designer": {
        "name": "UI Designer",
        "category": "creative",
        "description": "Diseñador de interfaces de usuario",
        "emoji": "📱",
        "capabilities": ["ui_design", "design_systems", "prototyping", "figma"],
        "specialization": "Diseño UI",
        "complexity": "advanced"
    },
    "ux_designer": {
        "name": "UX Designer",
        "category": "creative",
        "description": "Diseñador de experiencia de usuario",
        "emoji": "🧪",
        "capabilities": ["ux_research", "user_testing", "wireframing", "journey_mapping"],
        "specialization": "Diseño UX",
        "complexity": "advanced"
    },
    "video_producer": {
        "name": "Video Producer",
        "category": "creative",
        "description": "Productor de video y contenido audiovisual",
        "emoji": "🎬",
        "capabilities": ["video_production", "editing", "storytelling", "post_production"],
        "specialization": "Producción de Video",
        "complexity": "advanced"
    },
    "motion_designer": {
        "name": "Motion Designer",
        "category": "creative",
        "description": "Diseñador de motion graphics",
        "emoji": "✨",
        "capabilities": ["motion_graphics", "animation", "after_effects", "compositing"],
        "specialization": "Motion Graphics",
        "complexity": "advanced"
    },
    "illustrator": {
        "name": "Illustrator",
        "category": "creative",
        "description": "Ilustrador digital y tradicional",
        "emoji": "🖼️",
        "capabilities": ["illustration", "concept_art", "character_design", "digital_art"],
        "specialization": "Ilustración",
        "complexity": "intermediate"
    },
    "brand_designer": {
        "name": "Brand Designer",
        "category": "creative",
        "description": "Diseñador de identidad de marca",
        "emoji": "⭐",
        "capabilities": ["brand_identity", "logo_design", "guidelines", "visual_strategy"],
        "specialization": "Diseño de Marca",
        "complexity": "advanced"
    },
    "creative_director": {
        "name": "Creative Director",
        "category": "creative",
        "description": "Director creativo",
        "emoji": "🎯",
        "capabilities": ["creative_direction", "team_leadership", "concept_development", "campaigns"],
        "specialization": "Dirección Creativa",
        "complexity": "expert"
    },
    "animator": {
        "name": "Animator",
        "category": "creative",
        "description": "Animador 2D/3D",
        "emoji": "🎭",
        "capabilities": ["2d_animation", "3d_animation", "character_animation", "rigging"],
        "specialization": "Animación",
        "complexity": "advanced"
    },
    "three_d_artist": {
        "name": "3D Artist",
        "category": "creative",
        "description": "Artista 3D y modelado",
        "emoji": "🧊",
        "capabilities": ["3d_modeling", "texturing", "rendering", "lighting"],
        "specialization": "Arte 3D",
        "complexity": "advanced"
    },
}

# ============================================================================
# CATEGORÍA: PROJECT MANAGEMENT (10 agentes)
# ============================================================================
PROJECT_MANAGEMENT_DEFINITIONS = {
    "project_manager": {
        "name": "Project Manager",
        "category": "project_management",
        "description": "Gerente de proyectos certificado",
        "emoji": "📋",
        "capabilities": ["project_planning", "risk_management", "stakeholders", "delivery"],
        "specialization": "Gestión de Proyectos",
        "complexity": "advanced"
    },
    "scrum_master": {
        "name": "Scrum Master",
        "category": "project_management",
        "description": "Scrum Master certificado",
        "emoji": "🔄",
        "capabilities": ["scrum", "facilitation", "coaching", "impediment_removal"],
        "specialization": "Scrum",
        "complexity": "advanced"
    },
    "agile_coach": {
        "name": "Agile Coach",
        "category": "project_management",
        "description": "Coach ágil y transformación",
        "emoji": "🏃",
        "capabilities": ["agile_coaching", "transformation", "frameworks", "culture"],
        "specialization": "Coaching Ágil",
        "complexity": "expert"
    },
    "product_owner": {
        "name": "Product Owner",
        "category": "project_management",
        "description": "Product Owner y gestión de backlog",
        "emoji": "📦",
        "capabilities": ["backlog_management", "prioritization", "stakeholder_collaboration", "vision"],
        "specialization": "Product Owner",
        "complexity": "advanced"
    },
    "program_manager": {
        "name": "Program Manager",
        "category": "project_management",
        "description": "Gerente de programas y portafolios",
        "emoji": "🎯",
        "capabilities": ["program_management", "portfolio", "governance", "benefits_realization"],
        "specialization": "Gestión de Programas",
        "complexity": "expert"
    },
    "portfolio_manager": {
        "name": "Portfolio Manager",
        "category": "project_management",
        "description": "Gestor de portafolio de proyectos",
        "emoji": "📊",
        "capabilities": ["portfolio_management", "prioritization", "resource_allocation", "roi"],
        "specialization": "Gestión de Portafolio",
        "complexity": "expert"
    },
    "resource_planner": {
        "name": "Resource Planner",
        "category": "project_management",
        "description": "Planificador de recursos",
        "emoji": "👥",
        "capabilities": ["resource_planning", "capacity", "allocation", "forecasting"],
        "specialization": "Planificación de Recursos",
        "complexity": "intermediate"
    },
    "change_manager": {
        "name": "Change Manager",
        "category": "project_management",
        "description": "Gestor del cambio organizacional",
        "emoji": "🔀",
        "capabilities": ["change_management", "communication", "training", "adoption"],
        "specialization": "Gestión del Cambio",
        "complexity": "advanced"
    },
    "pmo_specialist": {
        "name": "PMO Specialist",
        "category": "project_management",
        "description": "Especialista de PMO",
        "emoji": "🏛️",
        "capabilities": ["pmo", "governance", "standards", "reporting"],
        "specialization": "PMO",
        "complexity": "advanced"
    },
    "stakeholder_manager": {
        "name": "Stakeholder Manager",
        "category": "project_management",
        "description": "Gestor de stakeholders",
        "emoji": "🤝",
        "capabilities": ["stakeholder_management", "communication", "engagement", "influence"],
        "specialization": "Gestión de Stakeholders",
        "complexity": "advanced"
    },
}

# ============================================================================
# CATEGORÍA: MERCADO LIBRE (10 agentes)
# ============================================================================
MERCADOLIBRE_DEFINITIONS = {
    "ml_listing_optimizer": {
        "name": "ML Listing Optimizer",
        "category": "mercadolibre",
        "description": "Optimizador de publicaciones en Mercado Libre",
        "emoji": "✨",
        "capabilities": ["title_optimization", "seo_ml", "attributes", "keywords"],
        "specialization": "Optimización de Publicaciones",
        "complexity": "advanced"
    },
    "ml_ads_specialist": {
        "name": "ML Ads Specialist",
        "category": "mercadolibre",
        "description": "Especialista en Product Ads de Mercado Libre",
        "emoji": "🎯",
        "capabilities": ["product_ads", "campaigns", "bidding", "acos_optimization"],
        "specialization": "Publicidad ML",
        "complexity": "advanced"
    },
    "ml_customer_service": {
        "name": "ML Customer Service",
        "category": "mercadolibre",
        "description": "Especialista en atención al cliente ML",
        "emoji": "💬",
        "capabilities": ["customer_service", "questions", "claims", "conversion"],
        "specialization": "Atención al Cliente ML",
        "complexity": "intermediate"
    },
    "ml_reputation_manager": {
        "name": "ML Reputation Manager",
        "category": "mercadolibre",
        "description": "Gestor de reputación en Mercado Libre",
        "emoji": "⭐",
        "capabilities": ["reputation", "mercadolider", "claims", "reviews"],
        "specialization": "Gestión de Reputación",
        "complexity": "advanced"
    },
    "ml_pricing_strategist": {
        "name": "ML Pricing Strategist",
        "category": "mercadolibre",
        "description": "Estratega de precios para Mercado Libre",
        "emoji": "💰",
        "capabilities": ["pricing", "competition", "margins", "promotions"],
        "specialization": "Estrategia de Precios",
        "complexity": "advanced"
    },
    "ml_logistics_expert": {
        "name": "ML Logistics Expert",
        "category": "mercadolibre",
        "description": "Experto en logística Mercado Envíos",
        "emoji": "🚚",
        "capabilities": ["mercado_envios", "fulfillment", "shipping", "costs"],
        "specialization": "Logística ML",
        "complexity": "advanced"
    },
    "ml_catalog_manager": {
        "name": "ML Catalog Manager",
        "category": "mercadolibre",
        "description": "Gestor de catálogo y variaciones",
        "emoji": "📋",
        "capabilities": ["catalog", "variations", "categories", "bulk_upload"],
        "specialization": "Gestión de Catálogo",
        "complexity": "intermediate"
    },
    "ml_analytics_expert": {
        "name": "ML Analytics Expert",
        "category": "mercadolibre",
        "description": "Analista de datos de Mercado Libre",
        "emoji": "📊",
        "capabilities": ["analytics", "metrics", "trends", "reporting"],
        "specialization": "Analytics ML",
        "complexity": "advanced"
    },
    "mercadolibre_product_specialist": {
        "name": "ML Product Specialist",
        "category": "mercadolibre",
        "description": "Especialista en fichas de producto",
        "emoji": "📦",
        "capabilities": ["product_specs", "descriptions", "photos", "attributes"],
        "specialization": "Fichas de Producto",
        "complexity": "advanced"
    },
    "mercadolibre_sales_optimizer": {
        "name": "ML Sales Optimizer",
        "category": "mercadolibre",
        "description": "Optimizador de ventas en Mercado Libre",
        "emoji": "📈",
        "capabilities": ["sales_strategy", "conversion", "growth", "optimization"],
        "specialization": "Optimización de Ventas",
        "complexity": "advanced"
    },
}

# ============================================================================
# CATEGORÍA: YOUTUBE (10 agentes)
# ============================================================================
YOUTUBE_DEFINITIONS = {
    "yt_content_strategist": {
        "name": "YT Content Strategist",
        "category": "youtube",
        "description": "Estratega de contenido para YouTube",
        "emoji": "📺",
        "capabilities": ["content_strategy", "niche", "pillars", "calendar"],
        "specialization": "Estrategia de Contenido YT",
        "complexity": "advanced"
    },
    "yt_seo_specialist": {
        "name": "YT SEO Specialist",
        "category": "youtube",
        "description": "Especialista en SEO de YouTube",
        "emoji": "🔍",
        "capabilities": ["youtube_seo", "keywords", "tags", "optimization"],
        "specialization": "SEO YouTube",
        "complexity": "advanced"
    },
    "yt_script_writer": {
        "name": "YT Script Writer",
        "category": "youtube",
        "description": "Guionista para videos de YouTube",
        "emoji": "📝",
        "capabilities": ["script_writing", "hooks", "retention", "storytelling"],
        "specialization": "Guiones YouTube",
        "complexity": "advanced"
    },
    "yt_thumbnail_designer": {
        "name": "YT Thumbnail Designer",
        "category": "youtube",
        "description": "Diseñador de thumbnails",
        "emoji": "🖼️",
        "capabilities": ["thumbnail_design", "ctr", "visual_strategy", "a_b_testing"],
        "specialization": "Thumbnails YouTube",
        "complexity": "intermediate"
    },
    "yt_analytics_expert": {
        "name": "YT Analytics Expert",
        "category": "youtube",
        "description": "Experto en YouTube Analytics",
        "emoji": "📊",
        "capabilities": ["youtube_analytics", "metrics", "retention", "insights"],
        "specialization": "Analytics YouTube",
        "complexity": "advanced"
    },
    "yt_monetization_expert": {
        "name": "YT Monetization Expert",
        "category": "youtube",
        "description": "Experto en monetización de YouTube",
        "emoji": "💵",
        "capabilities": ["monetization", "adsense", "sponsors", "revenue"],
        "specialization": "Monetización YouTube",
        "complexity": "advanced"
    },
    "yt_shorts_specialist": {
        "name": "YT Shorts Specialist",
        "category": "youtube",
        "description": "Especialista en YouTube Shorts",
        "emoji": "📱",
        "capabilities": ["shorts", "viral_content", "trends", "hooks"],
        "specialization": "YouTube Shorts",
        "complexity": "intermediate"
    },
    "yt_community_manager": {
        "name": "YT Community Manager",
        "category": "youtube",
        "description": "Community Manager de YouTube",
        "emoji": "👥",
        "capabilities": ["community", "comments", "engagement", "posts"],
        "specialization": "Comunidad YouTube",
        "complexity": "intermediate"
    },
    "yt_video_editor_advisor": {
        "name": "YT Video Editor Advisor",
        "category": "youtube",
        "description": "Asesor de edición de video",
        "emoji": "🎞️",
        "capabilities": ["editing", "pacing", "effects", "retention"],
        "specialization": "Edición YouTube",
        "complexity": "advanced"
    },
    "yt_growth_strategist": {
        "name": "YT Growth Strategist",
        "category": "youtube",
        "description": "Estratega de crecimiento de YouTube",
        "emoji": "🚀",
        "capabilities": ["growth", "subscribers", "virality", "algorithm"],
        "specialization": "Crecimiento YouTube",
        "complexity": "advanced"
    },
}

# ============================================================================
# COMBINAR TODAS LAS DEFINICIONES
# ============================================================================

AGENT_DEFINITIONS.update(SOFTWARE_DEVELOPMENT_DEFINITIONS)
AGENT_DEFINITIONS.update(MARKETING_DEFINITIONS)
AGENT_DEFINITIONS.update(FINANCE_DEFINITIONS)
AGENT_DEFINITIONS.update(LEGAL_DEFINITIONS)
AGENT_DEFINITIONS.update(HUMAN_RESOURCES_DEFINITIONS)
AGENT_DEFINITIONS.update(SALES_DEFINITIONS)
AGENT_DEFINITIONS.update(OPERATIONS_DEFINITIONS)
AGENT_DEFINITIONS.update(EDUCATION_DEFINITIONS)
AGENT_DEFINITIONS.update(CREATIVE_DEFINITIONS)
AGENT_DEFINITIONS.update(PROJECT_MANAGEMENT_DEFINITIONS)
AGENT_DEFINITIONS.update(MERCADOLIBRE_DEFINITIONS)
AGENT_DEFINITIONS.update(YOUTUBE_DEFINITIONS)

# ============================================================================
# CATEGORÍAS Y METADATA
# ============================================================================

CATEGORIES = {
    "software_development": {
        "name": "Desarrollo de Software",
        "emoji": "💻",
        "description": "Agentes especializados en desarrollo, arquitectura y tecnología",
        "color": "#3B82F6",
        "agents_count": 10
    },
    "marketing": {
        "name": "Marketing Digital",
        "emoji": "📢",
        "description": "Agentes de marketing, publicidad y growth",
        "color": "#EC4899",
        "agents_count": 10
    },
    "finance": {
        "name": "Finanzas",
        "emoji": "💰",
        "description": "Agentes de finanzas, contabilidad e inversiones",
        "color": "#10B981",
        "agents_count": 10
    },
    "legal": {
        "name": "Legal",
        "emoji": "⚖️",
        "description": "Agentes legales, compliance y contratos",
        "color": "#8B5CF6",
        "agents_count": 10
    },
    "human_resources": {
        "name": "Recursos Humanos",
        "emoji": "👥",
        "description": "Agentes de RRHH, talento y cultura",
        "color": "#F59E0B",
        "agents_count": 10
    },
    "sales": {
        "name": "Ventas",
        "emoji": "🤝",
        "description": "Agentes de ventas, desarrollo de negocios y CRM",
        "color": "#EF4444",
        "agents_count": 10
    },
    "operations": {
        "name": "Operaciones",
        "emoji": "⚙️",
        "description": "Agentes de operaciones, logística y supply chain",
        "color": "#6B7280",
        "agents_count": 10
    },
    "education": {
        "name": "Educación",
        "emoji": "📚",
        "description": "Agentes educativos, e-learning y capacitación",
        "color": "#14B8A6",
        "agents_count": 10
    },
    "creative": {
        "name": "Creatividad",
        "emoji": "🎨",
        "description": "Agentes creativos, diseño y multimedia",
        "color": "#F472B6",
        "agents_count": 10
    },
    "project_management": {
        "name": "Gestión de Proyectos",
        "emoji": "📋",
        "description": "Agentes de PM, Agile y PMO",
        "color": "#06B6D4",
        "agents_count": 10
    },
    "mercadolibre": {
        "name": "Mercado Libre",
        "emoji": "🛒",
        "description": "Agentes especializados en Mercado Libre",
        "color": "#FFE600",
        "agents_count": 10
    },
    "youtube": {
        "name": "YouTube",
        "emoji": "▶️",
        "description": "Agentes especializados en YouTube",
        "color": "#FF0000",
        "agents_count": 10
    },
}

def get_agents_by_category(category: str) -> Dict[str, Dict[str, Any]]:
    """Obtiene todos los agentes de una categoría"""
    return {
        agent_id: info 
        for agent_id, info in AGENT_DEFINITIONS.items() 
        if info.get("category") == category
    }

def get_all_categories() -> List[str]:
    """Obtiene lista de todas las categorías"""
    return list(CATEGORIES.keys())

def get_category_info(category: str) -> Optional[Dict[str, Any]]:
    """Obtiene información de una categoría"""
    return CATEGORIES.get(category)

def get_agent_count() -> int:
    """Obtiene el número total de agentes"""
    return len(AGENT_DEFINITIONS)
