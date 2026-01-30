import {
    Rocket, Code2, Scale, LineChart, Megaphone, BookOpen, DollarSign, Map,
    Search, RefreshCw, AlertTriangle, Palette, Database, Target, GraduationCap,
    Users, Briefcase, TrendingUp, Shield, Zap, Globe, Package, FileText,
    MessageSquare, PieChart, Settings, Cloud, Smartphone, Video, ShoppingCart,
    Heart, Music, Camera, Plane, Coffee, Home, Car, Book, Lightbulb, Trophy,
    Star, Gift, Bell, Mail, Phone, Calendar, Clock, Flag, Hash, Percent, Boxes,
    Building2, Workflow, CheckCircle2, BarChart3, Repeat, Network, Layers, Youtube
} from "lucide-react";

// AFW v0.5.0 - 50 Tareas Predefinidas en Español con Mínimo 5 Agentes
export const PRESETS = [
    // ========== DESARROLLO DE SOFTWARE (10 tareas) ==========
    {
        title: "Aplicación FullStack",
        description: "Desarrollo completo de aplicación web frontend y backend",
        icon: Code2,
        agents: ["fullstack_developer", "backend_architect", "frontend_specialist", "database_expert", "qa_automation"]
    },
    {
        title: "Arquitectura Microservicios",
        description: "Diseño de sistemas distribuidos escalables y resilientes",
        icon: Cloud,
        agents: ["backend_architect", "devops_engineer", "database_expert", "tech_lead", "security_specialist"]
    },
    {
        title: "Revisión de Código",
        description: "Auditoría exhaustiva de código, arquitectura y mejores prácticas",
        icon: Search,
        agents: ["code_reviewer", "tech_lead", "security_specialist", "backend_architect", "qa_automation"]
    },
    {
        title: "Pipeline CI/CD",
        description: "Automatización completa de integración y despliegue continuo",
        icon: RefreshCw,
        agents: ["devops_engineer", "backend_architect", "security_specialist", "tech_lead", "qa_automation"]
    },
    {
        title: "Aplicación Móvil",
        description: "Desarrollo de app iOS/Android nativa o cross-platform",
        icon: Smartphone,
        agents: ["mobile_developer", "frontend_specialist", "qa_automation", "ui_designer", "ux_designer"]
    },
    {
        title: "API REST Escalable",
        description: "Diseño e implementación de APIs robustas y documentadas",
        icon: Zap,
        agents: ["backend_architect", "fullstack_developer", "database_expert", "security_specialist", "tech_lead"]
    },
    {
        title: "Optimización de BD",
        description: "Optimización de bases de datos, consultas y esquemas",
        icon: Database,
        agents: ["database_expert", "backend_architect", "devops_engineer", "tech_lead", "fullstack_developer"]
    },
    {
        title: "Auditoría de Seguridad",
        description: "Análisis completo de vulnerabilidades y hardening",
        icon: Shield,
        agents: ["security_specialist", "code_reviewer", "devops_engineer", "backend_architect", "tech_lead"]
    },
    {
        title: "Automatización QA",
        description: "Suite completa de pruebas automatizadas y CI",
        icon: Target,
        agents: ["qa_automation", "tech_lead", "fullstack_developer", "devops_engineer", "frontend_specialist"]
    },
    {
        title: "Liderazgo Técnico",
        description: "Estrategia técnica, mentoring y toma de decisiones",
        icon: Users,
        agents: ["tech_lead", "backend_architect", "code_reviewer", "devops_engineer", "fullstack_developer"]
    },

    // ========== MARKETING DIGITAL (5 tareas) ==========
    {
        title: "Campaña Digital 360°",
        description: "Estrategia integral de marketing digital multicanal",
        icon: Megaphone,
        agents: ["content_strategist", "social_media_manager", "ppc_specialist", "copywriter", "analytics_expert"]
    },
    {
        title: "Estrategia SEO",
        description: "Posicionamiento orgánico, contenido y link building",
        icon: TrendingUp,
        agents: ["seo_specialist", "content_strategist", "copywriter", "analytics_expert", "growth_hacker"]
    },
    {
        title: "Gestión Redes Sociales",
        description: "Community management y estrategia social media",
        icon: MessageSquare,
        agents: ["social_media_manager", "copywriter", "influencer_coordinator", "analytics_expert", "content_strategist"]
    },
    {
        title: "Email Marketing",
        description: "Campañas automatizadas, segmentación y nurturing",
        icon: Mail,
        agents: ["email_marketer", "copywriter", "analytics_expert", "content_strategist", "growth_hacker"]
    },
    {
        title: "Estrategia de Marca",
        description: "Branding, posicionamiento y crecimiento acelerado",
        icon: Star,
        agents: ["brand_strategist", "growth_hacker", "content_strategist", "analytics_expert", "copywriter"]
    },

    // ========== FINANZAS (5 tareas) ==========
    {
        title: "Análisis Financiero",
        description: "Análisis completo, proyecciones y valoración",
        icon: DollarSign,
        agents: ["financial_analyst", "investment_advisor", "risk_analyst", "financial_controller", "budget_planner"]
    },
    {
        title: "Planificación Presupuestaria",
        description: "Presupuestos, control de costos y forecasting",
        icon: PieChart,
        agents: ["budget_planner", "financial_controller", "accountant", "financial_analyst", "risk_analyst"]
    },
    {
        title: "Gestión de Inversiones",
        description: "Portafolio de inversiones y asset allocation",
        icon: TrendingUp,
        agents: ["investment_advisor", "financial_analyst", "risk_analyst", "treasury_manager", "financial_controller"]
    },
    {
        title: "Planificación Fiscal",
        description: "Estrategia fiscal, compliance y optimización",
        icon: FileText,
        agents: ["tax_specialist", "accountant", "auditor", "financial_controller", "compliance_officer"]
    },
    {
        title: "Gestión de Riesgos",
        description: "Análisis, mitigación y control de riesgos financieros",
        icon: AlertTriangle,
        agents: ["risk_analyst", "financial_analyst", "auditor", "financial_controller", "treasury_manager"]
    },

    // ========== LEGAL (5 tareas) ==========
    {
        title: "Gestión de Contratos",
        description: "Redacción, revisión y negociación de contratos",
        icon: FileText,
        agents: ["contract_specialist", "corporate_lawyer", "paralegal_assistant", "compliance_officer", "legal_researcher"]
    },
    {
        title: "Cumplimiento Normativo",
        description: "Compliance regulatorio y políticas corporativas",
        icon: Scale,
        agents: ["compliance_officer", "corporate_lawyer", "regulatory_advisor", "data_privacy_officer", "legal_researcher"]
    },
    {
        title: "Propiedad Intelectual",
        description: "Protección de patentes, marcas y derechos de autor",
        icon: Shield,
        agents: ["intellectual_property", "corporate_lawyer", "contract_specialist", "legal_researcher", "paralegal_assistant"]
    },
    {
        title: "Investigación Legal",
        description: "Análisis jurisprudencial y due diligence",
        icon: BookOpen,
        agents: ["legal_researcher", "corporate_lawyer", "paralegal_assistant", "litigation_specialist", "regulatory_advisor"]
    },
    {
        title: "Derecho Laboral",
        description: "Relaciones laborales, contratos y conflictos",
        icon: Users,
        agents: ["labor_law_expert", "corporate_lawyer", "employee_relations", "compliance_officer", "legal_researcher"]
    },

    // ========== RECURSOS HUMANOS (5 tareas) ==========
    {
        title: "Adquisición de Talento",
        description: "Reclutamiento estratégico y employer branding",
        icon: Users,
        agents: ["recruiter", "talent_development", "hr_analytics", "onboarding_specialist", "culture_champion"]
    },
    {
        title: "Gestión del Desempeño",
        description: "Evaluaciones, feedback y planes de mejora",
        icon: Target,
        agents: ["performance_manager", "talent_development", "hr_analytics", "training_coordinator", "culture_champion"]
    },
    {
        title: "Capacitación y Desarrollo",
        description: "Programas de formación y desarrollo de carrera",
        icon: GraduationCap,
        agents: ["training_coordinator", "talent_development", "onboarding_specialist", "hr_analytics", "performance_manager"]
    },
    {
        title: "Cultura Organizacional",
        description: "Engagement, clima laboral y bienestar",
        icon: Heart,
        agents: ["culture_champion", "employee_relations", "hr_analytics", "talent_development", "onboarding_specialist"]
    },
    {
        title: "Compensaciones y Beneficios",
        description: "Diseño de paquetes salariales y prestaciones",
        icon: DollarSign,
        agents: ["compensation_analyst", "benefits_administrator", "hr_analytics", "payroll_specialist", "talent_development"]
    },

    // ========== VENTAS (5 tareas) ==========
    {
        title: "Estrategia Comercial",
        description: "Planificación de ventas y desarrollo de mercado",
        icon: TrendingUp,
        agents: ["sales_executive", "business_development", "sales_analyst", "account_manager", "customer_success"]
    },
    {
        title: "Generación de Leads",
        description: "Prospección, nurturing y calificación de leads",
        icon: Target,
        agents: ["business_development", "sales_executive", "crm_specialist", "sales_analyst", "proposal_writer"]
    },
    {
        title: "Automatización CRM",
        description: "Implementación y optimización de CRM",
        icon: Database,
        agents: ["crm_specialist", "sales_analyst", "sales_executive", "customer_success", "business_development"]
    },
    {
        title: "Capacitación en Ventas",
        description: "Entrenamiento, coaching y metodologías de venta",
        icon: GraduationCap,
        agents: ["sales_trainer", "sales_executive", "proposal_writer", "sales_analyst", "customer_success"]
    },
    {
        title: "Gestión de Cuentas",
        description: "Account management, upselling y retención",
        icon: Briefcase,
        agents: ["account_manager", "customer_success", "sales_executive", "crm_specialist", "business_development"]
    },

    // ========== OPERACIONES (5 tareas) ==========
    {
        title: "Optimización de Procesos",
        description: "Mejora continua, eficiencia y automatización",
        icon: Settings,
        agents: ["process_optimizer", "operations_manager", "lean_specialist", "quality_assurance", "supply_chain_analyst"]
    },
    {
        title: "Cadena de Suministro",
        description: "Supply chain, proveedores y abastecimiento",
        icon: Package,
        agents: ["supply_chain_analyst", "operations_manager", "procurement_specialist", "logistics_coordinator", "inventory_specialist"]
    },
    {
        title: "Control de Calidad",
        description: "Aseguramiento de calidad y estándares",
        icon: CheckCircle2,
        agents: ["quality_assurance", "operations_manager", "lean_specialist", "process_optimizer", "supply_chain_analyst"]
    },
    {
        title: "Logística y Distribución",
        description: "Planificación logística, rutas y almacenes",
        icon: Map,
        agents: ["logistics_coordinator", "distribution_planner", "warehouse_manager", "inventory_specialist", "supply_chain_analyst"]
    },
    {
        title: "Gestión de Inventarios",
        description: "Control de stock, forecasting y optimización",
        icon: Boxes,
        agents: ["inventory_specialist", "supply_chain_analyst", "warehouse_manager", "procurement_specialist", "operations_manager"]
    },

    // ========== EDUCACIÓN (5 tareas) ==========
    {
        title: "Diseño de Cursos",
        description: "Diseño instruccional y desarrollo curricular",
        icon: BookOpen,
        agents: ["instructional_designer", "curriculum_developer", "assessment_specialist", "elearning_specialist", "content_curator"]
    },
    {
        title: "Plataforma E-Learning",
        description: "Implementación de LMS y tecnología educativa",
        icon: Globe,
        agents: ["elearning_specialist", "educational_technologist", "instructional_designer", "learning_analyst", "content_curator"]
    },
    {
        title: "Contenido Educativo",
        description: "Creación de materiales y recursos didácticos",
        icon: FileText,
        agents: ["content_curator", "instructional_designer", "training_facilitator", "curriculum_developer", "elearning_specialist"]
    },
    {
        title: "Evaluación Educativa",
        description: "Diseño de evaluaciones y análisis de resultados",
        icon: Target,
        agents: ["assessment_specialist", "learning_analyst", "instructional_designer", "educational_technologist", "curriculum_developer"]
    },
    {
        title: "Facilitación de Capacitación",
        description: "Impartición de cursos y tutoría personalizada",
        icon: GraduationCap,
        agents: ["training_facilitator", "tutor_specialist", "academic_advisor", "instructional_designer", "elearning_specialist"]
    },

    // ========== CREATIVIDAD Y DISEÑO (5 tareas) ==========
    {
        title: "Identidad de Marca",
        description: "Branding, logo y guía de estilo visual",
        icon: Palette,
        agents: ["brand_designer", "creative_director", "graphic_designer", "ui_designer", "illustrator"]
    },
    {
        title: "Producción de Video",
        description: "Grabación, edición y post-producción audiovisual",
        icon: Video,
        agents: ["video_producer", "motion_designer", "animator", "creative_director", "graphic_designer"]
    },
    {
        title: "Sistema de Diseño UI/UX",
        description: "Design system, componentes y guías de experiencia",
        icon: Smartphone,
        agents: ["ux_designer", "ui_designer", "graphic_designer", "brand_designer", "creative_director"]
    },
    {
        title: "Arte 3D y Animación",
        description: "Modelado 3D, texturizado y animación",
        icon: Camera,
        agents: ["three_d_artist", "animator", "motion_designer", "creative_director", "illustrator"]
    },
    {
        title: "Motion Graphics",
        description: "Animación gráfica, efectos visuales y compositing",
        icon: Zap,
        agents: ["motion_designer", "animator", "video_producer", "graphic_designer", "creative_director"]
    },

    // ========== GESTIÓN DE PROYECTOS (5 tareas) ==========
    {
        title: "Planificación de Proyectos",
        description: "Cronogramas, recursos y gestión de entregables",
        icon: Calendar,
        agents: ["project_manager", "resource_planner", "stakeholder_manager", "pmo_specialist", "change_manager"]
    },
    {
        title: "Transformación Ágil",
        description: "Adopción de metodologías ágiles y coaching",
        icon: Repeat,
        agents: ["agile_coach", "scrum_master", "change_manager", "project_manager", "product_owner"]
    },
    {
        title: "Gestión de Programas",
        description: "Coordinación de múltiples proyectos relacionados",
        icon: Network,
        agents: ["program_manager", "portfolio_manager", "pmo_specialist", "project_manager", "stakeholder_manager"]
    },
    {
        title: "Implementación Scrum",
        description: "Framework Scrum, sprints y ceremonias ágiles",
        icon: Workflow,
        agents: ["scrum_master", "product_owner", "agile_coach", "project_manager", "resource_planner"]
    },
    {
        title: "Gestión del Cambio",
        description: "Change management, adopción y comunicación",
        icon: TrendingUp,
        agents: ["change_manager", "stakeholder_manager", "project_manager", "agile_coach", "pmo_specialist"]
    },

    // ========== MERCADO LIBRE (5 tareas) ==========
    {
        title: "Optimización de Publicaciones",
        description: "Títulos, fichas técnicas y posicionamiento ML",
        icon: Star,
        agents: ["ml_listing_optimizer", "ml_ads_specialist", "ml_customer_service", "ml_reputation_manager", "mercadolibre_product_specialist"]
    },
    {
        title: "Campañas Product Ads",
        description: "Publicidad pagada, ACOS y optimización de campañas",
        icon: Target,
        agents: ["ml_ads_specialist", "ml_listing_optimizer", "ml_reputation_manager", "ml_analytics_expert", "ml_pricing_strategist"]
    },
    {
        title: "Atención al Cliente ML",
        description: "Gestión de preguntas, reclamos y conversión",
        icon: MessageSquare,
        agents: ["ml_customer_service", "ml_reputation_manager", "ml_listing_optimizer", "ml_analytics_expert", "mercadolibre_sales_optimizer"]
    },
    {
        title: "Gestión de Reputación",
        description: "MercadoLíder, métricas y reviews",
        icon: Trophy,
        agents: ["ml_reputation_manager", "ml_customer_service", "ml_analytics_expert", "ml_listing_optimizer", "mercadolibre_sales_optimizer"]
    },
    {
        title: "Gestión Completa ML",
        description: "Administración integral de cuenta Mercado Libre",
        icon: Briefcase,
        agents: ["ml_listing_optimizer", "ml_ads_specialist", "ml_customer_service", "ml_reputation_manager", "ml_analytics_expert"]
    },

    // ========== YOUTUBE (5 tareas) ==========
    {
        title: "Estrategia de Contenido YT",
        description: "Planificación de contenido, nichos y calendario editorial",
        icon: Youtube,
        agents: ["yt_content_strategist", "yt_seo_specialist", "yt_script_writer", "yt_analytics_expert", "yt_growth_strategist"]
    },
    {
        title: "SEO para YouTube",
        description: "Optimización de títulos, tags y descripciones",
        icon: Search,
        agents: ["yt_seo_specialist", "yt_content_strategist", "yt_analytics_expert", "yt_thumbnail_designer", "yt_growth_strategist"]
    },
    {
        title: "Producción de Videos YT",
        description: "Guiones, edición y thumbnails optimizados",
        icon: Video,
        agents: ["yt_script_writer", "yt_video_editor_advisor", "yt_thumbnail_designer", "yt_content_strategist", "yt_seo_specialist"]
    },
    {
        title: "Monetización YouTube",
        description: "Estrategias de ingresos, sponsors y AdSense",
        icon: DollarSign,
        agents: ["yt_monetization_expert", "yt_growth_strategist", "yt_analytics_expert", "yt_content_strategist", "yt_community_manager"]
    },
    {
        title: "Crecimiento de Canal",
        description: "Estrategias de crecimiento, viralidad y retención",
        icon: TrendingUp,
        agents: ["yt_growth_strategist", "yt_analytics_expert", "yt_shorts_specialist", "yt_community_manager", "yt_content_strategist"]
    }
];
