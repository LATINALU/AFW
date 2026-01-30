"""
AFW v0.5.0 - Workflow Registry
Registro de 50 workflows pre-programados
"""
from typing import Dict, List, Optional
from .base_workflow import WorkflowTemplate, WorkflowStep, WorkflowComplexity

class WorkflowRegistry:
    """Registro singleton de todos los workflows disponibles"""
    _instance = None
    _workflows: Dict[str, WorkflowTemplate] = {}
    
    def __new__(cls):
        if cls._instance is None:
            cls._instance = super().__new__(cls)
            cls._instance._initialize_workflows()
        return cls._instance
    
    def _initialize_workflows(self):
        """Inicializa los 50 workflows pre-programados"""
        self._register_software_workflows()
        self._register_marketing_workflows()
        self._register_finance_workflows()
        self._register_legal_workflows()
        self._register_hr_workflows()
        self._register_sales_workflows()
        self._register_operations_workflows()
        self._register_education_workflows()
        self._register_creative_workflows()
        self._register_pm_workflows()
    
    def register(self, workflow: WorkflowTemplate):
        """Registra un workflow"""
        self._workflows[workflow.workflow_id] = workflow
    
    def get(self, workflow_id: str) -> Optional[WorkflowTemplate]:
        """Obtiene un workflow por ID"""
        return self._workflows.get(workflow_id)
    
    def get_by_category(self, category: str) -> List[WorkflowTemplate]:
        """Obtiene workflows por categoría"""
        return [w for w in self._workflows.values() if w.category == category]
    
    def get_all(self) -> List[WorkflowTemplate]:
        """Obtiene todos los workflows"""
        return list(self._workflows.values())
    
    def search(self, query: str) -> List[WorkflowTemplate]:
        """Busca workflows por nombre o descripción"""
        query = query.lower()
        return [w for w in self._workflows.values() 
                if query in w.name.lower() or query in w.description.lower()]

    def _register_software_workflows(self):
        """5 workflows de desarrollo de software"""
        self.register(WorkflowTemplate(
            workflow_id="sw_code_review", name="Code Review Completo",
            description="Revisión exhaustiva de código con análisis de seguridad y rendimiento",
            category="software_development", complexity=WorkflowComplexity.MEDIUM,
            estimated_time_minutes=30, required_agents=["code_reviewer", "security_specialist"],
            tags=["code", "review", "quality"], inputs=["code_snippet", "language"],
            outputs=["review_report", "recommendations"],
            steps=[
                WorkflowStep("s1", "Análisis de código", "Revisar estructura y patrones", 
                            "code_reviewer", "Revisa el siguiente código: {code_snippet}", 1),
                WorkflowStep("s2", "Revisión de seguridad", "Verificar vulnerabilidades",
                            "security_specialist", "Analiza seguridad: {code_snippet}", 2, ["s1"])
            ]
        ))
        self.register(WorkflowTemplate(
            workflow_id="sw_api_design", name="Diseño de API REST",
            description="Diseño completo de API REST con documentación OpenAPI",
            category="software_development", complexity=WorkflowComplexity.HIGH,
            estimated_time_minutes=60, required_agents=["backend_architect", "tech_lead"],
            tags=["api", "rest", "design"], inputs=["requirements", "domain"],
            outputs=["api_spec", "endpoints", "documentation"],
            steps=[
                WorkflowStep("s1", "Análisis de requisitos", "Entender necesidades",
                            "tech_lead", "Analiza requisitos: {requirements}", 1),
                WorkflowStep("s2", "Diseño de endpoints", "Definir estructura API",
                            "backend_architect", "Diseña API para: {domain}", 2, ["s1"])
            ]
        ))
        self.register(WorkflowTemplate(
            workflow_id="sw_db_optimization", name="Optimización de Base de Datos",
            description="Análisis y optimización de consultas y estructura de BD",
            category="software_development", complexity=WorkflowComplexity.HIGH,
            estimated_time_minutes=45, required_agents=["database_expert", "backend_architect"],
            tags=["database", "optimization", "performance"], inputs=["schema", "queries"],
            outputs=["optimization_report", "improved_queries"],
            steps=[
                WorkflowStep("s1", "Análisis de esquema", "Revisar estructura",
                            "database_expert", "Analiza esquema: {schema}", 1),
                WorkflowStep("s2", "Optimización de queries", "Mejorar consultas",
                            "database_expert", "Optimiza: {queries}", 2, ["s1"])
            ]
        ))
        self.register(WorkflowTemplate(
            workflow_id="sw_ci_cd_setup", name="Configuración CI/CD",
            description="Setup completo de pipeline de integración y despliegue continuo",
            category="software_development", complexity=WorkflowComplexity.HIGH,
            estimated_time_minutes=90, required_agents=["devops_engineer", "security_specialist"],
            tags=["cicd", "devops", "automation"], inputs=["project_type", "cloud_provider"],
            outputs=["pipeline_config", "deployment_scripts"],
            steps=[
                WorkflowStep("s1", "Diseño de pipeline", "Definir etapas CI/CD",
                            "devops_engineer", "Diseña pipeline para: {project_type}", 1),
                WorkflowStep("s2", "Seguridad del pipeline", "Agregar controles",
                            "security_specialist", "Asegura pipeline para: {cloud_provider}", 2, ["s1"])
            ]
        ))
        self.register(WorkflowTemplate(
            workflow_id="sw_mobile_app", name="Planificación App Móvil",
            description="Planificación técnica completa para desarrollo de app móvil",
            category="software_development", complexity=WorkflowComplexity.HIGH,
            estimated_time_minutes=120, required_agents=["mobile_developer", "frontend_specialist", "tech_lead"],
            tags=["mobile", "app", "planning"], inputs=["app_concept", "platforms"],
            outputs=["technical_spec", "architecture", "timeline"],
            steps=[
                WorkflowStep("s1", "Definición técnica", "Especificar arquitectura",
                            "tech_lead", "Define arquitectura para: {app_concept}", 1),
                WorkflowStep("s2", "Diseño móvil", "Planificar desarrollo",
                            "mobile_developer", "Planifica para: {platforms}", 2, ["s1"])
            ]
        ))

    def _register_marketing_workflows(self):
        """5 workflows de marketing"""
        self.register(WorkflowTemplate(
            workflow_id="mk_campaign_launch", name="Lanzamiento de Campaña",
            description="Planificación y ejecución de campaña de marketing digital",
            category="marketing", complexity=WorkflowComplexity.HIGH,
            estimated_time_minutes=120, required_agents=["content_strategist", "seo_specialist", "social_media_manager"],
            tags=["campaign", "digital", "launch"], inputs=["product", "target_audience", "budget"],
            outputs=["campaign_plan", "content_calendar", "kpis"],
            steps=[
                WorkflowStep("s1", "Estrategia de contenido", "Definir mensajes clave",
                            "content_strategist", "Crea estrategia para: {product}", 1),
                WorkflowStep("s2", "Optimización SEO", "Palabras clave y SEO",
                            "seo_specialist", "Optimiza para: {target_audience}", 2, ["s1"]),
                WorkflowStep("s3", "Plan de redes sociales", "Calendario de publicaciones",
                            "social_media_manager", "Planifica contenido social", 3, ["s1"])
            ]
        ))
        self.register(WorkflowTemplate(
            workflow_id="mk_seo_audit", name="Auditoría SEO Completa",
            description="Auditoría técnica y de contenido SEO con recomendaciones",
            category="marketing", complexity=WorkflowComplexity.MEDIUM,
            estimated_time_minutes=60, required_agents=["seo_specialist", "analytics_expert"],
            tags=["seo", "audit", "optimization"], inputs=["website_url"],
            outputs=["seo_report", "recommendations", "action_plan"],
            steps=[
                WorkflowStep("s1", "Análisis técnico", "Revisar SEO técnico",
                            "seo_specialist", "Audita: {website_url}", 1),
                WorkflowStep("s2", "Análisis de datos", "Revisar métricas",
                            "analytics_expert", "Analiza datos de: {website_url}", 2)
            ]
        ))
        self.register(WorkflowTemplate(
            workflow_id="mk_email_sequence", name="Secuencia de Email Marketing",
            description="Diseño de secuencia automatizada de emails",
            category="marketing", complexity=WorkflowComplexity.MEDIUM,
            estimated_time_minutes=45, required_agents=["email_marketer", "copywriter"],
            tags=["email", "automation", "nurturing"], inputs=["goal", "audience_segment"],
            outputs=["email_sequence", "subject_lines", "automation_flow"],
            steps=[
                WorkflowStep("s1", "Diseño de secuencia", "Planificar flujo de emails",
                            "email_marketer", "Diseña secuencia para: {goal}", 1),
                WorkflowStep("s2", "Redacción de emails", "Escribir contenido",
                            "copywriter", "Redacta para: {audience_segment}", 2, ["s1"])
            ]
        ))
        self.register(WorkflowTemplate(
            workflow_id="mk_brand_strategy", name="Estrategia de Marca",
            description="Desarrollo de estrategia de marca y posicionamiento",
            category="marketing", complexity=WorkflowComplexity.HIGH,
            estimated_time_minutes=90, required_agents=["brand_strategist", "content_strategist"],
            tags=["brand", "strategy", "positioning"], inputs=["company", "competitors"],
            outputs=["brand_strategy", "positioning", "messaging"],
            steps=[
                WorkflowStep("s1", "Análisis de marca", "Evaluar posición actual",
                            "brand_strategist", "Analiza marca: {company}", 1),
                WorkflowStep("s2", "Estrategia de contenido", "Definir voz de marca",
                            "content_strategist", "Define voz para competir con: {competitors}", 2, ["s1"])
            ]
        ))
        self.register(WorkflowTemplate(
            workflow_id="mk_ppc_campaign", name="Campaña PPC",
            description="Setup y optimización de campaña de pago por clic",
            category="marketing", complexity=WorkflowComplexity.MEDIUM,
            estimated_time_minutes=60, required_agents=["ppc_specialist", "copywriter"],
            tags=["ppc", "ads", "google"], inputs=["product", "budget", "target"],
            outputs=["campaign_structure", "ad_copy", "keywords"],
            steps=[
                WorkflowStep("s1", "Estructura de campaña", "Diseñar estructura PPC",
                            "ppc_specialist", "Diseña campaña para: {product}", 1),
                WorkflowStep("s2", "Copy de anuncios", "Redactar anuncios",
                            "copywriter", "Escribe ads para: {target}", 2, ["s1"])
            ]
        ))

    def _register_finance_workflows(self):
        """5 workflows de finanzas"""
        self.register(WorkflowTemplate(
            workflow_id="fn_financial_analysis", name="Análisis Financiero",
            description="Análisis completo de estados financieros y proyecciones",
            category="finance", complexity=WorkflowComplexity.HIGH,
            estimated_time_minutes=90, required_agents=["financial_analyst", "financial_controller"],
            tags=["analysis", "financial", "projections"], inputs=["financial_statements"],
            outputs=["analysis_report", "ratios", "projections"],
            steps=[
                WorkflowStep("s1", "Análisis de estados", "Revisar estados financieros",
                            "financial_analyst", "Analiza: {financial_statements}", 1),
                WorkflowStep("s2", "Validación", "Verificar consistencia",
                            "financial_controller", "Valida análisis", 2, ["s1"])
            ]
        ))
        self.register(WorkflowTemplate(
            workflow_id="fn_budget_planning", name="Planificación Presupuestal",
            description="Desarrollo de presupuesto anual con proyecciones",
            category="finance", complexity=WorkflowComplexity.HIGH,
            estimated_time_minutes=120, required_agents=["budget_planner", "financial_analyst"],
            tags=["budget", "planning", "annual"], inputs=["historical_data", "goals"],
            outputs=["budget", "variance_analysis", "forecasts"],
            steps=[
                WorkflowStep("s1", "Análisis histórico", "Revisar datos pasados",
                            "financial_analyst", "Analiza histórico: {historical_data}", 1),
                WorkflowStep("s2", "Planificación", "Crear presupuesto",
                            "budget_planner", "Planifica para: {goals}", 2, ["s1"])
            ]
        ))
        self.register(WorkflowTemplate(
            workflow_id="fn_investment_eval", name="Evaluación de Inversión",
            description="Análisis de viabilidad de inversión con ROI",
            category="finance", complexity=WorkflowComplexity.HIGH,
            estimated_time_minutes=60, required_agents=["investment_advisor", "risk_analyst"],
            tags=["investment", "roi", "evaluation"], inputs=["investment_proposal"],
            outputs=["evaluation_report", "roi_analysis", "risk_assessment"],
            steps=[
                WorkflowStep("s1", "Análisis de inversión", "Evaluar oportunidad",
                            "investment_advisor", "Evalúa: {investment_proposal}", 1),
                WorkflowStep("s2", "Análisis de riesgo", "Evaluar riesgos",
                            "risk_analyst", "Analiza riesgos de inversión", 2, ["s1"])
            ]
        ))
        self.register(WorkflowTemplate(
            workflow_id="fn_tax_planning", name="Planificación Fiscal",
            description="Estrategia de optimización fiscal",
            category="finance", complexity=WorkflowComplexity.EXPERT,
            estimated_time_minutes=90, required_agents=["tax_specialist", "accountant"],
            tags=["tax", "planning", "optimization"], inputs=["company_info", "fiscal_year"],
            outputs=["tax_strategy", "savings_opportunities", "compliance_checklist"],
            steps=[
                WorkflowStep("s1", "Revisión contable", "Analizar situación actual",
                            "accountant", "Revisa: {company_info}", 1),
                WorkflowStep("s2", "Estrategia fiscal", "Planificar optimización",
                            "tax_specialist", "Planifica para: {fiscal_year}", 2, ["s1"])
            ]
        ))
        self.register(WorkflowTemplate(
            workflow_id="fn_audit_prep", name="Preparación de Auditoría",
            description="Preparación completa para auditoría externa",
            category="finance", complexity=WorkflowComplexity.HIGH,
            estimated_time_minutes=120, required_agents=["auditor", "accountant", "financial_controller"],
            tags=["audit", "preparation", "compliance"], inputs=["audit_period"],
            outputs=["audit_package", "documentation", "checklists"],
            steps=[
                WorkflowStep("s1", "Revisión de cuentas", "Verificar registros",
                            "accountant", "Revisa periodo: {audit_period}", 1),
                WorkflowStep("s2", "Pre-auditoría", "Simular auditoría",
                            "auditor", "Ejecuta pre-auditoría", 2, ["s1"]),
                WorkflowStep("s3", "Validación", "Aprobar documentación",
                            "financial_controller", "Valida paquete", 3, ["s2"])
            ]
        ))

    def _register_legal_workflows(self):
        """5 workflows legales"""
        self.register(WorkflowTemplate(
            workflow_id="lg_contract_review", name="Revisión de Contrato",
            description="Revisión legal exhaustiva de contrato comercial",
            category="legal", complexity=WorkflowComplexity.HIGH,
            estimated_time_minutes=60, required_agents=["contract_specialist", "corporate_lawyer"],
            tags=["contract", "review", "legal"], inputs=["contract_document"],
            outputs=["review_report", "redlines", "recommendations"],
            steps=[
                WorkflowStep("s1", "Análisis de cláusulas", "Revisar términos",
                            "contract_specialist", "Revisa: {contract_document}", 1),
                WorkflowStep("s2", "Validación corporativa", "Verificar cumplimiento",
                            "corporate_lawyer", "Valida contrato", 2, ["s1"])
            ]
        ))
        self.register(WorkflowTemplate(
            workflow_id="lg_compliance_audit", name="Auditoría de Compliance",
            description="Evaluación de cumplimiento normativo",
            category="legal", complexity=WorkflowComplexity.HIGH,
            estimated_time_minutes=90, required_agents=["compliance_officer", "regulatory_advisor"],
            tags=["compliance", "audit", "regulatory"], inputs=["company_area"],
            outputs=["compliance_report", "gaps", "action_plan"],
            steps=[
                WorkflowStep("s1", "Evaluación regulatoria", "Revisar requisitos",
                            "regulatory_advisor", "Evalúa requisitos para: {company_area}", 1),
                WorkflowStep("s2", "Auditoría de cumplimiento", "Verificar cumplimiento",
                            "compliance_officer", "Audita cumplimiento", 2, ["s1"])
            ]
        ))
        self.register(WorkflowTemplate(
            workflow_id="lg_ip_protection", name="Protección de Propiedad Intelectual",
            description="Estrategia de protección de PI",
            category="legal", complexity=WorkflowComplexity.EXPERT,
            estimated_time_minutes=90, required_agents=["intellectual_property", "corporate_lawyer"],
            tags=["ip", "patents", "trademarks"], inputs=["intellectual_assets"],
            outputs=["ip_strategy", "registration_plan", "protection_measures"],
            steps=[
                WorkflowStep("s1", "Inventario de PI", "Identificar activos",
                            "intellectual_property", "Analiza: {intellectual_assets}", 1),
                WorkflowStep("s2", "Estrategia legal", "Planificar protección",
                            "corporate_lawyer", "Define estrategia", 2, ["s1"])
            ]
        ))
        self.register(WorkflowTemplate(
            workflow_id="lg_privacy_assessment", name="Evaluación de Privacidad",
            description="DPIA y evaluación de cumplimiento de privacidad",
            category="legal", complexity=WorkflowComplexity.HIGH,
            estimated_time_minutes=90, required_agents=["data_privacy_officer", "compliance_officer"],
            tags=["privacy", "gdpr", "dpia"], inputs=["data_processing_activities"],
            outputs=["dpia_report", "risk_assessment", "recommendations"],
            steps=[
                WorkflowStep("s1", "Mapeo de datos", "Identificar tratamientos",
                            "data_privacy_officer", "Mapea: {data_processing_activities}", 1),
                WorkflowStep("s2", "Evaluación de riesgos", "Analizar riesgos",
                            "compliance_officer", "Evalúa riesgos de privacidad", 2, ["s1"])
            ]
        ))
        self.register(WorkflowTemplate(
            workflow_id="lg_labor_issue", name="Gestión de Caso Laboral",
            description="Manejo de situación laboral compleja",
            category="legal", complexity=WorkflowComplexity.HIGH,
            estimated_time_minutes=60, required_agents=["labor_law_expert", "litigation_specialist"],
            tags=["labor", "employment", "dispute"], inputs=["case_details"],
            outputs=["legal_opinion", "strategy", "documentation"],
            steps=[
                WorkflowStep("s1", "Análisis del caso", "Evaluar situación",
                            "labor_law_expert", "Analiza: {case_details}", 1),
                WorkflowStep("s2", "Estrategia de litigio", "Preparar defensa",
                            "litigation_specialist", "Define estrategia", 2, ["s1"])
            ]
        ))

    def _register_hr_workflows(self):
        """5 workflows de recursos humanos"""
        self.register(WorkflowTemplate(
            workflow_id="hr_hiring_process", name="Proceso de Contratación",
            description="Proceso completo de reclutamiento y selección",
            category="human_resources", complexity=WorkflowComplexity.MEDIUM,
            estimated_time_minutes=90, required_agents=["recruiter", "talent_development"],
            tags=["hiring", "recruitment", "selection"], inputs=["job_description", "requirements"],
            outputs=["job_posting", "interview_guide", "evaluation_matrix"],
            steps=[
                WorkflowStep("s1", "Diseño de puesto", "Definir perfil",
                            "recruiter", "Diseña puesto: {job_description}", 1),
                WorkflowStep("s2", "Plan de evaluación", "Definir criterios",
                            "talent_development", "Evalúa competencias: {requirements}", 2, ["s1"])
            ]
        ))
        self.register(WorkflowTemplate(
            workflow_id="hr_onboarding", name="Programa de Onboarding",
            description="Diseño de programa de incorporación de nuevos empleados",
            category="human_resources", complexity=WorkflowComplexity.MEDIUM,
            estimated_time_minutes=60, required_agents=["onboarding_specialist", "training_coordinator"],
            tags=["onboarding", "new hire", "integration"], inputs=["role", "department"],
            outputs=["onboarding_plan", "checklist", "training_schedule"],
            steps=[
                WorkflowStep("s1", "Plan de onboarding", "Diseñar programa",
                            "onboarding_specialist", "Diseña para: {role}", 1),
                WorkflowStep("s2", "Calendario de training", "Planificar capacitación",
                            "training_coordinator", "Coordina para: {department}", 2, ["s1"])
            ]
        ))
        self.register(WorkflowTemplate(
            workflow_id="hr_performance_cycle", name="Ciclo de Evaluación de Desempeño",
            description="Gestión del ciclo de evaluación de desempeño",
            category="human_resources", complexity=WorkflowComplexity.MEDIUM,
            estimated_time_minutes=45, required_agents=["performance_manager", "hr_analytics"],
            tags=["performance", "evaluation", "reviews"], inputs=["evaluation_period"],
            outputs=["evaluation_templates", "calibration_guide", "reports"],
            steps=[
                WorkflowStep("s1", "Diseño de evaluación", "Configurar ciclo",
                            "performance_manager", "Configura para: {evaluation_period}", 1),
                WorkflowStep("s2", "Análisis de datos", "Preparar analytics",
                            "hr_analytics", "Prepara métricas", 2, ["s1"])
            ]
        ))
        self.register(WorkflowTemplate(
            workflow_id="hr_compensation_review", name="Revisión de Compensaciones",
            description="Análisis y ajuste de estructura de compensaciones",
            category="human_resources", complexity=WorkflowComplexity.HIGH,
            estimated_time_minutes=90, required_agents=["compensation_analyst", "hr_analytics"],
            tags=["compensation", "salary", "benefits"], inputs=["market_data"],
            outputs=["compensation_analysis", "recommendations", "budget_impact"],
            steps=[
                WorkflowStep("s1", "Análisis de mercado", "Comparar compensaciones",
                            "compensation_analyst", "Analiza mercado: {market_data}", 1),
                WorkflowStep("s2", "Impacto financiero", "Calcular impacto",
                            "hr_analytics", "Calcula impacto", 2, ["s1"])
            ]
        ))
        self.register(WorkflowTemplate(
            workflow_id="hr_culture_initiative", name="Iniciativa de Cultura",
            description="Diseño de programa de cultura organizacional",
            category="human_resources", complexity=WorkflowComplexity.MEDIUM,
            estimated_time_minutes=60, required_agents=["culture_champion", "employee_relations"],
            tags=["culture", "engagement", "dei"], inputs=["culture_goals"],
            outputs=["culture_program", "activities", "metrics"],
            steps=[
                WorkflowStep("s1", "Diseño de programa", "Planificar iniciativa",
                            "culture_champion", "Diseña para: {culture_goals}", 1),
                WorkflowStep("s2", "Plan de engagement", "Involucrar empleados",
                            "employee_relations", "Planifica engagement", 2, ["s1"])
            ]
        ))

    def _register_sales_workflows(self):
        """5 workflows de ventas"""
        self.register(WorkflowTemplate(
            workflow_id="sl_sales_process", name="Proceso de Ventas B2B",
            description="Gestión de oportunidad de venta enterprise",
            category="sales", complexity=WorkflowComplexity.HIGH,
            estimated_time_minutes=60, required_agents=["sales_executive", "sales_engineer"],
            tags=["sales", "b2b", "enterprise"], inputs=["opportunity", "prospect"],
            outputs=["sales_strategy", "proposal_outline", "demo_plan"],
            steps=[
                WorkflowStep("s1", "Estrategia de venta", "Definir approach",
                            "sales_executive", "Estrategia para: {opportunity}", 1),
                WorkflowStep("s2", "Preparación técnica", "Planificar demo",
                            "sales_engineer", "Prepara demo para: {prospect}", 2, ["s1"])
            ]
        ))
        self.register(WorkflowTemplate(
            workflow_id="sl_proposal_creation", name="Creación de Propuesta",
            description="Desarrollo de propuesta comercial profesional",
            category="sales", complexity=WorkflowComplexity.MEDIUM,
            estimated_time_minutes=90, required_agents=["proposal_writer", "sales_executive"],
            tags=["proposal", "quote", "rfp"], inputs=["requirements", "pricing"],
            outputs=["proposal_document", "pricing_table", "executive_summary"],
            steps=[
                WorkflowStep("s1", "Estrategia de propuesta", "Definir win themes",
                            "sales_executive", "Define estrategia: {requirements}", 1),
                WorkflowStep("s2", "Redacción de propuesta", "Escribir propuesta",
                            "proposal_writer", "Redacta con pricing: {pricing}", 2, ["s1"])
            ]
        ))
        self.register(WorkflowTemplate(
            workflow_id="sl_account_plan", name="Plan de Cuenta",
            description="Planificación estratégica de cuenta clave",
            category="sales", complexity=WorkflowComplexity.HIGH,
            estimated_time_minutes=60, required_agents=["account_manager", "customer_success"],
            tags=["account", "planning", "key account"], inputs=["account_info"],
            outputs=["account_plan", "growth_strategy", "risk_mitigation"],
            steps=[
                WorkflowStep("s1", "Análisis de cuenta", "Evaluar oportunidades",
                            "account_manager", "Analiza: {account_info}", 1),
                WorkflowStep("s2", "Plan de éxito", "Asegurar retención",
                            "customer_success", "Define plan de éxito", 2, ["s1"])
            ]
        ))
        self.register(WorkflowTemplate(
            workflow_id="sl_pipeline_review", name="Revisión de Pipeline",
            description="Análisis y optimización del pipeline de ventas",
            category="sales", complexity=WorkflowComplexity.MEDIUM,
            estimated_time_minutes=45, required_agents=["sales_analyst", "sales_executive"],
            tags=["pipeline", "forecast", "analysis"], inputs=["pipeline_data"],
            outputs=["pipeline_report", "forecast", "recommendations"],
            steps=[
                WorkflowStep("s1", "Análisis de pipeline", "Revisar oportunidades",
                            "sales_analyst", "Analiza: {pipeline_data}", 1),
                WorkflowStep("s2", "Recomendaciones", "Acciones prioritarias",
                            "sales_executive", "Define acciones", 2, ["s1"])
            ]
        ))
        self.register(WorkflowTemplate(
            workflow_id="sl_channel_strategy", name="Estrategia de Canales",
            description="Desarrollo de estrategia de partners y canales",
            category="sales", complexity=WorkflowComplexity.HIGH,
            estimated_time_minutes=90, required_agents=["channel_manager", "business_development"],
            tags=["channel", "partners", "alliances"], inputs=["market", "goals"],
            outputs=["channel_strategy", "partner_program", "incentives"],
            steps=[
                WorkflowStep("s1", "Análisis de mercado", "Identificar oportunidades",
                            "business_development", "Analiza: {market}", 1),
                WorkflowStep("s2", "Diseño de programa", "Crear programa de partners",
                            "channel_manager", "Diseña para: {goals}", 2, ["s1"])
            ]
        ))

    def _register_operations_workflows(self):
        """5 workflows de operaciones"""
        self.register(WorkflowTemplate(
            workflow_id="op_process_improvement", name="Mejora de Procesos",
            description="Análisis y optimización de procesos operativos",
            category="operations", complexity=WorkflowComplexity.HIGH,
            estimated_time_minutes=90, required_agents=["process_optimizer", "lean_specialist"],
            tags=["process", "improvement", "lean"], inputs=["process_name", "current_state"],
            outputs=["process_analysis", "recommendations", "implementation_plan"],
            steps=[
                WorkflowStep("s1", "Mapeo de proceso", "Documentar estado actual",
                            "process_optimizer", "Mapea: {process_name}", 1),
                WorkflowStep("s2", "Análisis Lean", "Identificar desperdicios",
                            "lean_specialist", "Analiza: {current_state}", 2, ["s1"])
            ]
        ))
        self.register(WorkflowTemplate(
            workflow_id="op_supply_chain_opt", name="Optimización de Supply Chain",
            description="Análisis y mejora de cadena de suministro",
            category="operations", complexity=WorkflowComplexity.HIGH,
            estimated_time_minutes=120, required_agents=["supply_chain_analyst", "logistics_coordinator"],
            tags=["supply chain", "logistics", "optimization"], inputs=["supply_chain_data"],
            outputs=["optimization_report", "cost_savings", "action_plan"],
            steps=[
                WorkflowStep("s1", "Análisis de cadena", "Evaluar supply chain",
                            "supply_chain_analyst", "Analiza: {supply_chain_data}", 1),
                WorkflowStep("s2", "Optimización logística", "Mejorar flujos",
                            "logistics_coordinator", "Optimiza logística", 2, ["s1"])
            ]
        ))
        self.register(WorkflowTemplate(
            workflow_id="op_inventory_opt", name="Optimización de Inventario",
            description="Análisis y optimización de niveles de inventario",
            category="operations", complexity=WorkflowComplexity.MEDIUM,
            estimated_time_minutes=60, required_agents=["inventory_specialist", "warehouse_manager"],
            tags=["inventory", "stock", "optimization"], inputs=["inventory_data"],
            outputs=["inventory_analysis", "reorder_points", "recommendations"],
            steps=[
                WorkflowStep("s1", "Análisis de inventario", "Revisar niveles",
                            "inventory_specialist", "Analiza: {inventory_data}", 1),
                WorkflowStep("s2", "Optimización de almacén", "Mejorar layout",
                            "warehouse_manager", "Optimiza almacenamiento", 2, ["s1"])
            ]
        ))
        self.register(WorkflowTemplate(
            workflow_id="op_quality_system", name="Sistema de Calidad",
            description="Implementación de sistema de gestión de calidad",
            category="operations", complexity=WorkflowComplexity.HIGH,
            estimated_time_minutes=120, required_agents=["quality_assurance_ops", "process_optimizer"],
            tags=["quality", "iso", "management"], inputs=["scope", "standards"],
            outputs=["quality_manual", "procedures", "implementation_plan"],
            steps=[
                WorkflowStep("s1", "Diseño de SGC", "Definir sistema",
                            "quality_assurance_ops", "Diseña para: {scope}", 1),
                WorkflowStep("s2", "Documentación", "Crear procedimientos",
                            "process_optimizer", "Documenta: {standards}", 2, ["s1"])
            ]
        ))
        self.register(WorkflowTemplate(
            workflow_id="op_vendor_evaluation", name="Evaluación de Proveedores",
            description="Evaluación y selección de proveedores",
            category="operations", complexity=WorkflowComplexity.MEDIUM,
            estimated_time_minutes=60, required_agents=["procurement_specialist", "quality_assurance_ops"],
            tags=["vendor", "procurement", "evaluation"], inputs=["vendor_list", "criteria"],
            outputs=["evaluation_report", "scorecard", "recommendations"],
            steps=[
                WorkflowStep("s1", "Evaluación comercial", "Analizar propuestas",
                            "procurement_specialist", "Evalúa: {vendor_list}", 1),
                WorkflowStep("s2", "Evaluación de calidad", "Verificar calidad",
                            "quality_assurance_ops", "Valida con: {criteria}", 2, ["s1"])
            ]
        ))

    def _register_education_workflows(self):
        """5 workflows de educación"""
        self.register(WorkflowTemplate(
            workflow_id="ed_course_design", name="Diseño de Curso",
            description="Diseño instruccional completo de curso",
            category="education", complexity=WorkflowComplexity.HIGH,
            estimated_time_minutes=120, required_agents=["instructional_designer", "curriculum_developer"],
            tags=["course", "design", "instructional"], inputs=["topic", "audience", "duration"],
            outputs=["course_outline", "learning_objectives", "activities"],
            steps=[
                WorkflowStep("s1", "Diseño curricular", "Definir estructura",
                            "curriculum_developer", "Diseña para: {topic}", 1),
                WorkflowStep("s2", "Diseño instruccional", "Crear actividades",
                            "instructional_designer", "Diseña para: {audience}", 2, ["s1"])
            ]
        ))
        self.register(WorkflowTemplate(
            workflow_id="ed_elearning_module", name="Módulo E-Learning",
            description="Desarrollo de módulo de e-learning interactivo",
            category="education", complexity=WorkflowComplexity.MEDIUM,
            estimated_time_minutes=90, required_agents=["elearning_specialist", "instructional_designer"],
            tags=["elearning", "module", "interactive"], inputs=["content", "platform"],
            outputs=["storyboard", "script", "technical_specs"],
            steps=[
                WorkflowStep("s1", "Diseño instruccional", "Crear guión",
                            "instructional_designer", "Diseña para: {content}", 1),
                WorkflowStep("s2", "Desarrollo e-learning", "Especificar técnico",
                            "elearning_specialist", "Desarrolla para: {platform}", 2, ["s1"])
            ]
        ))
        self.register(WorkflowTemplate(
            workflow_id="ed_training_program", name="Programa de Capacitación",
            description="Diseño de programa de capacitación corporativa",
            category="education", complexity=WorkflowComplexity.HIGH,
            estimated_time_minutes=90, required_agents=["training_facilitator", "learning_analyst"],
            tags=["training", "corporate", "program"], inputs=["skills", "target_group"],
            outputs=["training_program", "materials", "evaluation_plan"],
            steps=[
                WorkflowStep("s1", "Diseño de programa", "Planificar capacitación",
                            "training_facilitator", "Diseña para: {skills}", 1),
                WorkflowStep("s2", "Métricas de evaluación", "Definir KPIs",
                            "learning_analyst", "Define métricas para: {target_group}", 2, ["s1"])
            ]
        ))
        self.register(WorkflowTemplate(
            workflow_id="ed_assessment_design", name="Diseño de Evaluación",
            description="Diseño de sistema de evaluación del aprendizaje",
            category="education", complexity=WorkflowComplexity.MEDIUM,
            estimated_time_minutes=60, required_agents=["assessment_specialist", "instructional_designer"],
            tags=["assessment", "evaluation", "testing"], inputs=["learning_objectives"],
            outputs=["assessment_blueprint", "rubrics", "item_bank"],
            steps=[
                WorkflowStep("s1", "Blueprint de evaluación", "Diseñar estructura",
                            "assessment_specialist", "Diseña para: {learning_objectives}", 1),
                WorkflowStep("s2", "Alineación instruccional", "Validar alineación",
                            "instructional_designer", "Valida diseño", 2, ["s1"])
            ]
        ))
        self.register(WorkflowTemplate(
            workflow_id="ed_learning_path", name="Ruta de Aprendizaje",
            description="Diseño de learning path personalizado",
            category="education", complexity=WorkflowComplexity.MEDIUM,
            estimated_time_minutes=45, required_agents=["content_curator", "curriculum_developer"],
            tags=["learning path", "personalized", "curation"], inputs=["role", "skill_gaps"],
            outputs=["learning_path", "resources", "milestones"],
            steps=[
                WorkflowStep("s1", "Diseño de ruta", "Estructurar path",
                            "curriculum_developer", "Diseña para: {role}", 1),
                WorkflowStep("s2", "Curación de contenido", "Seleccionar recursos",
                            "content_curator", "Cura para: {skill_gaps}", 2, ["s1"])
            ]
        ))

    def _register_creative_workflows(self):
        """5 workflows creativos"""
        self.register(WorkflowTemplate(
            workflow_id="cr_brand_identity", name="Identidad de Marca",
            description="Desarrollo de identidad visual de marca",
            category="creative", complexity=WorkflowComplexity.HIGH,
            estimated_time_minutes=120, required_agents=["brand_designer", "creative_director"],
            tags=["brand", "identity", "visual"], inputs=["company", "values", "industry"],
            outputs=["brand_guidelines", "logo_variations", "color_palette"],
            steps=[
                WorkflowStep("s1", "Dirección creativa", "Definir concepto",
                            "creative_director", "Conceptualiza para: {company}", 1),
                WorkflowStep("s2", "Diseño de identidad", "Crear elementos",
                            "brand_designer", "Diseña para: {industry}", 2, ["s1"])
            ]
        ))
        self.register(WorkflowTemplate(
            workflow_id="cr_ux_redesign", name="Rediseño UX",
            description="Rediseño de experiencia de usuario de producto digital",
            category="creative", complexity=WorkflowComplexity.HIGH,
            estimated_time_minutes=120, required_agents=["ux_designer", "ui_designer"],
            tags=["ux", "redesign", "product"], inputs=["product", "pain_points"],
            outputs=["wireframes", "user_flows", "ui_mockups"],
            steps=[
                WorkflowStep("s1", "Research y UX", "Diseñar experiencia",
                            "ux_designer", "Rediseña: {product}", 1),
                WorkflowStep("s2", "Diseño UI", "Crear interfaces",
                            "ui_designer", "Diseña para: {pain_points}", 2, ["s1"])
            ]
        ))
        self.register(WorkflowTemplate(
            workflow_id="cr_video_campaign", name="Campaña de Video",
            description="Producción de campaña de video marketing",
            category="creative", complexity=WorkflowComplexity.HIGH,
            estimated_time_minutes=90, required_agents=["video_producer", "motion_designer"],
            tags=["video", "campaign", "production"], inputs=["message", "platforms"],
            outputs=["video_script", "storyboard", "motion_assets"],
            steps=[
                WorkflowStep("s1", "Producción de video", "Planificar producción",
                            "video_producer", "Produce para: {message}", 1),
                WorkflowStep("s2", "Motion graphics", "Crear animaciones",
                            "motion_designer", "Anima para: {platforms}", 2, ["s1"])
            ]
        ))
        self.register(WorkflowTemplate(
            workflow_id="cr_illustration_set", name="Set de Ilustraciones",
            description="Creación de set de ilustraciones personalizadas",
            category="creative", complexity=WorkflowComplexity.MEDIUM,
            estimated_time_minutes=60, required_agents=["illustrator", "creative_director"],
            tags=["illustration", "custom", "visual"], inputs=["style", "use_cases"],
            outputs=["illustration_set", "style_guide", "variations"],
            steps=[
                WorkflowStep("s1", "Dirección artística", "Definir estilo",
                            "creative_director", "Define estilo: {style}", 1),
                WorkflowStep("s2", "Ilustración", "Crear ilustraciones",
                            "illustrator", "Ilustra para: {use_cases}", 2, ["s1"])
            ]
        ))
        self.register(WorkflowTemplate(
            workflow_id="cr_3d_visualization", name="Visualización 3D",
            description="Creación de visualización 3D de producto",
            category="creative", complexity=WorkflowComplexity.HIGH,
            estimated_time_minutes=90, required_agents=["three_d_artist", "creative_director"],
            tags=["3d", "visualization", "product"], inputs=["product_specs", "angles"],
            outputs=["3d_renders", "animations", "materials"],
            steps=[
                WorkflowStep("s1", "Dirección visual", "Definir visualización",
                            "creative_director", "Dirige para: {product_specs}", 1),
                WorkflowStep("s2", "Modelado 3D", "Crear visualización",
                            "three_d_artist", "Modela: {angles}", 2, ["s1"])
            ]
        ))

    def _register_pm_workflows(self):
        """5 workflows de gestión de proyectos"""
        self.register(WorkflowTemplate(
            workflow_id="pm_project_kickoff", name="Kickoff de Proyecto",
            description="Planificación y lanzamiento de proyecto",
            category="project_management", complexity=WorkflowComplexity.MEDIUM,
            estimated_time_minutes=60, required_agents=["project_manager", "stakeholder_manager"],
            tags=["kickoff", "planning", "launch"], inputs=["project_scope", "stakeholders"],
            outputs=["project_charter", "stakeholder_register", "kickoff_deck"],
            steps=[
                WorkflowStep("s1", "Planificación", "Crear plan de proyecto",
                            "project_manager", "Planifica: {project_scope}", 1),
                WorkflowStep("s2", "Gestión de stakeholders", "Mapear interesados",
                            "stakeholder_manager", "Gestiona: {stakeholders}", 2, ["s1"])
            ]
        ))
        self.register(WorkflowTemplate(
            workflow_id="pm_agile_setup", name="Setup de Equipo Ágil",
            description="Configuración de equipo y procesos ágiles",
            category="project_management", complexity=WorkflowComplexity.MEDIUM,
            estimated_time_minutes=60, required_agents=["scrum_master", "product_owner"],
            tags=["agile", "scrum", "setup"], inputs=["team", "product"],
            outputs=["team_agreement", "backlog", "ceremonies_calendar"],
            steps=[
                WorkflowStep("s1", "Setup de Scrum", "Configurar framework",
                            "scrum_master", "Configura para: {team}", 1),
                WorkflowStep("s2", "Backlog inicial", "Crear backlog",
                            "product_owner", "Define backlog para: {product}", 2, ["s1"])
            ]
        ))
        self.register(WorkflowTemplate(
            workflow_id="pm_change_initiative", name="Iniciativa de Cambio",
            description="Gestión de iniciativa de cambio organizacional",
            category="project_management", complexity=WorkflowComplexity.HIGH,
            estimated_time_minutes=90, required_agents=["change_manager", "program_manager"],
            tags=["change", "transformation", "organizational"], inputs=["change_scope", "impact"],
            outputs=["change_plan", "communication_plan", "training_plan"],
            steps=[
                WorkflowStep("s1", "Planificación de programa", "Estructurar iniciativa",
                            "program_manager", "Planifica: {change_scope}", 1),
                WorkflowStep("s2", "Gestión del cambio", "Planificar adopción",
                            "change_manager", "Gestiona impacto: {impact}", 2, ["s1"])
            ]
        ))
        self.register(WorkflowTemplate(
            workflow_id="pm_portfolio_review", name="Revisión de Portafolio",
            description="Análisis y priorización de portafolio de proyectos",
            category="project_management", complexity=WorkflowComplexity.HIGH,
            estimated_time_minutes=90, required_agents=["portfolio_manager", "resource_planner"],
            tags=["portfolio", "prioritization", "strategic"], inputs=["portfolio_data"],
            outputs=["portfolio_analysis", "prioritization", "resource_plan"],
            steps=[
                WorkflowStep("s1", "Análisis de portafolio", "Evaluar proyectos",
                            "portfolio_manager", "Analiza: {portfolio_data}", 1),
                WorkflowStep("s2", "Planificación de recursos", "Asignar recursos",
                            "resource_planner", "Planifica recursos", 2, ["s1"])
            ]
        ))
        self.register(WorkflowTemplate(
            workflow_id="pm_pmo_implementation", name="Implementación de PMO",
            description="Diseño e implementación de oficina de proyectos",
            category="project_management", complexity=WorkflowComplexity.EXPERT,
            estimated_time_minutes=120, required_agents=["pmo_specialist", "agile_coach"],
            tags=["pmo", "implementation", "governance"], inputs=["organization", "maturity"],
            outputs=["pmo_charter", "methodology", "governance_framework"],
            steps=[
                WorkflowStep("s1", "Diseño de PMO", "Definir estructura",
                            "pmo_specialist", "Diseña para: {organization}", 1),
                WorkflowStep("s2", "Metodología ágil", "Integrar agilidad",
                            "agile_coach", "Integra para: {maturity}", 2, ["s1"])
            ]
        ))


# Singleton instance
workflow_registry = WorkflowRegistry()

def get_workflow(workflow_id: str) -> Optional[WorkflowTemplate]:
    """Obtiene un workflow por ID"""
    return workflow_registry.get(workflow_id)

def get_workflows_by_category(category: str) -> List[WorkflowTemplate]:
    """Obtiene workflows por categoría"""
    return workflow_registry.get_by_category(category)
