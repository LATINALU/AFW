# ATP API Documentation v1.0.0

## Descripción General

La API de ATP (Agentic Task Platform) permite integrar el sistema de agentes especializados en aplicaciones externas. Proporciona acceso programático a 30 agentes especializados con capacidades de procesamiento de lenguaje natural avanzado.

## Autenticación

La API utiliza autenticación basada en API Keys. Debes incluir tu API key en el header `X-API-Key` de cada request.

```bash
X-API-Key: atp_your_api_key_here
```

### Obtener una API Key

1. Inicia sesión en tu cuenta ATP
2. Ve a Configuración → API Keys
3. Genera una nueva API key
4. **Importante**: Guarda la key de forma segura, solo se muestra una vez

## Base URL

```
https://api.atp.com/api/v1
```

Para desarrollo local:
```
http://localhost:8001/api/v1
```

## Rate Limiting

- **Chat Endpoint**: 30 requests/minuto por API key
- **List Endpoints**: 60 requests/minuto por API key
- **Usage Stats**: 30 requests/minuto por API key

Los headers de respuesta incluyen información sobre el rate limit:
```
X-RateLimit-Limit: 30
X-RateLimit-Remaining: 25
X-RateLimit-Reset: 1640000000
```

## Endpoints

### 1. Chat con Agentes

Procesa una tarea usando agentes especializados seleccionados.

**Endpoint**: `POST /chat`

**Headers**:
```
Content-Type: application/json
X-API-Key: your_api_key
```

**Request Body**:
```json
{
  "message": "Analiza las tendencias del mercado de IA en 2024",
  "agents": ["research", "analysis", "synthesis"],
  "model": "openai/gpt-4o-mini",
  "stream": false
}
```

**Parámetros**:
- `message` (string, requerido): Tarea o pregunta a procesar (1-10000 caracteres)
- `agents` (array, requerido): Lista de IDs de agentes a usar (1-30 agentes)
- `model` (string, opcional): Modelo de IA a usar (default: "openai/gpt-4o-mini")
- `stream` (boolean, opcional): Habilitar streaming (default: false)

**Response**:
```json
{
  "success": true,
  "result": "Análisis detallado de las tendencias...",
  "agents_used": ["research", "analysis", "synthesis"],
  "model_used": "openai/gpt-4o-mini",
  "timestamp": "2024-01-23T19:35:00.000Z",
  "request_id": "req_abc123xyz"
}
```

**Códigos de Estado**:
- `200`: Éxito
- `400`: Request inválido
- `401`: API key inválida o faltante
- `429`: Rate limit excedido
- `500`: Error del servidor

---

### 2. Listar Agentes

Obtiene la lista de todos los agentes disponibles.

**Endpoint**: `GET /agents`

**Headers**:
```
X-API-Key: your_api_key
```

**Response**:
```json
{
  "success": true,
  "agents": [
    {
      "id": "reasoning",
      "name": "Agente de Razonamiento",
      "level": 1,
      "description": "Especializado en razonamiento lógico y análisis crítico"
    },
    {
      "id": "coding",
      "name": "Agente de Programación",
      "level": 2,
      "description": "Experto en desarrollo de software y debugging"
    }
  ],
  "total": 30,
  "timestamp": "2024-01-23T19:35:00.000Z"
}
```

---

### 3. Listar Modelos

Obtiene la lista de modelos de IA disponibles.

**Endpoint**: `GET /models`

**Headers**:
```
X-API-Key: your_api_key
```

**Response**:
```json
{
  "success": true,
  "models": [
    {
      "id": "groq-default",
      "provider": "groq",
      "model": "openai/gpt-oss-120b"
    },
    {
      "id": "openai-gpt4",
      "provider": "openai",
      "model": "gpt-4"
    }
  ],
  "total": 8,
  "timestamp": "2024-01-23T19:35:00.000Z"
}
```

---

### 4. Estadísticas de Uso

Obtiene estadísticas de uso de tu API key.

**Endpoint**: `GET /usage`

**Headers**:
```
X-API-Key: your_api_key
```

**Response**:
```json
{
  "success": true,
  "usage": {
    "requests_today": 45,
    "requests_month": 1250,
    "last_request": "2024-01-23T19:30:00.000Z"
  },
  "timestamp": "2024-01-23T19:35:00.000Z"
}
```

---

### 5. Gestión de API Keys

#### Generar Nueva API Key

**Endpoint**: `POST /keys/generate`

**Headers**:
```
X-API-Key: your_existing_api_key
```

**Request Body**:
```json
{
  "name": "Production API Key"
}
```

**Response**:
```json
{
  "success": true,
  "api_key": "atp_new_generated_key_here",
  "name": "Production API Key",
  "message": "Save this key securely. It won't be shown again.",
  "timestamp": "2024-01-23T19:35:00.000Z"
}
```

#### Listar API Keys

**Endpoint**: `GET /keys`

**Response**:
```json
{
  "success": true,
  "keys": [
    {
      "id": 1,
      "key_prefix": "atp_abc123...",
      "name": "Production API Key",
      "created_at": "2024-01-20T10:00:00.000Z",
      "last_used": "2024-01-23T19:30:00.000Z",
      "is_active": true
    }
  ],
  "total": 2,
  "timestamp": "2024-01-23T19:35:00.000Z"
}
```

#### Revocar API Key

**Endpoint**: `DELETE /keys/{key_prefix}`

**Response**:
```json
{
  "success": true,
  "message": "API key revoked",
  "timestamp": "2024-01-23T19:35:00.000Z"
}
```

---

## Agentes Disponibles

### Nivel 1: Fundamentos
- `reasoning`: Razonamiento lógico
- `planning`: Planificación estratégica
- `research`: Investigación y búsqueda
- `analysis`: Análisis de datos
- `synthesis`: Síntesis de información
- `critical_thinking`: Pensamiento crítico
- `coding`: Programación
- `data`: Ciencia de datos
- `writing`: Escritura profesional
- `communication`: Comunicación efectiva

### Nivel 2: Especializados
- `decision`: Toma de decisiones
- `problem_solving`: Resolución de problemas
- `legal`: Asesoría legal
- `financial`: Análisis financiero
- `creative`: Creatividad e innovación
- `technical`: Documentación técnica
- `educational`: Contenido educativo
- `marketing`: Marketing y ventas
- `qa`: Control de calidad
- `documentation`: Documentación

### Nivel 3: Avanzados
- `optimization`: Optimización
- `security`: Seguridad
- `integration`: Integración de sistemas
- `review`: Revisión de código
- `translation`: Traducción
- `summary`: Resumen
- `formatting`: Formateo
- `validation`: Validación
- `coordination`: Coordinación
- `explanation`: Explicación

---

## Ejemplos de Uso

### Python

```python
import requests

API_KEY = "atp_your_api_key_here"
BASE_URL = "https://api.atp.com/api/v1"

headers = {
    "X-API-Key": API_KEY,
    "Content-Type": "application/json"
}

# Chat con agentes
response = requests.post(
    f"{BASE_URL}/chat",
    headers=headers,
    json={
        "message": "Crea un plan de marketing para un producto SaaS",
        "agents": ["planning", "marketing", "creative"],
        "model": "openai/gpt-4o-mini"
    }
)

result = response.json()
print(result["result"])
```

### JavaScript/Node.js

```javascript
const axios = require('axios');

const API_KEY = 'atp_your_api_key_here';
const BASE_URL = 'https://api.atp.com/api/v1';

async function chatWithAgents() {
  try {
    const response = await axios.post(
      `${BASE_URL}/chat`,
      {
        message: 'Analiza este código y sugiere mejoras',
        agents: ['coding', 'review', 'optimization'],
        model: 'openai/gpt-4o-mini'
      },
      {
        headers: {
          'X-API-Key': API_KEY,
          'Content-Type': 'application/json'
        }
      }
    );
    
    console.log(response.data.result);
  } catch (error) {
    console.error('Error:', error.response.data);
  }
}

chatWithAgents();
```

### cURL

```bash
curl -X POST https://api.atp.com/api/v1/chat \
  -H "X-API-Key: atp_your_api_key_here" \
  -H "Content-Type: application/json" \
  -d '{
    "message": "Explica el concepto de machine learning",
    "agents": ["educational", "explanation", "synthesis"],
    "model": "openai/gpt-4o-mini"
  }'
```

---

## Manejo de Errores

Todos los errores siguen el formato:

```json
{
  "success": false,
  "error": "Error type",
  "message": "Detailed error message",
  "timestamp": "2024-01-23T19:35:00.000Z"
}
```

### Códigos de Error Comunes

- `400 Bad Request`: Parámetros inválidos o faltantes
- `401 Unauthorized`: API key inválida o faltante
- `403 Forbidden`: Acceso denegado
- `429 Too Many Requests`: Rate limit excedido
- `500 Internal Server Error`: Error del servidor

---

## Mejores Prácticas

1. **Seguridad**:
   - Nunca expongas tu API key en código del cliente
   - Usa variables de entorno para almacenar keys
   - Rota tus API keys regularmente

2. **Rate Limiting**:
   - Implementa retry logic con backoff exponencial
   - Monitorea los headers de rate limit
   - Cachea respuestas cuando sea posible

3. **Selección de Agentes**:
   - Usa solo los agentes necesarios para tu tarea
   - Combina agentes complementarios para mejores resultados
   - Experimenta con diferentes combinaciones

4. **Optimización**:
   - Cachea respuestas para consultas frecuentes
   - Usa el modelo más eficiente para tu caso de uso
   - Implementa timeouts apropiados

---

## Soporte

- **Documentación**: https://docs.atp.com
- **Email**: support@atp.com
- **Discord**: https://discord.gg/atp
- **GitHub**: https://github.com/atp/api-examples

---

## Changelog

### v1.0.0 (2024-01-23)
- Lanzamiento inicial de la API
- 30 agentes especializados disponibles
- Autenticación por API key
- Rate limiting implementado
- Soporte para múltiples modelos de IA
