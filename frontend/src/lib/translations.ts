/**
 * ATP v0.8.0+ - Translations System
 * ==================================
 * Sistema de traducciones mejorado ES/EN
 */

export type Language = "es" | "en";

export const translations = {
  es: {
    // Autenticación
    auth: {
      login: "Iniciar Sesión",
      register: "Registrarse",
      logout: "Cerrar Sesión",
      username: "Usuario",
      email: "Correo Electrónico",
      password: "Contraseña",
      confirmPassword: "Confirmar Contraseña",
      forgotPassword: "¿Olvidaste tu contraseña?",
      createAccount: "Crear Cuenta",
      alreadyHaveAccount: "¿Ya tienes cuenta?",
      dontHaveAccount: "¿No tienes cuenta?",
      loginSuccess: "Sesión iniciada correctamente",
      registerSuccess: "Cuenta creada correctamente",
      invalidCredentials: "Credenciales inválidas",
      userCode: "Código de Usuario",
    },
    
    // Navegación
    nav: {
      home: "Inicio",
      agents: "Agentes",
      conversations: "Conversaciones",
      settings: "Configuración",
      admin: "Administración",
      profile: "Perfil",
      help: "Ayuda",
    },
    
    // Agentes
    agents: {
      title: "Agentes de IA",
      selectAgents: "Seleccionar Agentes",
      selectedAgents: "Agentes Seleccionados",
      noAgentsSelected: "No hay agentes seleccionados",
      selectAtLeast: "Selecciona al menos un agente",
      maxAgents: "Máximo de agentes alcanzado",
      availableAgents: "Agentes Disponibles",
      level: "Nivel",
      specialty: "Especialidad",
      description: "Descripción",
      clearSelection: "Limpiar Selección",
      selectAll: "Seleccionar Todos",
    },
    
    // Chat
    chat: {
      typeMessage: "Escribe tu mensaje...",
      send: "Enviar",
      thinking: "Pensando...",
      processing: "Procesando...",
      newConversation: "Nueva Conversación",
      saveConversation: "Guardar Conversación",
      deleteConversation: "Eliminar Conversación",
      exportConversation: "Exportar Conversación",
      conversationHistory: "Historial de Conversaciones",
      noMessages: "No hay mensajes",
      startConversation: "Inicia una conversación",
      agentsResponding: "Los agentes están respondiendo en tiempo real",
    },
    
    // Conexión
    connection: {
      connected: "Conectado",
      disconnected: "Desconectado",
      connecting: "Conectando...",
      reconnecting: "Reconectando...",
      connectionError: "Error de conexión",
      retrying: "Reintentando...",
    },
    
    // Suscripciones
    subscription: {
      plan: "Plan",
      free: "Gratuito",
      premium: "Premium",
      admin: "Administrador",
      upgrade: "Actualizar Plan",
      downgrade: "Cambiar Plan",
      currentPlan: "Plan Actual",
      features: "Características",
      pricing: "Precios",
      monthlyQueries: "Consultas Mensuales",
      unlimited: "Ilimitado",
      queriesRemaining: "Consultas Restantes",
      queriesUsed: "Consultas Utilizadas",
      limitReached: "Límite alcanzado",
      upgradeRequired: "Actualización requerida",
    },
    
    // Configuración
    settings: {
      title: "Configuración",
      general: "General",
      appearance: "Apariencia",
      language: "Idioma",
      theme: "Tema",
      notifications: "Notificaciones",
      privacy: "Privacidad",
      security: "Seguridad",
      account: "Cuenta",
      apiKeys: "Claves API",
      model: "Modelo",
      temperature: "Temperatura",
      maxTokens: "Tokens Máximos",
      save: "Guardar",
      cancel: "Cancelar",
      reset: "Restablecer",
      apply: "Aplicar",
    },
    
    // Temas
    themes: {
      executive: "Ejecutivo",
      blueprint: "Plano Técnico",
      ironMan: "Iron Man",
      kawai: "Kawaii",
      cyborg: "Cyborg",
      matrix: "Matrix",
      gamerRgb: "Gamer RGB",
      corporativoVip: "Corporativo VIP",
      criminologia: "Criminología",
      blancoSimple: "Blanco Simple",
      selectTheme: "Seleccionar Tema",
      currentTheme: "Tema Actual",
    },
    
    // Administración
    admin: {
      title: "Panel de Administración",
      users: "Usuarios",
      createUser: "Crear Usuario",
      editUser: "Editar Usuario",
      deleteUser: "Eliminar Usuario",
      userManagement: "Gestión de Usuarios",
      statistics: "Estadísticas",
      totalUsers: "Usuarios Totales",
      activeUsers: "Usuarios Activos",
      totalQueries: "Consultas Totales",
      systemHealth: "Estado del Sistema",
      role: "Rol",
      status: "Estado",
      active: "Activo",
      inactive: "Inactivo",
      createdAt: "Creado el",
      lastLogin: "Último acceso",
    },
    
    // Errores
    errors: {
      generic: "Ha ocurrido un error",
      network: "Error de red",
      timeout: "Tiempo de espera agotado",
      unauthorized: "No autorizado",
      forbidden: "Acceso denegado",
      notFound: "No encontrado",
      serverError: "Error del servidor",
      validationError: "Error de validación",
      tryAgain: "Intentar de nuevo",
      contactSupport: "Contactar soporte",
    },
    
    // Mensajes
    messages: {
      success: "Operación exitosa",
      saved: "Guardado correctamente",
      deleted: "Eliminado correctamente",
      updated: "Actualizado correctamente",
      copied: "Copiado al portapapeles",
      loading: "Cargando...",
      processing: "Procesando...",
      pleaseWait: "Por favor espera...",
      confirm: "Confirmar",
      confirmDelete: "¿Estás seguro de que deseas eliminar?",
      cannotUndo: "Esta acción no se puede deshacer",
    },
    
    // Botones
    buttons: {
      ok: "Aceptar",
      cancel: "Cancelar",
      close: "Cerrar",
      save: "Guardar",
      delete: "Eliminar",
      edit: "Editar",
      create: "Crear",
      update: "Actualizar",
      submit: "Enviar",
      back: "Volver",
      next: "Siguiente",
      previous: "Anterior",
      finish: "Finalizar",
      retry: "Reintentar",
    },
  },
  
  en: {
    // Authentication
    auth: {
      login: "Login",
      register: "Sign Up",
      logout: "Logout",
      username: "Username",
      email: "Email",
      password: "Password",
      confirmPassword: "Confirm Password",
      forgotPassword: "Forgot your password?",
      createAccount: "Create Account",
      alreadyHaveAccount: "Already have an account?",
      dontHaveAccount: "Don't have an account?",
      loginSuccess: "Successfully logged in",
      registerSuccess: "Account created successfully",
      invalidCredentials: "Invalid credentials",
      userCode: "User Code",
    },
    
    // Navigation
    nav: {
      home: "Home",
      agents: "Agents",
      conversations: "Conversations",
      settings: "Settings",
      admin: "Administration",
      profile: "Profile",
      help: "Help",
    },
    
    // Agents
    agents: {
      title: "AI Agents",
      selectAgents: "Select Agents",
      selectedAgents: "Selected Agents",
      noAgentsSelected: "No agents selected",
      selectAtLeast: "Select at least one agent",
      maxAgents: "Maximum agents reached",
      availableAgents: "Available Agents",
      level: "Level",
      specialty: "Specialty",
      description: "Description",
      clearSelection: "Clear Selection",
      selectAll: "Select All",
    },
    
    // Chat
    chat: {
      typeMessage: "Type your message...",
      send: "Send",
      thinking: "Thinking...",
      processing: "Processing...",
      newConversation: "New Conversation",
      saveConversation: "Save Conversation",
      deleteConversation: "Delete Conversation",
      exportConversation: "Export Conversation",
      conversationHistory: "Conversation History",
      noMessages: "No messages",
      startConversation: "Start a conversation",
      agentsResponding: "Agents are responding in real-time",
    },
    
    // Connection
    connection: {
      connected: "Connected",
      disconnected: "Disconnected",
      connecting: "Connecting...",
      reconnecting: "Reconnecting...",
      connectionError: "Connection error",
      retrying: "Retrying...",
    },
    
    // Subscriptions
    subscription: {
      plan: "Plan",
      free: "Free",
      premium: "Premium",
      admin: "Administrator",
      upgrade: "Upgrade Plan",
      downgrade: "Change Plan",
      currentPlan: "Current Plan",
      features: "Features",
      pricing: "Pricing",
      monthlyQueries: "Monthly Queries",
      unlimited: "Unlimited",
      queriesRemaining: "Queries Remaining",
      queriesUsed: "Queries Used",
      limitReached: "Limit reached",
      upgradeRequired: "Upgrade required",
    },
    
    // Settings
    settings: {
      title: "Settings",
      general: "General",
      appearance: "Appearance",
      language: "Language",
      theme: "Theme",
      notifications: "Notifications",
      privacy: "Privacy",
      security: "Security",
      account: "Account",
      apiKeys: "API Keys",
      model: "Model",
      temperature: "Temperature",
      maxTokens: "Max Tokens",
      save: "Save",
      cancel: "Cancel",
      reset: "Reset",
      apply: "Apply",
    },
    
    // Themes
    themes: {
      executive: "Executive",
      blueprint: "Blueprint",
      ironMan: "Iron Man",
      kawai: "Kawaii",
      cyborg: "Cyborg",
      matrix: "Matrix",
      gamerRgb: "Gamer RGB",
      corporativoVip: "Corporate VIP",
      criminologia: "Criminology",
      blancoSimple: "Simple White",
      selectTheme: "Select Theme",
      currentTheme: "Current Theme",
    },
    
    // Administration
    admin: {
      title: "Administration Panel",
      users: "Users",
      createUser: "Create User",
      editUser: "Edit User",
      deleteUser: "Delete User",
      userManagement: "User Management",
      statistics: "Statistics",
      totalUsers: "Total Users",
      activeUsers: "Active Users",
      totalQueries: "Total Queries",
      systemHealth: "System Health",
      role: "Role",
      status: "Status",
      active: "Active",
      inactive: "Inactive",
      createdAt: "Created at",
      lastLogin: "Last login",
    },
    
    // Errors
    errors: {
      generic: "An error occurred",
      network: "Network error",
      timeout: "Request timeout",
      unauthorized: "Unauthorized",
      forbidden: "Access denied",
      notFound: "Not found",
      serverError: "Server error",
      validationError: "Validation error",
      tryAgain: "Try again",
      contactSupport: "Contact support",
    },
    
    // Messages
    messages: {
      success: "Operation successful",
      saved: "Saved successfully",
      deleted: "Deleted successfully",
      updated: "Updated successfully",
      copied: "Copied to clipboard",
      loading: "Loading...",
      processing: "Processing...",
      pleaseWait: "Please wait...",
      confirm: "Confirm",
      confirmDelete: "Are you sure you want to delete?",
      cannotUndo: "This action cannot be undone",
    },
    
    // Buttons
    buttons: {
      ok: "OK",
      cancel: "Cancel",
      close: "Close",
      save: "Save",
      delete: "Delete",
      edit: "Edit",
      create: "Create",
      update: "Update",
      submit: "Submit",
      back: "Back",
      next: "Next",
      previous: "Previous",
      finish: "Finish",
      retry: "Retry",
    },
  },
};

// Hook para usar traducciones
export function useTranslations(lang: Language = "es") {
  return translations[lang];
}

// Función helper para obtener traducción
export function t(key: string, lang: Language = "es"): string {
  const keys = key.split(".");
  let value: any = translations[lang];
  
  for (const k of keys) {
    value = value?.[k];
    if (value === undefined) return key;
  }
  
  return value || key;
}
