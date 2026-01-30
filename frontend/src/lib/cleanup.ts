/**
 * Limpieza de datos para lanzamiento público
 * Solo el propietario debe tener acceso a conversaciones anteriores
 */

export const cleanupUserData = () => {
  // Limpiar localStorage SOLO del sistema antiguo
  const keysToRemove = [
    'afw_conversations',        // Sistema antiguo
    'afw_current_conversation', // Sistema antiguo
    'afw-api-providers',       // Configuración API temporal
    'afw_settings'             // Settings antiguos
  ];
  
  keysToRemove.forEach(key => {
    localStorage.removeItem(key);
  });
  
  // 🔥 IMPORTANTE: NO eliminar claves del nuevo sistema
  // 'afw_anonymous_user' - ID de usuario
  // 'afw_user_conversations' - Conversaciones por usuario
  
  // Limpiar sessionStorage
  sessionStorage.clear();
  
  console.log('🧹 Sistema antiguo limpiado, nuevo sistema preservado');
};

export const resetForPublicLaunch = () => {
  cleanupUserData();
  
  // Mostrar mensaje de bienvenida para nuevos usuarios
  console.log('🚀 AFW Platform - Listo para lanzamiento público');
  console.log('📝 Todos los datos anteriores han sido eliminados');
  console.log('🔒 Solo el propietario tiene acceso a conversaciones anteriores');
};
