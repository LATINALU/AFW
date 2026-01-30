"""
AFW v1.0.0 - Agents For Work | Response Format Templates
Sistema de 10 formatos de respuesta especializados por categoría de agente
Paletas de colores profesionales inspiradas en Radix Colors y Catppuccin
"""

from typing import Dict, Any, List, Optional
from dataclasses import dataclass
from enum import Enum

class ResponseType(Enum):
    """Tipos de formato de respuesta"""
    CODE = "code"                    # Para agentes de desarrollo
    DOCUMENT = "document"            # Para agentes legales/documentación
    ANALYSIS = "analysis"            # Para agentes analíticos/financieros  
    CREATIVE = "creative"            # Para agentes creativos/marketing
    STRATEGIC = "strategic"          # Para agentes de gestión/estrategia
    EDUCATIONAL = "educational"      # Para agentes educativos
    MARKETPLACE = "marketplace"      # Para agentes de ML/YouTube
    OPERATIONAL = "operational"      # Para agentes de operaciones
    HR = "hr"                        # Para agentes de RRHH
    SALES = "sales"                  # Para agentes de ventas

@dataclass
class ResponseSection:
    """Define una sección de respuesta"""
    id: str
    title: str
    emoji: str
    required: bool = True
    min_words: int = 50

@dataclass 
class ResponseFormat:
    """Formato de respuesta para un tipo de agente"""
    type: ResponseType
    name: str
    description: str
    min_total_words: int
    sections: List[ResponseSection]
    formatting: Dict[str, bool]
    template: str
    color_scheme: str


# ============================================================================
# DEFINICIONES DE FORMATOS POR TIPO
# ============================================================================

RESPONSE_FORMATS: Dict[str, ResponseFormat] = {
    
    # =========================================================================
    # 💻 SOFTWARE DEVELOPMENT FORMAT
    # =========================================================================
    "code": ResponseFormat(
        type=ResponseType.CODE,
        name="Código y Desarrollo",
        description="Formato especializado para respuestas técnicas con código",
        min_total_words=800,
        sections=[
            ResponseSection("context", "🔍 Contexto y Análisis", "🔍", True, 100),
            ResponseSection("solution", "💡 Solución Propuesta", "💡", True, 150),
            ResponseSection("implementation", "⚙️ Implementación", "⚙️", True, 200),
            ResponseSection("code", "💻 Código", "💻", True, 100),
            ResponseSection("best_practices", "✅ Mejores Prácticas", "✅", True, 100),
            ResponseSection("testing", "🧪 Testing", "🧪", False, 80),
            ResponseSection("next_steps", "🚀 Próximos Pasos", "🚀", True, 50),
        ],
        formatting={
            "code_blocks": True,
            "syntax_highlighting": True,
            "tables": True,
            "lists": True,
            "diagrams": False,
            "file_tree": True
        },
        template="""
## 🔍 Contexto y Análisis

{context_analysis}

## 💡 Solución Propuesta

{solution_description}

## ⚙️ Implementación Detallada

{implementation_details}

## 💻 Código

```{language}
{code}
```

### Explicación del Código:
{code_explanation}

## ✅ Mejores Prácticas Aplicadas

{best_practices}

## 🧪 Consideraciones de Testing

{testing_notes}

## 🚀 Próximos Pasos Recomendados

{next_steps}

---
📌 **Notas Adicionales:** {additional_notes}
""",
        color_scheme="sky"
    ),

    # =========================================================================
    # 📄 DOCUMENT FORMAT (Legal, Contracts)
    # =========================================================================
    "document": ResponseFormat(
        type=ResponseType.DOCUMENT,
        name="Documento Legal/Formal",
        description="Formato estructurado para documentos legales y formales",
        min_total_words=1000,
        sections=[
            ResponseSection("header", "📋 Encabezado", "📋", True, 50),
            ResponseSection("background", "📌 Antecedentes", "📌", True, 150),
            ResponseSection("analysis", "⚖️ Análisis Legal", "⚖️", True, 250),
            ResponseSection("considerations", "🔍 Consideraciones", "🔍", True, 150),
            ResponseSection("recommendations", "✅ Recomendaciones", "✅", True, 200),
            ResponseSection("risks", "⚠️ Riesgos", "⚠️", True, 100),
            ResponseSection("conclusion", "📝 Conclusión", "📝", True, 100),
        ],
        formatting={
            "code_blocks": False,
            "syntax_highlighting": False,
            "tables": True,
            "lists": True,
            "numbered_sections": True,
            "formal_headers": True
        },
        template="""
# 📋 {document_title}

**Fecha:** {date}  
**Referencia:** {reference}  
**Clasificación:** {classification}

---

## 1. 📌 ANTECEDENTES

{background}

## 2. ⚖️ ANÁLISIS LEGAL

### 2.1 Marco Normativo Aplicable
{legal_framework}

### 2.2 Análisis de la Situación
{situation_analysis}

### 2.3 Jurisprudencia Relevante
{jurisprudence}

## 3. 🔍 CONSIDERACIONES IMPORTANTES

{considerations}

## 4. ⚠️ RIESGOS IDENTIFICADOS

| Riesgo | Probabilidad | Impacto | Mitigación |
|--------|--------------|---------|------------|
{risks_table}

## 5. ✅ RECOMENDACIONES

{recommendations}

## 6. 📝 CONCLUSIÓN

{conclusion}

---

**Disclaimer:** {disclaimer}
""",
        color_scheme="violet"
    ),

    # =========================================================================
    # 📊 ANALYSIS FORMAT (Finance, Data, Research)
    # =========================================================================
    "analysis": ResponseFormat(
        type=ResponseType.ANALYSIS,
        name="Análisis Profesional",
        description="Formato para análisis financieros, de datos e investigación",
        min_total_words=1200,
        sections=[
            ResponseSection("executive_summary", "📊 Resumen Ejecutivo", "📊", True, 150),
            ResponseSection("methodology", "🔬 Metodología", "🔬", True, 100),
            ResponseSection("data_analysis", "📈 Análisis de Datos", "📈", True, 300),
            ResponseSection("findings", "🔍 Hallazgos Clave", "🔍", True, 200),
            ResponseSection("insights", "💡 Insights", "💡", True, 150),
            ResponseSection("recommendations", "✅ Recomendaciones", "✅", True, 150),
            ResponseSection("appendix", "📎 Anexos", "📎", False, 50),
        ],
        formatting={
            "code_blocks": True,
            "syntax_highlighting": True,
            "tables": True,
            "lists": True,
            "charts_description": True,
            "metrics_boxes": True
        },
        template="""
# 📊 ANÁLISIS: {title}

## Resumen Ejecutivo

> {executive_summary}

---

## 🔬 Metodología

{methodology}

## 📈 Análisis de Datos

### Métricas Clave

| Métrica | Valor Actual | Benchmark | Variación |
|---------|--------------|-----------|-----------|
{metrics_table}

### Análisis Detallado

{detailed_analysis}

### Tendencias Identificadas

{trends}

## 🔍 Hallazgos Clave

{findings}

## 💡 Insights Estratégicos

{insights}

## ✅ Recomendaciones

### Corto Plazo (0-30 días)
{short_term}

### Mediano Plazo (30-90 días)
{medium_term}

### Largo Plazo (90+ días)
{long_term}

## ⚠️ Riesgos y Consideraciones

{risks}

---

**Fuentes:** {sources}
**Fecha de Análisis:** {date}
""",
        color_scheme="green"
    ),

    # =========================================================================
    # 🎨 CREATIVE FORMAT (Marketing, Design, Content)
    # =========================================================================
    "creative": ResponseFormat(
        type=ResponseType.CREATIVE,
        name="Creativo y Marketing",
        description="Formato para contenido creativo, marketing y diseño",
        min_total_words=800,
        sections=[
            ResponseSection("concept", "💡 Concepto", "💡", True, 100),
            ResponseSection("strategy", "🎯 Estrategia", "🎯", True, 150),
            ResponseSection("execution", "🚀 Ejecución", "🚀", True, 200),
            ResponseSection("content", "✍️ Contenido", "✍️", True, 200),
            ResponseSection("channels", "📱 Canales", "📱", True, 100),
            ResponseSection("metrics", "📊 Métricas", "📊", True, 50),
        ],
        formatting={
            "code_blocks": False,
            "syntax_highlighting": False,
            "tables": True,
            "lists": True,
            "quotes": True,
            "call_to_action": True
        },
        template="""
# 🎨 {project_title}

## 💡 Concepto Creativo

> *"{tagline}"*

{concept_description}

## 🎯 Estrategia

### Objetivo Principal
{main_objective}

### Audiencia Target
{target_audience}

### Propuesta de Valor
{value_proposition}

## 🚀 Plan de Ejecución

### Fase 1: {phase1_name}
{phase1_details}

### Fase 2: {phase2_name}
{phase2_details}

### Fase 3: {phase3_name}
{phase3_details}

## ✍️ Contenido Propuesto

{content_examples}

### Copy Principal
> {main_copy}

### Variaciones
{copy_variations}

## 📱 Canales y Distribución

| Canal | Formato | Frecuencia | Objetivo |
|-------|---------|------------|----------|
{channels_table}

## 📊 KPIs y Métricas

{kpis}

---

🎯 **Call to Action:** {cta}
""",
        color_scheme="fuchsia"
    ),

    # =========================================================================
    # 📋 STRATEGIC FORMAT (Project Management, Strategy)
    # =========================================================================
    "strategic": ResponseFormat(
        type=ResponseType.STRATEGIC,
        name="Estratégico y Gestión",
        description="Formato para planes estratégicos y gestión de proyectos",
        min_total_words=1000,
        sections=[
            ResponseSection("overview", "🎯 Visión General", "🎯", True, 100),
            ResponseSection("objectives", "📌 Objetivos", "📌", True, 150),
            ResponseSection("action_plan", "📋 Plan de Acción", "📋", True, 300),
            ResponseSection("resources", "👥 Recursos", "👥", True, 100),
            ResponseSection("timeline", "📅 Cronograma", "📅", True, 100),
            ResponseSection("risks", "⚠️ Riesgos", "⚠️", True, 100),
            ResponseSection("success_criteria", "✅ Criterios de Éxito", "✅", True, 100),
        ],
        formatting={
            "code_blocks": False,
            "syntax_highlighting": False,
            "tables": True,
            "lists": True,
            "gantt_description": True,
            "milestones": True
        },
        template="""
# 📋 PLAN: {plan_title}

## 🎯 Visión General

{overview}

### Alcance
{scope}

### Restricciones
{constraints}

## 📌 Objetivos SMART

| # | Objetivo | Específico | Medible | Alcanzable | Relevante | Temporal |
|---|----------|------------|---------|------------|-----------|----------|
{objectives_table}

## 📋 Plan de Acción Detallado

### Fase 1: {phase1_name}
**Duración:** {phase1_duration}

| Actividad | Responsable | Entregable | Fecha |
|-----------|-------------|------------|-------|
{phase1_activities}

### Fase 2: {phase2_name}
**Duración:** {phase2_duration}

{phase2_details}

### Fase 3: {phase3_name}
**Duración:** {phase3_duration}

{phase3_details}

## 👥 Recursos Necesarios

### Equipo
{team_resources}

### Presupuesto
{budget}

### Herramientas
{tools}

## 📅 Cronograma (Hitos Principales)

{timeline}

## ⚠️ Gestión de Riesgos

| Riesgo | Probabilidad | Impacto | Plan de Mitigación |
|--------|--------------|---------|-------------------|
{risks_table}

## ✅ Criterios de Éxito

{success_criteria}

---

**Sponsor:** {sponsor}
**PM:** {project_manager}
**Fecha Inicio:** {start_date}
**Fecha Fin Estimada:** {end_date}
""",
        color_scheme="indigo"
    ),

    # =========================================================================
    # 📚 EDUCATIONAL FORMAT
    # =========================================================================
    "educational": ResponseFormat(
        type=ResponseType.EDUCATIONAL,
        name="Educativo",
        description="Formato para contenido educativo y capacitación",
        min_total_words=900,
        sections=[
            ResponseSection("introduction", "📖 Introducción", "📖", True, 100),
            ResponseSection("objectives", "🎯 Objetivos de Aprendizaje", "🎯", True, 80),
            ResponseSection("content", "📚 Contenido", "📚", True, 400),
            ResponseSection("examples", "💡 Ejemplos", "💡", True, 150),
            ResponseSection("practice", "✏️ Ejercicios", "✏️", True, 100),
            ResponseSection("summary", "📝 Resumen", "📝", True, 70),
        ],
        formatting={
            "code_blocks": True,
            "syntax_highlighting": True,
            "tables": True,
            "lists": True,
            "callouts": True,
            "tips": True
        },
        template="""
# 📚 {lesson_title}

## 📖 Introducción

{introduction}

## 🎯 Objetivos de Aprendizaje

Al finalizar, serás capaz de:
{learning_objectives}

---

## 📚 Contenido Principal

### {section1_title}

{section1_content}

> 💡 **Tip:** {tip1}

### {section2_title}

{section2_content}

> ⚠️ **Importante:** {important_note}

### {section3_title}

{section3_content}

## 💡 Ejemplos Prácticos

### Ejemplo 1: {example1_title}
{example1_content}

### Ejemplo 2: {example2_title}
{example2_content}

## ✏️ Ejercicios de Práctica

1. {exercise1}
2. {exercise2}
3. {exercise3}

## 📝 Resumen

{summary}

### Puntos Clave
{key_points}

---

📚 **Recursos Adicionales:** {resources}
""",
        color_scheme="teal"
    ),

    # =========================================================================
    # 🛒 MARKETPLACE FORMAT (Mercado Libre, E-commerce)
    # =========================================================================
    "marketplace": ResponseFormat(
        type=ResponseType.MARKETPLACE,
        name="Marketplace y E-commerce",
        description="Formato especializado para Mercado Libre, YouTube y marketplaces",
        min_total_words=1000,
        sections=[
            ResponseSection("summary", "📊 Resumen", "📊", True, 100),
            ResponseSection("product_info", "📦 Información del Producto", "📦", True, 200),
            ResponseSection("optimization", "✨ Optimización", "✨", True, 200),
            ResponseSection("strategy", "🎯 Estrategia", "🎯", True, 200),
            ResponseSection("metrics", "📈 Métricas", "📈", True, 100),
            ResponseSection("action_plan", "🚀 Plan de Acción", "🚀", True, 150),
        ],
        formatting={
            "code_blocks": False,
            "syntax_highlighting": False,
            "tables": True,
            "lists": True,
            "product_specs": True,
            "pricing_tables": True
        },
        template="""
# 🛒 {title}

## 📊 Resumen Ejecutivo

{executive_summary}

---

## 📦 Ficha de Producto/Canal

### Información Principal
{main_info}

### Especificaciones Técnicas
| Atributo | Valor |
|----------|-------|
{specs_table}

### Keywords Principales
{keywords}

## ✨ Optimización Propuesta

### Título Optimizado
> **{optimized_title}**

### Descripción SEO
{seo_description}

### Atributos Clave
{key_attributes}

### Imágenes Recomendadas
{image_recommendations}

## 🎯 Estrategia de Posicionamiento

### Análisis de Competencia
{competition_analysis}

### Diferenciadores
{differentiators}

### Precio Sugerido
| Estrategia | Precio | Margen |
|------------|--------|--------|
{pricing_table}

## 📈 Métricas Objetivo

| Métrica | Actual | Objetivo | Plazo |
|---------|--------|----------|-------|
{metrics_table}

## 🚀 Plan de Acción (30 días)

### Semana 1
{week1}

### Semana 2
{week2}

### Semana 3
{week3}

### Semana 4
{week4}

---

💰 **ROI Esperado:** {expected_roi}
📅 **Próxima Revisión:** {next_review}
""",
        color_scheme="amber"
    ),

    # =========================================================================
    # ⚙️ OPERATIONAL FORMAT
    # =========================================================================
    "operational": ResponseFormat(
        type=ResponseType.OPERATIONAL,
        name="Operaciones y Logística",
        description="Formato para operaciones, logística y procesos",
        min_total_words=800,
        sections=[
            ResponseSection("situation", "📋 Situación Actual", "📋", True, 100),
            ResponseSection("analysis", "🔍 Análisis", "🔍", True, 200),
            ResponseSection("process", "⚙️ Proceso", "⚙️", True, 200),
            ResponseSection("improvements", "📈 Mejoras", "📈", True, 150),
            ResponseSection("implementation", "🚀 Implementación", "🚀", True, 100),
        ],
        formatting={
            "code_blocks": False,
            "tables": True,
            "lists": True,
            "flowcharts": True,
            "kpis": True
        },
        template="""
# ⚙️ {operation_title}

## 📋 Situación Actual

{current_situation}

### Indicadores Actuales
| KPI | Valor Actual | Target | Gap |
|-----|--------------|--------|-----|
{kpis_table}

## 🔍 Análisis Detallado

### Diagnóstico
{diagnosis}

### Cuellos de Botella
{bottlenecks}

### Oportunidades
{opportunities}

## ⚙️ Proceso Propuesto

### Flujo de Trabajo
{workflow}

### Responsabilidades
{responsibilities}

## 📈 Mejoras Recomendadas

### Quick Wins (0-30 días)
{quick_wins}

### Mejoras Estructurales (30-90 días)
{structural_improvements}

## 🚀 Plan de Implementación

{implementation_plan}

---

📊 **Ahorro Estimado:** {savings}
⏱️ **Tiempo de Implementación:** {implementation_time}
""",
        color_scheme="slate"
    ),

    # =========================================================================
    # 👥 HR FORMAT
    # =========================================================================
    "hr": ResponseFormat(
        type=ResponseType.HR,
        name="Recursos Humanos",
        description="Formato para gestión de talento y RRHH",
        min_total_words=700,
        sections=[
            ResponseSection("overview", "👥 Visión General", "👥", True, 80),
            ResponseSection("analysis", "📊 Análisis", "📊", True, 150),
            ResponseSection("recommendations", "✅ Recomendaciones", "✅", True, 200),
            ResponseSection("action_plan", "📋 Plan de Acción", "📋", True, 150),
            ResponseSection("metrics", "📈 Métricas", "📈", True, 80),
        ],
        formatting={
            "code_blocks": False,
            "tables": True,
            "lists": True,
            "competency_matrices": True
        },
        template="""
# 👥 {hr_title}

## Visión General

{overview}

## 📊 Análisis

{analysis}

### Datos Clave
| Indicador | Valor | Benchmark |
|-----------|-------|-----------|
{data_table}

## ✅ Recomendaciones

{recommendations}

## 📋 Plan de Acción

### Inmediato (0-15 días)
{immediate_actions}

### Corto Plazo (15-30 días)
{short_term_actions}

### Mediano Plazo (30-90 días)
{medium_term_actions}

## 📈 Métricas de Seguimiento

{metrics}

---

🎯 **Impacto Esperado:** {expected_impact}
""",
        color_scheme="orange"
    ),

    # =========================================================================
    # 🤝 SALES FORMAT
    # =========================================================================
    "sales": ResponseFormat(
        type=ResponseType.SALES,
        name="Ventas y Comercial",
        description="Formato para ventas, propuestas y desarrollo de negocios",
        min_total_words=800,
        sections=[
            ResponseSection("opportunity", "💼 Oportunidad", "💼", True, 100),
            ResponseSection("value_prop", "💡 Propuesta de Valor", "💡", True, 150),
            ResponseSection("solution", "🎯 Solución", "🎯", True, 200),
            ResponseSection("roi", "📊 ROI", "📊", True, 100),
            ResponseSection("next_steps", "🚀 Próximos Pasos", "🚀", True, 100),
            ResponseSection("objections", "🛡️ Manejo de Objeciones", "🛡️", True, 100),
        ],
        formatting={
            "code_blocks": False,
            "tables": True,
            "lists": True,
            "pricing_tables": True,
            "comparisons": True
        },
        template="""
# 💼 {proposal_title}

## Oportunidad Identificada

{opportunity}

### Perfil del Cliente
{client_profile}

### Necesidades Detectadas
{needs}

## 💡 Propuesta de Valor

{value_proposition}

### Diferenciadores
{differentiators}

## 🎯 Solución Propuesta

{solution}

### Alcance
{scope}

### Entregables
{deliverables}

## 📊 Análisis de ROI

| Métrica | Valor |
|---------|-------|
{roi_table}

### Beneficios Cuantificables
{quantifiable_benefits}

### Beneficios Cualitativos
{qualitative_benefits}

## 💰 Inversión

{pricing}

## 🚀 Próximos Pasos

{next_steps}

## 🛡️ Manejo de Objeciones Comunes

{objection_handling}

---

📞 **Contacto:** {contact}
📅 **Validez:** {validity}
""",
        color_scheme="rose"
    ),
}


# ============================================================================
# MAPEO DE CATEGORÍAS A FORMATOS
# ============================================================================

CATEGORY_FORMAT_MAPPING: Dict[str, str] = {
    "software_development": "code",
    "marketing": "creative",
    "finance": "analysis",
    "legal": "document",
    "human_resources": "hr",
    "sales": "sales",
    "operations": "operational",
    "education": "educational",
    "creative": "creative",
    "project_management": "strategic",
    "mercadolibre": "marketplace",
    "youtube": "marketplace",
}


def get_format_for_agent(agent_id: str, agent_category: str) -> ResponseFormat:
    """Obtiene el formato de respuesta apropiado para un agente"""
    format_type = CATEGORY_FORMAT_MAPPING.get(agent_category, "analysis")
    return RESPONSE_FORMATS.get(format_type, RESPONSE_FORMATS["analysis"])


def get_format_for_category(category: str) -> ResponseFormat:
    """Obtiene el formato de respuesta para una categoría"""
    format_type = CATEGORY_FORMAT_MAPPING.get(category, "analysis")
    return RESPONSE_FORMATS.get(format_type, RESPONSE_FORMATS["analysis"])


def get_min_words_for_agent(agent_category: str) -> int:
    """Obtiene el mínimo de palabras requeridas para un agente"""
    format_obj = get_format_for_category(agent_category)
    return format_obj.min_total_words


def get_sections_for_agent(agent_category: str) -> List[ResponseSection]:
    """Obtiene las secciones requeridas para un agente"""
    format_obj = get_format_for_category(agent_category)
    return format_obj.sections


def build_response_prompt(agent_category: str, task: str) -> str:
    """Construye el prompt de formato para el agente"""
    format_obj = get_format_for_category(agent_category)
    
    sections_text = "\n".join([
        f"- {s.emoji} **{s.title}** (mínimo {s.min_words} palabras)"
        for s in format_obj.sections if s.required
    ])
    
    return f"""
## FORMATO DE RESPUESTA REQUERIDO

Tu respuesta debe seguir el formato "{format_obj.name}" con las siguientes secciones obligatorias:

{sections_text}

**Requisitos:**
- Mínimo total: {format_obj.min_total_words} palabras
- Usa markdown para formato
- Incluye tablas donde sea apropiado
- Sé exhaustivo y profesional
- Proporciona ejemplos concretos
- Incluye métricas cuando aplique

---

**TAREA A RESOLVER:**
{task}
"""
