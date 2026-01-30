# 🔑 Configuración de API - ATP v0.7.0

## ⚠️ IMPORTANTE: Configurar API Key

El sistema ATP v0.7.0 requiere que configures una API key para que los agentes puedan funcionar.

## Pasos para Configurar

### 1. Abrir Settings
- Haz clic en el ícono de **Settings (⚙️)** en la esquina superior derecha
- Se abrirá el panel de configuración de API

### 2. Agregar una API Key

#### Opción A: Groq (Recomendado - Gratis)
1. Ve a https://console.groq.com/keys
2. Crea una cuenta gratuita
3. Genera una API key
4. En ATP Settings:
   - **Name**: Groq
   - **Type**: groq
   - **API Key**: Pega tu key de Groq
   - **Base URL**: https://api.groq.com/openai/v1
5. Haz clic en **Add API**
6. Activa el toggle para marcarla como activa (✅)

#### Opción B: OpenAI
1. Ve a https://platform.openai.com/api-keys
2. Genera una API key
3. En ATP Settings:
   - **Name**: OpenAI
   - **Type**: openai
   - **API Key**: Pega tu key de OpenAI
   - **Base URL**: (dejar vacío)
5. Haz clic en **Add API**
6. Activa el toggle para marcarla como activa (✅)

### 3. Verificar Configuración
- Una vez configurada, verás los modelos disponibles en el selector del Header
- El sistema usará automáticamente la API activa para todos los agentes

## Modelos Disponibles

### Groq (Gratis)
- `llama-3.3-70b-versatile` - Rápido y eficiente
- `mixtral-8x7b-32768` - Gran contexto
- `llama-3.1-70b-versatile` - Balanceado

### OpenAI (Pago)
- `gpt-4o` - Más potente
- `gpt-4o-mini` - Económico
- `gpt-3.5-turbo` - Rápido

## Solución de Problemas

### Error: "No API key configured"
✅ **Solución**: Configura una API key siguiendo los pasos anteriores

### Los agentes no responden
1. Verifica que la API esté marcada como **activa** (toggle verde)
2. Verifica que la API key sea válida
3. Recarga la página (F5)

### No veo modelos en el selector
1. Haz clic en "Fetch Models" en Settings
2. Espera a que se carguen los modelos
3. Si no aparecen, verifica la API key

## Arquitectura del Sistema

```
Frontend (StreamingChatV2)
    ↓ apiConfig
WebSocket/SSE
    ↓ apiConfig
Backend (main.py)
    ↓ apiConfig
Agent Instances
    ↓ apiConfig
LLM Providers
    ↓ API Key
Groq/OpenAI API
```

## Notas Importantes

- **Seguridad**: Las API keys se guardan en localStorage del navegador
- **Privacidad**: Las keys NO se envían a ningún servidor externo excepto Groq/OpenAI
- **Múltiples APIs**: Puedes configurar varias y cambiar entre ellas
- **Fallback**: Si no hay API configurada, el sistema intentará usar GROQ_API_KEY del .env

## Ejemplo de Configuración Completa

```json
{
  "id": "groq-1",
  "name": "Groq Free",
  "type": "groq",
  "apiKey": "gsk_xxxxxxxxxxxxxxxxxxxxx",
  "baseUrl": "https://api.groq.com/openai/v1",
  "models": ["llama-3.3-70b-versatile"],
  "isActive": true
}
```

---

**¿Necesitas ayuda?** Revisa los logs del backend con:
```bash
docker-compose logs backend -f
```

Busca líneas como:
- `🔑 API Config recibida` - Confirmación de que la API llegó
- `⚠️ No se recibió apiConfig` - La API no se está enviando
- `❌ Error en agente` - Error al ejecutar el agente
