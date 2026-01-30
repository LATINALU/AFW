export type Language = 'es' | 'en';

export const translations = {
  es: {
    // Node Workflow Editor
    nodeWorkflowEditor: 'Editor de Flujo de Nodos',
    chatInterface: 'Interfaz de Chat',
    save: 'Guardar',
    load: 'Cargar',
    clear: 'Limpiar',
    import: 'Importar',
    export: 'Exportar',
    runWorkflow: 'Ejecutar Flujo',
    running: 'Ejecutando...',

    // Nodes
    addNodes: 'Agregar Nodos',
    inputNode: 'Entrada',
    agentNode: 'Agente',
    promptNode: 'Prompt',
    aiProviderNode: 'Proveedor IA',
    outputNode: 'Salida',

    // Descriptions
    userInput: 'Entrada del usuario',
    aiAgent: 'Agente IA',
    promptsPositiveNegative: 'Prompts +/-',
    modelConfig: 'Configuración de modelo',
    finalResult: 'Resultado final',

    // How to use
    howToUse: '💡 Cómo usar',
    clickNodesToAdd: 'Click en nodos para agregarlos',
    dragToConnect: 'Arrastra para conectar nodos',
    clickToConfig: 'Click en nodos para configurar',
    runToExecute: 'Ejecuta para procesar workflow',

    // Connection colors
    connectionColors: '🎨 Colores de Conexiones',
    inputConnection: 'Input → Prompt (Cyan)',
    promptConnection: 'Prompt → Agent (Púrpura)',
    agentConnection: 'Agent → AI Provider/Agent/Output (Verde)',
    providerConnection: 'AI Provider → Agent (Naranja)',

    // Validation
    invalidConnection: 'Conexión no válida',
    validConnections: 'Conexiones válidas',

    // Agent
    selectAgent: 'Seleccionar Agente',
    additionalInstructions: 'Instrucciones Adicionales',
    addSpecificInstructions: 'Agregar instrucciones específicas para este agente...',

    // Prompt
    positivePrompt: '✓ Prompt Positivo',
    negativePrompt: '✗ Prompt Negativo',
    whatYouWant: 'Lo que quieres...',
    whatYouDontWant: 'Lo que no quieres...',
    clickToEdit: 'Click + para editar prompts',

    // AI Provider
    provider: 'Proveedor',
    model: 'Modelo',
    temperature: 'Temperatura',
    maxTokens: 'Tokens Máximos',
    selectModel: '-- Seleccionar Modelo --',
    enterModelName: 'Ingresa nombre del modelo',

    // Output
    noOutputYet: 'Sin salida aún. Ejecuta el workflow para ver resultados.',
    copyResult: 'Copiar resultado',

    // Messages
    workflowSaved: '✅ Workflow guardado en el navegador!',
    workflowLoaded: '✅ Workflow cargado desde el navegador!',
    noSavedWorkflow: '⚠️ No se encontró workflow guardado en el navegador.',
    workflowImported: '✅ Workflow importado exitosamente!',
    invalidWorkflowFormat: '⚠️ Formato de workflow inválido.',
    errorParsingWorkflow: '❌ Error al analizar archivo de workflow.',
    workflowExecutedSuccess: '✅ Workflow ejecutado exitosamente!',
    workflowExecutionFailed: '❌ Ejecución de workflow falló',

    // Themes
    selectTheme: 'Seleccionar Tema',
    themesAvailable: '10 temas disponibles',

    // Agents
    agent_reasoning: 'Razonamiento',
    role_reasoning: 'Maestro de Razonamiento Lógico y Pensamiento Crítico',
    agent_planning: 'Planificación',
    role_planning: 'Estratega de Planificación y Gestión de Proyectos',
    agent_research: 'Investigación',
    role_research: 'Investigador Senior y Analista de Información',
    agent_analysis: 'Análisis',
    role_analysis: 'Analista Experto en Descomposición de Problemas',
    agent_synthesis: 'Síntesis',
    role_synthesis: 'Integrador de Conocimiento y Generador de Insights',
    agent_critical_thinking: 'Pensamiento Crítico',
    role_critical_thinking: 'Evaluador Crítico y Detector de Falacias',
    agent_coding: 'Programación',
    role_coding: 'Ingeniero de Software Senior y Arquitecto de Código',
    agent_data: 'Datos',
    role_data: 'Científico de Datos y Analista Cuantitativo',
    agent_writing: 'Escritura',
    role_writing: 'Escritor Profesional y Comunicador Experto',
    agent_communication: 'Comunicación',
    role_communication: 'Especialista en Comunicación y Relaciones',
    agent_decision: 'Decisiones',
    role_decision: 'Estratega de Decisiones y Análisis de Opciones',
    agent_problem_solving: 'Solución de Problemas',
    role_problem_solving: 'Solucionador Creativo de Problemas',
    agent_legal: 'Legal',
    role_legal: 'Asesor Legal y Especialista en Cumplimiento',
    agent_financial: 'Financiero',
    role_financial: 'Analista Financiero y Estratega Económico',
    agent_creative: 'Creativo',
    role_creative: 'Director Creativo y Generador de Ideas',
    agent_technical: 'Técnico',
    role_technical: 'Arquitecto Técnico y Especialista en Sistemas',
    agent_educational: 'Educativo',
    role_educational: 'Educador Experto y Diseñador Instruccional',
    agent_marketing: 'Marketing',
    role_marketing: 'Estratega de Marketing y Especialista en Branding',
    agent_qa: 'Calidad (QA)',
    role_qa: 'Ingeniero de Calidad y Testing',
    agent_documentation: 'Documentación',
    role_documentation: 'Especialista en Documentación Técnica',
    agent_optimization: 'Optimización',
    role_optimization: 'Ingeniero de Optimización y Performance',
    agent_security: 'Seguridad',
    role_security: 'Especialista en Seguridad de la Información',
    agent_integration: 'Integración',
    role_integration: 'Arquitecto de Integraciones y APIs',
    agent_review: 'Revisión',
    role_review: 'Revisor Experto y Coach de Mejora',
    agent_translation: 'Traducción',
    role_translation: 'Traductor Profesional y Especialista en Localización',
    agent_summary: 'Resumen',
    role_summary: 'Especialista en Síntesis y Resumen',
    agent_formatting: 'Formato',
    role_formatting: 'Especialista en Formato y Presentación Visual',
    agent_validation: 'Validación',
    role_validation: 'Verificador de Exactitud y Consistencia',
    agent_coordination: 'Coordinación',
    role_coordination: 'Coordinador de Equipos y Flujos de Trabajo',
    agent_explanation: 'Explicación',
    role_explanation: 'Explicador Experto y Clarificador',
  },
  en: {
    // Node Workflow Editor
    nodeWorkflowEditor: 'Node Workflow Editor',
    chatInterface: 'Chat Interface',
    save: 'Save',
    load: 'Load',
    clear: 'Clear',
    import: 'Import',
    export: 'Export',
    runWorkflow: 'Run Workflow',
    running: 'Running...',

    // Nodes
    addNodes: 'Add Nodes',
    inputNode: 'Input',
    agentNode: 'Agent',
    promptNode: 'Prompt',
    aiProviderNode: 'AI Provider',
    outputNode: 'Output',

    // Descriptions
    userInput: 'User input',
    aiAgent: 'AI Agent',
    promptsPositiveNegative: 'Prompts +/-',
    modelConfig: 'Model config',
    finalResult: 'Final result',

    // How to use
    howToUse: '💡 How to use',
    clickNodesToAdd: 'Click nodes to add them',
    dragToConnect: 'Drag to connect nodes',
    clickToConfig: 'Click nodes to configure',
    runToExecute: 'Run to execute workflow',

    // Connection colors
    connectionColors: '🎨 Connection Colors',
    inputConnection: 'Input → Prompt (Cyan)',
    promptConnection: 'Prompt → Agent (Purple)',
    agentConnection: 'Agent → AI Provider/Agent/Output (Green)',
    providerConnection: 'AI Provider → Agent (Orange)',

    // Validation
    invalidConnection: 'Invalid connection',
    validConnections: 'Valid connections',

    // Agent
    selectAgent: 'Select Agent',
    additionalInstructions: 'Additional Instructions',
    addSpecificInstructions: 'Add specific instructions for this agent...',

    // Prompt
    positivePrompt: '✓ Positive Prompt',
    negativePrompt: '✗ Negative Prompt',
    whatYouWant: 'What you want...',
    whatYouDontWant: "What you don't want...",
    clickToEdit: 'Click + to edit prompts',

    // AI Provider
    provider: 'Provider',
    model: 'Model',
    temperature: 'Temperature',
    maxTokens: 'Max Tokens',
    selectModel: '-- Select Model --',
    enterModelName: 'Enter model name',

    // Output
    noOutputYet: 'No output yet. Run the workflow to see results.',
    copyResult: 'Copy result',

    // Messages
    workflowSaved: '✅ Workflow saved to browser storage!',
    workflowLoaded: '✅ Workflow loaded from browser storage!',
    noSavedWorkflow: '⚠️ No saved workflow found in browser storage.',
    workflowImported: '✅ Workflow imported successfully!',
    invalidWorkflowFormat: '⚠️ Invalid workflow file format.',
    errorParsingWorkflow: '❌ Error parsing workflow file.',
    workflowExecutedSuccess: '✅ Workflow executed successfully!',
    workflowExecutionFailed: '❌ Workflow execution failed',

    // Themes
    selectTheme: 'Select Theme',
    themesAvailable: '10 themes available',

    // Settings
    newChat: 'New Chat',
    switchToNodeEditor: 'Switch to Node Editor',
    configureAPIs: 'Configure APIs',

    // Agents
    agent_reasoning: 'Reasoning',
    role_reasoning: 'Master of Logical Reasoning and Critical Thinking',
    agent_planning: 'Planning',
    role_planning: 'Planning Strategist and Project Manager',
    agent_research: 'Research',
    role_research: 'Senior Researcher and Information Analyst',
    agent_analysis: 'Analysis',
    role_analysis: 'Expert Analyst in Problem Decomposition',
    agent_synthesis: 'Synthesis',
    role_synthesis: 'Knowledge Integrator and Insight Generator',
    agent_critical_thinking: 'Critical Thinking',
    role_critical_thinking: 'Critical Evaluator and Fallacy Detector',
    agent_coding: 'Coding',
    role_coding: 'Senior Software Engineer and Code Architect',
    agent_data: 'Data',
    role_data: 'Data Scientist and Quantitative Analyst',
    agent_writing: 'Writing',
    role_writing: 'Professional Writer and Expert Communicator',
    agent_communication: 'Communication',
    role_communication: 'Communication Specialist and Relationship Expert',
    agent_decision: 'Decision',
    role_decision: 'Decision Strategist and Option Analyst',
    agent_problem_solving: 'Problem Solving',
    role_problem_solving: 'Creative Problem Solver',
    agent_legal: 'Legal',
    role_legal: 'Legal Advisor and Compliance Specialist',
    agent_financial: 'Financial',
    role_financial: 'Financial Analyst and Economic Strategist',
    agent_creative: 'Creative',
    role_creative: 'Creative Director and Idea Generator',
    agent_technical: 'Technical',
    role_technical: 'Technical Architect and Systems Specialist',
    agent_educational: 'Educational',
    role_educational: 'Expert Educator and Instructional Designer',
    agent_marketing: 'Marketing',
    role_marketing: 'Marketing Strategist and Branding Specialist',
    agent_qa: 'Quality Assurance',
    role_qa: 'Quality Engineer and Tester',
    agent_documentation: 'Documentation',
    role_documentation: 'Technical Documentation Specialist',
    agent_optimization: 'Optimization',
    role_optimization: 'Optimization and Performance Engineer',
    agent_security: 'Security',
    role_security: 'Information Security Specialist',
    agent_integration: 'Integration',
    role_integration: 'Integration and API Architect',
    agent_review: 'Review',
    role_review: 'Expert Reviewer and Improvement Coach',
    agent_translation: 'Translation',
    role_translation: 'Professional Translator and Localization Specialist',
    agent_summary: 'Summary',
    role_summary: 'Synthesis and Summary Specialist',
    agent_formatting: 'Formatting',
    role_formatting: 'Formatting and Visual Presentation Specialist',
    agent_validation: 'Validation',
    role_validation: 'Accuracy and Consistency Verifier',
    agent_coordination: 'Coordination',
    role_coordination: 'Team Coordinator and Workflow Manager',
    agent_explanation: 'Explanation',
    role_explanation: 'Expert Explainer and Clarifier',
  },
};

export function getTranslation(lang: Language, key: keyof typeof translations.es): string {
  return translations[lang][key] || translations.es[key];
}

export function getCurrentLanguage(): Language {
  if (typeof window !== 'undefined') {
    const saved = localStorage.getItem('atp-language') as Language;
    return saved || 'es';
  }
  return 'es';
}

export function setCurrentLanguage(lang: Language): void {
  if (typeof window !== 'undefined') {
    localStorage.setItem('atp-language', lang);
  }
}
