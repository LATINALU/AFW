/**
 * Sistema de Almacenamiento para Usuarios Anónimos
 * AFW Platform - Lanzamiento Público
 */

interface UserSession {
  userId: string;
  createdAt: string;
  lastActive: string;
  conversationCount: number;
  userAgent: string;
  ip?: string;
}

export interface Conversation {
  id: string;
  userId: string;
  title: string;
  messages: Array<{
    role: string;
    content: string;
    timestamp: string;
    agentResponses?: any[];
  }>;
  createdAt: string;
  updatedAt: string;
  model: string;
  agents: string[];
}

class UserStorageManager {
  private static instance: UserStorageManager;
  private currentUserId: string | null = null;
  private readonly USER_KEY = 'afw_anonymous_user';
  private readonly CONVERSATIONS_KEY = 'afw_user_conversations';

  static getInstance(): UserStorageManager {
    if (!UserStorageManager.instance) {
      UserStorageManager.instance = new UserStorageManager();
    }
    return UserStorageManager.instance;
  }

  // 🆔 Obtener o crear ID de usuario anónimo
  getUserId(): string {
    if (!this.currentUserId) {
      let userData = localStorage.getItem(this.USER_KEY);
      
      if (!userData) {
        // Nuevo usuario
        const newUser: UserSession = {
          userId: `user_${Date.now()}_${Math.random().toString(36).substr(2, 9)}`,
          createdAt: new Date().toISOString(),
          lastActive: new Date().toISOString(),
          conversationCount: 0,
          userAgent: navigator.userAgent.substring(0, 100)
        };
        
        localStorage.setItem(this.USER_KEY, JSON.stringify(newUser));
        this.currentUserId = newUser.userId;
        
        console.log('👤 Nuevo usuario creado:', newUser.userId);
      } else {
        // Usuario existente
        const user: UserSession = JSON.parse(userData);
        this.currentUserId = user.userId;
        
        // Actualizar última actividad
        user.lastActive = new Date().toISOString();
        localStorage.setItem(this.USER_KEY, JSON.stringify(user));
        
        console.log('🔄 Usuario existente:', user.userId);
      }
    }
    
    return this.currentUserId!;
  }

  // 💾 Guardar conversación
  saveConversation(conversation: Omit<Conversation, 'userId'>): void {
    const userId = this.getUserId();
    const fullConversation: Conversation = {
      ...conversation,
      userId
    };

    // Obtener conversaciones existentes
    const allConversations = this.getAllConversations();
    
    // Buscar si ya existe
    const existingIndex = allConversations.findIndex(c => c.id === conversation.id);
    
    if (existingIndex >= 0) {
      // Actualizar existente
      allConversations[existingIndex] = fullConversation;
      console.log('📝 Conversación actualizada:', conversation.id);
    } else {
      // Agregar nueva
      allConversations.push(fullConversation);
      
      // Incrementar contador de conversaciones del usuario
      this.incrementConversationCount();
      console.log('🆕 Nueva conversación creada:', conversation.id);
    }

    // Guardar en localStorage
    localStorage.setItem(this.CONVERSATIONS_KEY, JSON.stringify(allConversations));
    
    // 🔍 Depuración
    console.log('💾 Conversación guardada:', {
      id: conversation.id,
      userId: userId,
      totalMessages: conversation.messages.length,
      totalConversations: allConversations.length,
      storageKey: this.CONVERSATIONS_KEY
    });
    
    // Verificar que se guardó correctamente
    const saved = localStorage.getItem(this.CONVERSATIONS_KEY);
    if (saved) {
      const parsed = JSON.parse(saved);
      console.log('✅ Verificación:', {
        storedConversations: parsed.length,
        userConversations: parsed.filter((c: any) => c.userId === userId).length
      });
    }
  }

  // 📋 Obtener todas las conversaciones del usuario
  getUserConversations(): Conversation[] {
    const userId = this.getUserId();
    const allConversations = this.getAllConversations();
    
    return allConversations.filter(c => c.userId === userId);
  }

  // 🗑️ Eliminar conversación
  deleteConversation(conversationId: string): void {
    const userId = this.getUserId();
    const allConversations = this.getAllConversations();
    
    const filtered = allConversations.filter(c => 
      !(c.id === conversationId && c.userId === userId)
    );
    
    localStorage.setItem(this.CONVERSATIONS_KEY, JSON.stringify(filtered));
    
    console.log('🗑️ Conversación eliminada:', conversationId);
  }

  // 📊 Estadísticas del usuario
  getUserStats(): UserSession | null {
    const userData = localStorage.getItem(this.USER_KEY);
    return userData ? JSON.parse(userData) : null;
  }

  // 🧹 Limpiar datos del usuario (para logout)
  clearUserData(): void {
    const userId = this.getUserId();
    const allConversations = this.getAllConversations();
    
    // Eliminar solo las conversaciones de este usuario
    const otherUsersConversations = allConversations.filter(c => c.userId !== userId);
    localStorage.setItem(this.CONVERSATIONS_KEY, JSON.stringify(otherUsersConversations));
    
    // Eliminar sesión de usuario
    localStorage.removeItem(this.USER_KEY);
    
    this.currentUserId = null;
    
    console.log('🧹 Datos del usuario eliminados:', userId);
  }

  // 🔧 Métodos privados
  private getAllConversations(): Conversation[] {
    const data = localStorage.getItem(this.CONVERSATIONS_KEY);
    return data ? JSON.parse(data) : [];
  }

  private incrementConversationCount(): void {
    const userData = localStorage.getItem(this.USER_KEY);
    if (userData) {
      const user: UserSession = JSON.parse(userData);
      user.conversationCount++;
      user.lastActive = new Date().toISOString();
      localStorage.setItem(this.USER_KEY, JSON.stringify(user));
    }
  }
}

export default UserStorageManager.getInstance();
