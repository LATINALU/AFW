# Guía de Contribución - ATP

¡Gracias por tu interés en contribuir a ATP! Este documento te guiará en el proceso.

## 🚀 Cómo Empezar

### 1. Fork el Repositorio

Haz clic en el botón "Fork" en la esquina superior derecha de GitHub.

### 2. Clona tu Fork

```bash
git clone https://github.com/TU_USUARIO/ATP.git
cd ATP
```

### 3. Configura el Upstream

```bash
git remote add upstream https://github.com/USUARIO_ORIGINAL/ATP.git
```

### 4. Crea una Rama

```bash
git checkout -b feature/mi-nueva-caracteristica
# o
git checkout -b fix/arreglo-de-bug
```

## 🛠️ Configuración del Entorno de Desarrollo

### Backend (Python)

```bash
# Crear entorno virtual
python -m venv venv

# Activar (Windows)
venv\Scripts\activate

# Activar (Linux/Mac)
source venv/bin/activate

# Instalar dependencias
pip install -r requirements.txt
```

### Frontend (Next.js)

```bash
cd frontend
npm install
npm run dev
```

### Docker

```bash
docker-compose up --build
```

## 📝 Estándares de Código

### Python
- Usa **PEP 8** para el estilo de código
- Documenta funciones con docstrings
- Usa type hints cuando sea posible
- Nombres de variables en `snake_case`

### TypeScript/React
- Usa **ESLint** y **Prettier**
- Componentes funcionales con hooks
- Props tipadas con interfaces
- Nombres de componentes en `PascalCase`

### Commits
Usa mensajes de commit descriptivos:

```
feat: añadir nuevo agente de análisis de sentimientos
fix: corregir error en el selector de modelos
docs: actualizar README con instrucciones de Docker
style: formatear código del frontend
refactor: reorganizar estructura de agentes
test: añadir tests para el orquestador
```

## 🔧 Áreas de Contribución

### 🐛 Reportar Bugs

1. Verifica que el bug no haya sido reportado antes
2. Abre un Issue con:
   - Descripción clara del problema
   - Pasos para reproducir
   - Comportamiento esperado vs actual
   - Screenshots si aplica
   - Información del sistema (OS, versión de Python/Node)

### 💡 Sugerir Características

1. Abre un Issue con la etiqueta `enhancement`
2. Describe la característica propuesta
3. Explica por qué sería útil
4. Proporciona ejemplos de uso si es posible

### 🔧 Enviar Pull Requests

1. Asegúrate de que tu código sigue los estándares
2. Añade tests si es posible
3. Actualiza la documentación si es necesario
4. Describe los cambios en el PR
5. Referencia cualquier Issue relacionado

## 📁 Estructura del Proyecto

```
ATP/
├── agents/                 # Definición de agentes
│   ├── base_agent.py      # Clase base
│   ├── level1_critical.py # Agentes nivel 1
│   └── ...
├── backend/               # API FastAPI
│   └── main.py
├── frontend/              # Interfaz Next.js
│   ├── src/
│   │   ├── app/          # Páginas
│   │   ├── components/   # Componentes React
│   │   └── styles/       # Estilos CSS
│   └── package.json
├── orchestrator/          # Orquestador de tareas
├── config/               # Configuración
└── docker-compose.yml    # Docker
```

## 🎯 Prioridades Actuales

Estas son las áreas donde más necesitamos ayuda:

1. **Integración de Proveedores de IA**
   - Añadir soporte para más APIs (Anthropic, Cohere, etc.)
   - Mejorar el manejo de errores de API

2. **Sistema de Agentes**
   - Mejorar la selección automática de agentes
   - Añadir más agentes especializados
   - Optimizar el razonamiento

3. **Frontend**
   - Mejorar la UX/UI
   - Añadir más temas
   - Implementar historial de conversaciones
   - Añadir exportación de resultados

4. **Testing**
   - Tests unitarios para agentes
   - Tests de integración para API
   - Tests E2E para frontend

5. **Documentación**
   - Traducir a inglés
   - Añadir más ejemplos
   - Crear tutoriales en video

## ❓ Preguntas

Si tienes preguntas, puedes:
- Abrir un Issue con la etiqueta `question`
- Contactar al mantenedor

## 📜 Código de Conducta

- Sé respetuoso con otros contribuidores
- Acepta críticas constructivas
- Enfócate en lo mejor para el proyecto
- Muestra empatía hacia otros miembros

---

¡Gracias por contribuir! 🎉
