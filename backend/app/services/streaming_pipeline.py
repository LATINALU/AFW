"""
Streaming Agent Pipeline v0.8.0
===============================
Pipeline de agentes con streaming en tiempo real y formatos especializados.

Características:
- Ejecución jerárquica por niveles
- Streaming de respuestas vía WebSocket
- Formateo automático para humanos
- Inyección de contexto entre agentes
- **NUEVO**: Prompts especializados por tipo de agente
- **NUEVO**: Mínimos de palabras según funcionalidad
- Manejo robusto de errores
"""

import asyncio
from typing import List, Dict, Any, AsyncGenerator, Optional
from datetime import datetime
import traceback

from app.websocket_manager import manager
from app.formatters.human_formatter import HumanResponseFormatter

# === SISTEMA DE FORMATOS ESPECIALIZADOS ===
try:
    from app.agents.enhanced_registry import (
        build_agent_prompt,
        get_specialized_system_prompt,
        ENHANCED_AGENT_DEFINITIONS
    )
    from app.agents.response_formats import (
        CATEGORY_FORMAT_MAPPING,
        get_min_words_for_agent
    )
    SPECIALIZED_FORMATS_AVAILABLE = True
except ImportError:
    SPECIALIZED_FORMATS_AVAILABLE = False
    ENHANCED_AGENT_DEFINITIONS = {}
    CATEGORY_FORMAT_MAPPING = {}


class StreamingAgentPipeline:
    """
    Pipeline de agentes con capacidad de streaming en tiempo real.
    
    Integra:
    - Ejecución secuencial por niveles
    - WebSocket para actualizaciones en vivo
    - Formateo humano de respuestas
    - Contexto acumulativo entre agentes
    """
    
    def __init__(self, agents: List[Any], agent_definitions: Dict[str, Dict], language: str = "es"):
        """
        Inicializa el pipeline.
        
        Args:
            agents: Lista de instancias de agentes
            agent_definitions: Definiciones de agentes con niveles
            language: Idioma de la respuesta
        """
        self.agents = agents
        self.agent_definitions = agent_definitions
        self.language = language
        self.results: List[Dict] = []
        self.accumulated_context = ""
        self.start_time: Optional[datetime] = None
    
    async def execute_with_streaming(
        self,
        task: str,
        client_id: str,
        context: Optional[Dict] = None
    ) -> AsyncGenerator[Dict, None]:
        """
        Ejecuta el pipeline con streaming de resultados.
        
        Args:
            task: Tarea a procesar
            client_id: ID del cliente WebSocket
            context: Contexto inicial opcional
            
        Yields:
            Respuestas formateadas de cada agente
        """
        self.start_time = datetime.utcnow()
        self.results = []
        self.accumulated_context = ""
        
        # Ordenar agentes por nivel
        sorted_agents = self._sort_agents_by_level()
        total_agents = len(sorted_agents)
        
        # Notificar inicio del pipeline
        await manager.send_json(client_id, {
            "type": "pipeline_start",
            "total_agents": total_agents,
            "agents": [self._get_agent_info(a) for a in sorted_agents],
            "timestamp": datetime.utcnow().isoformat()
        })
        
        for i, agent in enumerate(sorted_agents, 1):
            agent_id = self._get_agent_id(agent)
            agent_info = self._get_agent_info(agent)
            
            try:
                # Notificar inicio del agente
                await manager.send_agent_start(
                    client_id,
                    agent_info["name"],
                    i,
                    total_agents
                )
                
                # Preparar input con contexto acumulado y prompt especializado
                agent_category = self._get_agent_category(agent)
                enhanced_task = self._prepare_task_with_context(task, i, agent)
                
                # Enviar progreso inicial
                await manager.send_agent_progress(
                    client_id,
                    agent_info["name"],
                    10,
                    "Analizando consulta..."
                )
                
                # Ejecutar agente
                raw_response = await self._execute_agent(agent, enhanced_task)
                
                # Enviar progreso de procesamiento
                await manager.send_agent_progress(
                    client_id,
                    agent_info["name"],
                    70,
                    "Formateando respuesta..."
                )
                
                # Formatear respuesta para humanos
                formatted = HumanResponseFormatter.format_agent_response(
                    raw_response=raw_response,
                    agent_id=agent_id,
                    agent_name=agent_info["name"],
                    level=agent_info["level"],
                    specialty=agent_info["specialty"],
                    step=i,
                    total_steps=total_agents,
                    language=self.language
                )
                
                # === AGREGAR METADATOS DE FORMATO ESPECIALIZADO ===
                formatted["category"] = agent_category
                if SPECIALIZED_FORMATS_AVAILABLE:
                    format_type = CATEGORY_FORMAT_MAPPING.get(agent_category, "analysis")
                    formatted["format_type"] = format_type
                    formatted["min_words"] = get_min_words_for_agent(agent_category)
                else:
                    formatted["format_type"] = "analysis"
                    formatted["min_words"] = 500
                
                # Agregar a resultados
                self.results.append(formatted)
                
                # Actualizar contexto acumulado
                self._update_accumulated_context(agent_info["name"], raw_response)
                
                # Enviar respuesta completa
                await manager.send_agent_response(client_id, formatted)
                
                # Enviar progreso completado
                await manager.send_agent_progress(
                    client_id,
                    agent_info["name"],
                    100,
                    "Completado"
                )
                
                # Yield para SSE
                yield formatted
                
                # Pequeña pausa para mejor UX
                await asyncio.sleep(0.3)
                
            except Exception as e:
                error_msg = str(e)
                error_traceback = traceback.format_exc()
                print(f"❌ Error en agente {agent_id}: {error_msg}")
                print(f"📋 Traceback:\n{error_traceback}")
                
                # Crear respuesta de error
                error_response = {
                    "agent_id": agent_id,
                    "agent_name": agent_info["name"],
                    "agent_emoji": "⚠️",
                    "level": agent_info["level"],
                    "level_name": f"Nivel {agent_info['level']}",
                    "specialty": agent_info["specialty"],
                    "response_type": "error",
                    "title": f"⚠️ Error en {agent_info['name']}",
                    "sections": [{
                        "title": "Error",
                        "type": "error",
                        "items": [f"Error: {error_msg}"]
                    }],
                    "key_points": ["Proceso interrumpido"],
                    "summary": "Error durante el procesamiento",
                    "raw_content": error_msg,
                    "step": i,
                    "total_steps": total_agents,
                    "progress": round((i / total_agents) * 100, 1),
                    "timestamp": datetime.utcnow().isoformat()
                }
                
                await manager.send_agent_error(client_id, agent_info["name"], error_msg)
                self.results.append(error_response)
                yield error_response
                
                # Continuar con el siguiente agente en lugar de detener todo
                continue
        
        # Calcular tiempo total
        total_time_ms = (datetime.utcnow() - self.start_time).total_seconds() * 1000
        
        # Generar resumen final
        summary = HumanResponseFormatter.create_pipeline_summary(
            agents_completed=[r["agent_id"] for r in self.results if r.get("response_type") != "error"],
            total_time_ms=total_time_ms,
            success=all(r.get("response_type") != "error" for r in self.results),
            language=self.language
        )
        
        # Enviar resumen
        await manager.send_pipeline_complete(client_id, summary)
        yield summary
    
    def _sort_agents_by_level(self) -> List[Any]:
        """Ordena agentes por nivel de expertise (1 primero)."""
        def get_level(agent) -> int:
            agent_id = self._get_agent_id(agent)
            agent_type = agent_id.rsplit('_', 2)[0] if '_' in agent_id else agent_id
            
            for key, info in self.agent_definitions.items():
                if agent_type.startswith(key) or key in agent_type:
                    return info.get('level', 3)
            return 3
        
        return sorted(self.agents, key=get_level)
    
    def _get_agent_id(self, agent: Any) -> str:
        """Obtiene el ID del agente."""
        if hasattr(agent, 'id'):
            return agent.id
        elif hasattr(agent, 'profile') and hasattr(agent.profile, 'id'):
            return agent.profile.id
        else:
            return str(type(agent).__name__).lower()
    
    def _get_agent_info(self, agent: Any) -> Dict[str, Any]:
        """Obtiene información del agente para display, traducida según el idioma del pipeline."""
        agent_id = self._get_agent_id(agent)
        agent_type = agent_id.rsplit('_', 2)[0] if '_' in agent_id else agent_id
        
        # Diccionario de traducciones para fallback si no está en AGENT_DEFINITIONS
        # O para complementar AGENT_DEFINITIONS
        names_trans = {
            "es": {
                "reasoning": "Agente de Razonamiento",
                "planning": "Agente de Planificación",
                "research": "Agente de Investigación",
                "analysis": "Agente de Análisis",
                "synthesis": "Agente de Síntesis",
                "critical_thinking": "Agente de Pensamiento Crítico",
                "coding": "Agente de Programación",
                "data": "Agente de Datos",
                "writing": "Agente de Escritura",
                "communication": "Agente de Comunicación",
                "decision": "Agente de Decisiones",
                "problem_solving": "Agente de Solución de Problemas",
                "legal": "Agente Legal",
                "financial": "Agente Financiero",
                "creative": "Agente Creativo",
                "technical": "Agente Técnico",
                "educational": "Agente Educativo",
                "marketing": "Agente de Marketing",
                "qa": "Agente de Calidad (QA)",
                "documentation": "Agente de Documentación",
                "optimization": "Agente de Optimización",
                "security": "Agente de Seguridad",
                "integration": "Agente de Integración",
                "review": "Agente de Revisión",
                "translation": "Agente de Traducción",
                "summary": "Agente de Resumen",
                "formatting": "Agente de Formato",
                "validation": "Agente de Validación",
                "coordination": "Agente de Coordinación",
                "explanation": "Agente de Explicación",
            },
            "en": {
                "reasoning": "Reasoning Agent",
                "planning": "Planning Agent",
                "research": "Research Agent",
                "analysis": "Analysis Agent",
                "synthesis": "Synthesis Agent",
                "critical_thinking": "Critical Thinking Agent",
                "coding": "Coding Agent",
                "data": "Data Agent",
                "writing": "Writing Agent",
                "communication": "Communication Agent",
                "decision": "Decision Agent",
                "problem_solving": "Problem Solving Agent",
                "legal": "Legal Agent",
                "financial": "Financial Agent",
                "creative": "Creative Agent",
                "technical": "Technical Agent",
                "educational": "Educational Agent",
                "marketing": "Marketing Agent",
                "qa": "QA Agent",
                "documentation": "Documentation Agent",
                "optimization": "Optimization Agent",
                "security": "Security Agent",
                "integration": "Integration Agent",
                "review": "Review Agent",
                "translation": "Translation Agent",
                "summary": "Summary Agent",
                "formatting": "Formatting Agent",
                "validation": "Validation Agent",
                "coordination": "Coordination Agent",
                "explanation": "Explanation Agent",
            }
        }

        # Buscar en definiciones
        level = 3
        name = names_trans.get(self.language, names_trans["es"]).get(agent_type, agent_id.replace('_', ' ').title())
        
        for key, info in self.agent_definitions.items():
            if agent_type.startswith(key) or key in agent_type:
                level = info.get('level', 3)
                # Si queremos usar el nombre de AGENT_DEFINITIONS, deberíamos tenerlo traducido allí
                # Pero por ahora usamos names_trans para asegurar consistencia con el pedido del usuario
                break
        
        # Obtener especialización del perfil si existe
        specialty = "Agente Especializado" if self.language == "es" else "Specialized Agent"
        if hasattr(agent, 'profile') and hasattr(agent.profile, 'specialization'):
            specialty = agent.profile.specialization
        elif hasattr(agent, 'profile') and hasattr(agent.profile, 'role'):
            specialty = agent.profile.role
        
        return {
            "id": agent_id,
            "name": name,
            "level": level,
            "specialty": specialty
        }
    
    def _prepare_task_with_context(self, task: str, step: int, agent: Any = None) -> str:
        """
        Prepara la tarea con contexto acumulado y prompt especializado según categoría.
        
        Args:
            task: Tarea original
            step: Paso actual en el pipeline
            agent: Instancia del agente (opcional, para obtener categoría)
        
        Returns:
            Tarea enriquecida con formato especializado
        """
        # Obtener información del agente si está disponible
        agent_id = self._get_agent_id(agent) if agent else "generic"
        agent_category = self._get_agent_category(agent) if agent else "analysis"
        
        # === USAR PROMPT ESPECIALIZADO SI ESTÁ DISPONIBLE ===
        specialized_prompt = ""
        if SPECIALIZED_FORMATS_AVAILABLE and agent:
            agent_data = ENHANCED_AGENT_DEFINITIONS.get(agent_id, {})
            if agent_data:
                try:
                    specialized_prompt = build_agent_prompt(agent_id, agent_data, task)
                except Exception as e:
                    print(f"⚠️ Error generando prompt especializado: {e}")
                    specialized_prompt = ""
        
        # Construir prompt base si no hay especializado
        if specialized_prompt:
            base_task = specialized_prompt
        else:
            base_task = task
        
        # Agregar contexto de agentes anteriores
        if step == 1 or not self.accumulated_context:
            return base_task
        
        # Combinar con contexto acumulado
        enhanced = f"""{base_task}

---

## CONTEXTO DE EXPERTOS ANTERIORES

{self.accumulated_context}

---

**INSTRUCCIÓN:** Considera el análisis previo y COMPLEMENTA con tu expertise especializado.
Tu respuesta debe seguir la estructura de formato indicada arriba y ser EXHAUSTIVA."""
        
        return enhanced
    
    def _get_agent_category(self, agent: Any) -> str:
        """
        Obtiene la categoría del agente para determinar el formato de respuesta.
        
        Args:
            agent: Instancia del agente
            
        Returns:
            Categoría del agente (software_development, marketing, etc.)
        """
        agent_id = self._get_agent_id(agent)
        
        # Buscar en definiciones mejoradas primero
        if SPECIALIZED_FORMATS_AVAILABLE and agent_id in ENHANCED_AGENT_DEFINITIONS:
            return ENHANCED_AGENT_DEFINITIONS[agent_id].get("category", "analysis")
        
        # Buscar en definiciones del pipeline
        for key, info in self.agent_definitions.items():
            if agent_id.startswith(key) or key in agent_id:
                return info.get('category', 'analysis')
        
        # Inferir categoría por prefijo del agent_id
        category_prefixes = {
            "backend": "software_development",
            "frontend": "software_development",
            "devops": "software_development",
            "fullstack": "software_development",
            "api": "software_development",
            "database": "software_development",
            "architect": "software_development",
            "cto": "software_development",
            "qa": "software_development",
            "security": "software_development",
            "marketing": "marketing",
            "content": "marketing",
            "seo": "marketing",
            "social": "marketing",
            "brand": "marketing",
            "growth": "marketing",
            "email": "marketing",
            "ppc": "marketing",
            "finance": "finance",
            "cfo": "finance",
            "accountant": "finance",
            "tax": "finance",
            "investment": "finance",
            "budget": "finance",
            "audit": "finance",
            "legal": "legal",
            "compliance": "legal",
            "contract": "legal",
            "ip": "legal",
            "privacy": "legal",
            "hr": "human_resources",
            "talent": "human_resources",
            "recruiter": "human_resources",
            "training": "human_resources",
            "culture": "human_resources",
            "sales": "sales",
            "account": "sales",
            "negotiation": "sales",
            "crm": "sales",
            "operations": "operations",
            "logistics": "operations",
            "supply": "operations",
            "inventory": "operations",
            "process": "operations",
            "education": "education",
            "instructor": "education",
            "curriculum": "education",
            "elearning": "education",
            "creative": "creative",
            "design": "creative",
            "video": "creative",
            "animator": "creative",
            "illustration": "creative",
            "project": "project_management",
            "scrum": "project_management",
            "agile": "project_management",
            "pmo": "project_management",
            "ml_": "mercadolibre",
            "mercadolibre": "mercadolibre",
            "yt_": "youtube",
            "youtube": "youtube",
        }
        
        for prefix, category in category_prefixes.items():
            if agent_id.startswith(prefix) or prefix in agent_id:
                return category
        
        return "analysis"  # Default
    
    def _update_accumulated_context(self, agent_name: str, response: Any):
        """Actualiza el contexto acumulado con la respuesta del agente."""
        response_text = str(response) if not isinstance(response, str) else response
        
        # Limitar tamaño del contexto
        if len(response_text) > 1000:
            response_text = response_text[:1000] + "..."
        
        self.accumulated_context += f"\n\n--- {agent_name} ---\n{response_text}"
        
        # Mantener contexto manejable
        if len(self.accumulated_context) > 5000:
            self.accumulated_context = self.accumulated_context[-4000:]
    
    async def _execute_agent(self, agent: Any, task: str) -> Any:
        """
        Ejecuta un agente individual.
        
        Args:
            agent: Instancia del agente
            task: Tarea a procesar
            
        Returns:
            Respuesta del agente
        """
        # Verificar si el agente tiene método execute/process
        if hasattr(agent, 'execute'):
            if asyncio.iscoroutinefunction(agent.execute):
                return await agent.execute(task)
            return agent.execute(task)
        
        elif hasattr(agent, 'process_task'):
            if asyncio.iscoroutinefunction(agent.process_task):
                result = await agent.process_task(task, {})
                # Extraer contenido si es dict
                if isinstance(result, dict):
                    return result.get("content", result.get("response", str(result)))
                return str(result)
            result = agent.process_task(task, {})
            if isinstance(result, dict):
                return result.get("content", result.get("response", str(result)))
            return str(result)
        
        elif hasattr(agent, 'process'):
            if asyncio.iscoroutinefunction(agent.process):
                return await agent.process(task)
            return agent.process(task)
        
        elif hasattr(agent, 'call_llm'):
            # call_llm espera lista de mensajes, no string
            messages = [{"role": "user", "content": task}]
            if asyncio.iscoroutinefunction(agent.call_llm):
                return await agent.call_llm(messages)
            return agent.call_llm(messages)
        
        elif hasattr(agent, '__call__'):
            result = agent(task)
            if asyncio.iscoroutine(result):
                return await result
            return result
        
        else:
            raise ValueError(f"Agent {type(agent).__name__} no tiene método de ejecución válido")
    
    def get_results(self) -> List[Dict]:
        """Retorna todos los resultados del pipeline."""
        return self.results
    
    def get_accumulated_context(self) -> str:
        """Retorna el contexto acumulado."""
        return self.accumulated_context
