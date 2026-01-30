# LangGraph + A2A Protocol Architecture - ATP v0.9.0

## 🎯 Objetivo

Implementar una arquitectura limpia donde:
- **LangGraph** gestiona el flujo de ejecución (StateGraph)
- **A2A Protocol** maneja TODA la comunicación entre agentes (capa aislada)
- Los agentes NUNCA se comunican directamente entre sí
- Sin enredos: comunicación estructurada y validada

---

## 🆕 Cambios clave en v0.9.0

- **Comunicación A2A corregida**: todos los agentes usan `AgentCapability` válidos (se añadió `COMMUNICATION` al enum) y la orquestación registra al propio `orchestrator` dentro del protocolo.
- **LLM async real**: `chat_completion` y `test_connection` ahora son funciones `async`, evitando bloqueos y errores tipo `COMMUNICATION`.
- **Node Workflow Editor alineado**: el backend del editor utiliza el mismo flujo `User Query → LangGraph StateGraph → A2A Messages → Agents → A2A Responses → Síntesis → Final Result`, garantizando paridad entre UI y ejecución real.
- **Modelo por defecto documentado**: `llama-3.3-70b-versatile` (Groq) es el modelo gratuito configurado; cualquier otra clave se inyecta vía `.env`.
- **Logging y trazabilidad**: se añadieron logs para cada agente ejecutado (`✅/❌`) y para el endpoint `/api/chat`, facilitando depuración.

---

## 🏗️ Arquitectura

```
┌─────────────────────────────────────────────────────────────┐
│                      USER REQUEST                           │
└──────────────────────┬──────────────────────────────────────┘
                       │
                       ▼
┌─────────────────────────────────────────────────────────────┐
│                   LANGGRAPH ORCHESTRATOR                    │
│  ┌──────────────────────────────────────────────────────┐  │
│  │  StateGraph: Gestión de flujo y estado              │  │
│  │  - analyze_query                                     │  │
│  │  - execute_agents (loop)                             │  │
│  │  - synthesize_results                                │  │
│  │  - finalize_result                                   │  │
│  └──────────────────────────────────────────────────────┘  │
└──────────────────────┬──────────────────────────────────────┘
                       │
                       ▼
┌─────────────────────────────────────────────────────────────┐
│                   A2A PROTOCOL LAYER                        │
│  ┌──────────────────────────────────────────────────────┐  │
│  │  Capa aislada de comunicación                        │  │
│  │  - A2AMessage: Mensajes estructurados                │  │
│  │  - A2AResponse: Respuestas estructuradas             │  │
│  │  - Validación de mensajes                            │  │
│  │  - Routing inteligente                               │  │
│  │  - Trazabilidad completa                             │  │
│  └──────────────────────────────────────────────────────┘  │
└──────────────────────┬──────────────────────────────────────┘
                       │
                       ▼
┌─────────────────────────────────────────────────────────────┐
│                    SPECIALIZED AGENTS                       │
│  ┌──────────┐  ┌──────────┐  ┌──────────┐  ┌──────────┐   │
│  │ Reasoning│  │ Planning │  │  Coding  │  │   Data   │   │
│  │  Agent   │  │  Agent   │  │  Agent   │  │  Agent   │   │
│  └──────────┘  └──────────┘  └──────────┘  └──────────┘   │
│       │              │              │              │        │
│       └──────────────┴──────────────┴──────────────┘        │
│                       │                                     │
│                       ▼                                     │
│               ┌──────────────┐                              │
│               │  Groq LLM    │                              │
│               │ llama-3.3    │                              │
│               └──────────────┘                              │
└─────────────────────────────────────────────────────────────┘
```

---

## 🔄 Flujo de Ejecución (Usado por el Node Workflow Editor)

### 1. **Entrada del Usuario**
```python
User Query → FastAPI Endpoint → AgentOrchestrator.execute()
```

### 2. **LangGraph StateGraph**
```python
# Estado inicial
AgentState = {
    "user_query": "...",
    "a2a_messages": [],
    "a2a_responses": [],
    "agents_to_execute": ["reasoning", "planning", ...],
    "agents_completed": [],
    ...
}

# Flujo del grafo
analyze_query → execute_agents → (loop) → synthesize → finalize → END
```

### 3. **Comunicación A2A**
```python
# Orchestrator crea mensaje A2A
message = protocol.create_message(
    sender_id="orchestrator",
    recipient_id="reasoning",
    subject="Task Execution Request",
    payload={"query": "...", "context": {...}}
)

# Agente procesa y responde
response = protocol.create_response(
    original_message=message,
    responder_id="reasoning",
    result="...",
    success=True
)
```

### 4. **Síntesis de Resultados**
```python
# Combinar todas las respuestas A2A
final_result = synthesize_all_responses(state["a2a_responses"])
```

---

## 📦 Componentes Clave

### **AgentState (TypedDict)**
Estado compartido en el grafo de LangGraph:

```python
class AgentState(TypedDict):
    # Input
    user_query: str
    context: Dict[str, Any]
    
    # Comunicación A2A (capa aislada)
    a2a_messages: List[A2AMessage]
    a2a_responses: List[A2AResponse]
    
    # Control de flujo
    agents_to_execute: List[str]
    agents_completed: List[str]
    
    # Resultados
    intermediate_results: Dict[str, Any]
    final_result: Optional[str]
```

### **A2AMessage**
Mensaje estructurado entre agentes:

```python
class A2AMessage(BaseModel):
    message_id: str
    timestamp: datetime
    message_type: MessageType  # REQUEST, RESPONSE, BROADCAST, etc.
    priority: Priority
    
    sender_id: str
    sender_capability: AgentCapability
    recipient_id: Optional[str]
    
    subject: str
    payload: Dict[str, Any]
    conversation_id: str
```

### **A2AResponse**
Respuesta estructurada de agentes:

```python
class A2AResponse(BaseModel):
    response_id: str
    original_message_id: str
    conversation_id: str
    
    responder_id: str
    responder_capability: AgentCapability
    
    success: bool
    result: Any
    reasoning: Optional[str]
    confidence: float
```

---

## 🎯 Beneficios de esta Arquitectura

### ✅ **Sin Enredos**
- Comunicación estructurada y validada
- Todos los mensajes pasan por A2A Protocol
- No hay comunicación directa entre agentes

### ✅ **Trazabilidad Completa**
- Cada mensaje tiene ID único
- Historial completo de conversaciones
- Fácil debugging y auditoría

### ✅ **Escalabilidad**
- Agregar nuevos agentes es trivial
- Solo registrar en el protocolo A2A
- LangGraph maneja el flujo automáticamente

### ✅ **Mantenibilidad**
- Capa de comunicación aislada
- Cambios en agentes no afectan el protocolo
- Fácil testing de componentes individuales

### ✅ **Flexibilidad**
- Soporte para diferentes tipos de mensajes
- Prioridades configurables
- Routing inteligente basado en capacidades

---

## 🔧 Implementación

### **1. Orchestrator (orchestrator.py)**

```python
class AgentOrchestrator:
    def __init__(self):
        self.agents: Dict[str, Any] = {}
        self.protocol = a2a_protocol  # Capa aislada
        self.graph = None  # StateGraph de LangGraph
        self._register_orchestrator_agent()  # ← nuevo en v0.9.0
    
    def register_agents(self, agents: List[Any]):
        """Registra agentes en orchestrator y protocolo A2A"""
        for agent in agents:
            self.agents[agent.profile.agent_id] = agent
            self.protocol.register_agent(agent.profile)
        
        self.graph = self._build_graph()
    
    def _build_graph(self) -> StateGraph:
        """Construye grafo de LangGraph"""
        workflow = StateGraph(AgentState)
        
        workflow.add_node("analyze_query", self._analyze_query)
        workflow.add_node("execute_agents", self._execute_agents)
        workflow.add_node("synthesize", self._synthesize_results)
        workflow.add_node("finalize", self._finalize_result)
        
        workflow.set_entry_point("analyze_query")
        workflow.add_edge("analyze_query", "execute_agents")
        workflow.add_conditional_edges(
            "execute_agents",
            self._should_continue,
            {"continue": "execute_agents", "synthesize": "synthesize"}
        )
        workflow.add_edge("synthesize", "finalize")
        workflow.add_edge("finalize", END)
        
        return workflow.compile()
```

### **2. Ejecución de Agentes**

```python
async def _execute_agents(self, state: AgentState) -> AgentState:
    """Ejecuta agentes usando A2A Protocol"""
    
    # Obtener siguiente agente pendiente
    pending = [a for a in state["agents_to_execute"] 
               if a not in state["agents_completed"]]
    
    if not pending:
        return state
    
    agent_id = pending[0]
    agent = self.agents[agent_id]
    
    # Crear mensaje A2A
    message = self.protocol.create_message(
        sender_id="orchestrator",
        recipient_id=agent_id,
        subject="Task Execution",
        payload={"query": state["user_query"], ...}
    )
    
    # Ejecutar agente usando A2A
    response = await agent.handle_message(message)
    
    # Crear respuesta A2A
    if response.success:
        state["intermediate_results"][agent_id] = response.result
    
    # Actualizar estado
    state["a2a_messages"] = [message]
    state["a2a_responses"] = [response]
    state["intermediate_results"][agent_id] = result
    state["agents_completed"] = [agent_id]
    
    return state
```

---

## 📊 Ejemplo de Flujo Completo

```python
# 1. Usuario envía query
query = "Analiza las ventajas de microservicios"

# 2. Orchestrator recibe y prepara
orchestrator.execute(
    task=query,
    agents=[reasoning_agent, planning_agent],
    context={}
)

# 3. LangGraph ejecuta flujo
analyze_query(state)
  → Crea mensaje A2A inicial
  
execute_agents(state)
  → Mensaje A2A a reasoning_agent
  → reasoning_agent.execute()
  → Respuesta A2A con resultado
  → Almacena en state["intermediate_results"]
  
execute_agents(state)  # Loop
  → Mensaje A2A a planning_agent
  → planning_agent.execute()
  → Respuesta A2A con resultado
  → Almacena en state["intermediate_results"]
  
synthesize(state)
  → Combina todas las respuestas A2A
  → Genera final_result coherente
  
finalize(state)
  → Marca como completo
  → Retorna resultado final

# 4. Usuario recibe respuesta estructurada
{
    "success": True,
    "final_result": "...",
    "agents_used": ["reasoning", "planning"],
    "a2a_messages_count": 2,
    "a2a_responses_count": 2
}
```

---

## 🚀 Ventajas sobre Implementación Anterior

| Aspecto | Antes | Ahora |
|---------|-------|-------|
| **Comunicación** | Directa entre agentes | A2A Protocol (aislada) |
| **Flujo** | Manual/hardcoded | LangGraph StateGraph |
| **Trazabilidad** | Limitada | Completa (todos los mensajes) |
| **Escalabilidad** | Difícil agregar agentes | Trivial (solo registrar) |
| **Debugging** | Complejo | Fácil (historial A2A) |
| **Mantenibilidad** | Acoplamiento alto | Bajo acoplamiento |
| **Testing** | Difícil | Fácil (componentes aislados) |

---

## 📝 Próximos Pasos

1. ✅ Orchestrator refactorizado con LangGraph + A2A
2. ⏳ Actualizar todos los agentes para usar A2A Protocol
3. ⏳ Verificar flujo de comunicación aislado
4. ⏳ Testing end-to-end
5. ⏳ Documentar patrones de uso

---

## 🎓 Conclusión

Esta arquitectura combina lo mejor de LangGraph (gestión de flujo) con A2A Protocol (comunicación estructurada) para crear un sistema escalable, mantenible y sin enredos.

**Principio clave:** Los agentes NUNCA se comunican directamente. TODO pasa por A2A Protocol.

---

**Versión:** 0.6.8  
**Fecha:** 5 de enero, 2026  
**Estado:** Implementado en orchestrator.py
