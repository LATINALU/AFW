/**
 * Conversation Storage System - AFW v0.8.0
 * ==========================================
 * Sistema de almacenamiento híbrido de conversaciones
 * con persistencia en localStorage + sincronización con servidor.
 */

import { 
  getConversations as apiGetConversations,
  getConversation as apiGetConversation,
  deleteConversation as apiDeleteConversation,
  updateConversationTitle as apiUpdateTitle,
  Conversation as ServerConversation,
  Message as ServerMessage
} from "./api";

export interface StoredMessage {
  role: "user" | "assistant";
  content: string;
  agentResponses?: any[];
  timestamp: string;
  agent_id?: string;
  metadata?: any;
}

export interface Conversation {
  id: string;
  title: string;
  messages: StoredMessage[];
  createdAt: string;
  updatedAt: string;
  model: string;
  agents: string[];
}

const STORAGE_KEY = "afw_conversations";
const CURRENT_CONVERSATION_KEY = "afw_current_conversation";
const CLIENT_ID_KEY = "afw_client_id";

// Obtener o crear client_id persistente
export function getClientId(): string {
  if (typeof window === 'undefined') return 'server';
  let clientId = localStorage.getItem(CLIENT_ID_KEY);
  if (!clientId) {
    clientId = `client_${Date.now()}_${Math.random().toString(36).substr(2, 9)}`;
    localStorage.setItem(CLIENT_ID_KEY, clientId);
  }
  return clientId;
}

export class ConversationStorage {
  /**
   * Obtener todas las conversaciones guardadas
   */
  static getAllConversations(): Conversation[] {
    try {
      const stored = localStorage.getItem(STORAGE_KEY);
      return stored ? JSON.parse(stored) : [];
    } catch (error) {
      console.error("Error loading conversations:", error);
      return [];
    }
  }

  /**
   * Guardar una conversación
   */
  static saveConversation(conversation: Conversation): void {
    try {
      const conversations = this.getAllConversations();
      const existingIndex = conversations.findIndex(c => c.id === conversation.id);
      
      if (existingIndex >= 0) {
        conversations[existingIndex] = {
          ...conversation,
          updatedAt: new Date().toISOString()
        };
      } else {
        conversations.push(conversation);
      }
      
      localStorage.setItem(STORAGE_KEY, JSON.stringify(conversations));
    } catch (error) {
      console.error("Error saving conversation:", error);
    }
  }

  /**
   * Obtener una conversación por ID
   */
  static getConversation(id: string): Conversation | null {
    const conversations = this.getAllConversations();
    return conversations.find(c => c.id === id) || null;
  }

  /**
   * Eliminar una conversación
   */
  static deleteConversation(id: string): void {
    try {
      const conversations = this.getAllConversations();
      const filtered = conversations.filter(c => c.id !== id);
      localStorage.setItem(STORAGE_KEY, JSON.stringify(filtered));
    } catch (error) {
      console.error("Error deleting conversation:", error);
    }
  }

  /**
   * Crear una nueva conversación
   */
  static createConversation(model: string, agents: string[]): Conversation {
    return {
      id: `conv_${Date.now()}_${Math.random().toString(36).substr(2, 9)}`,
      title: `Nueva conversación - ${new Date().toLocaleString()}`,
      messages: [],
      createdAt: new Date().toISOString(),
      updatedAt: new Date().toISOString(),
      model,
      agents
    };
  }

  /**
   * Actualizar el título de una conversación
   */
  static updateConversationTitle(id: string, title: string): void {
    try {
      const conversations = this.getAllConversations();
      const conversation = conversations.find(c => c.id === id);
      
      if (conversation) {
        conversation.title = title;
        conversation.updatedAt = new Date().toISOString();
        localStorage.setItem(STORAGE_KEY, JSON.stringify(conversations));
      }
    } catch (error) {
      console.error("Error updating conversation title:", error);
    }
  }

  /**
   * Obtener la conversación actual
   */
  static getCurrentConversationId(): string | null {
    return localStorage.getItem(CURRENT_CONVERSATION_KEY);
  }

  /**
   * Establecer la conversación actual
   */
  static setCurrentConversationId(id: string): void {
    localStorage.setItem(CURRENT_CONVERSATION_KEY, id);
  }

  /**
   * Exportar conversación a JSON
   */
  static exportToJSON(conversation: Conversation): string {
    return JSON.stringify(conversation, null, 2);
  }

  /**
   * Exportar conversación a Markdown
   */
  static exportToMarkdown(conversation: Conversation): string {
    let markdown = `# ${conversation.title}\n\n`;
    markdown += `**Fecha:** ${new Date(conversation.createdAt).toLocaleString()}\n`;
    markdown += `**Modelo:** ${conversation.model}\n`;
    markdown += `**Agentes:** ${conversation.agents.join(", ")}\n\n`;
    markdown += `---\n\n`;

    conversation.messages.forEach((message, index) => {
      if (message.role === "user") {
        markdown += `## 👤 Usuario\n\n${message.content}\n\n`;
      } else {
        markdown += `## 🤖 Asistente\n\n`;
        
        if (message.agentResponses && message.agentResponses.length > 0) {
          message.agentResponses.forEach((response, idx) => {
            markdown += `### ${response.agent_name}\n\n`;
            markdown += `${response.raw_content || response.summary || message.content}\n\n`;
            if (idx < message.agentResponses!.length - 1) {
              markdown += `---\n\n`;
            }
          });
        } else {
          markdown += `${message.content}\n\n`;
        }
      }
      
      markdown += `---\n\n`;
    });

    return markdown;
  }

  /**
   * Descargar conversación como archivo
   */
  static downloadConversation(conversation: Conversation, format: 'json' | 'markdown'): void {
    const content = format === 'json' 
      ? this.exportToJSON(conversation)
      : this.exportToMarkdown(conversation);
    
    const blob = new Blob([content], { type: format === 'json' ? 'application/json' : 'text/markdown' });
    const url = URL.createObjectURL(blob);
    const a = document.createElement('a');
    a.href = url;
    a.download = `${conversation.title.replace(/[^a-z0-9]/gi, '_')}.${format === 'json' ? 'json' : 'md'}`;
    document.body.appendChild(a);
    a.click();
    document.body.removeChild(a);
    URL.revokeObjectURL(url);
  }

  /**
   * Limpiar conversaciones antiguas (mantener últimas N)
   */
  static cleanOldConversations(keepCount: number = 50): void {
    try {
      const conversations = this.getAllConversations();
      
      if (conversations.length > keepCount) {
        // Ordenar por fecha de actualización (más recientes primero)
        conversations.sort((a, b) => 
          new Date(b.updatedAt).getTime() - new Date(a.updatedAt).getTime()
        );
        
        // Mantener solo las más recientes
        const toKeep = conversations.slice(0, keepCount);
        localStorage.setItem(STORAGE_KEY, JSON.stringify(toKeep));
      }
    } catch (error) {
      console.error("Error cleaning old conversations:", error);
    }
  }

  // ============== MÉTODOS DE SINCRONIZACIÓN CON SERVIDOR ==============

  /**
   * Obtener conversaciones del servidor
   */
  static async getServerConversations(): Promise<Conversation[]> {
    try {
      const clientId = getClientId();
      const response = await apiGetConversations(clientId);
      
      if (response.success && response.conversations) {
        return response.conversations.map((conv: ServerConversation) => ({
          id: conv.conversation_id,
          title: conv.title,
          messages: [],
          createdAt: conv.created_at,
          updatedAt: conv.updated_at,
          model: conv.model || '',
          agents: conv.agents ? JSON.parse(conv.agents) : []
        }));
      }
      return [];
    } catch (error) {
      console.error("Error getting server conversations:", error);
      return [];
    }
  }

  /**
   * Obtener mensajes de una conversación del servidor
   */
  static async getServerConversationMessages(conversationId: string): Promise<StoredMessage[]> {
    try {
      const response = await apiGetConversation(conversationId);
      
      if (response.success && response.messages) {
        return response.messages.map((msg: ServerMessage) => ({
          role: msg.role,
          content: msg.content,
          timestamp: msg.timestamp,
          agent_id: msg.agent_id,
          metadata: msg.metadata,
          agentResponses: msg.metadata?.sections || []
        }));
      }
      return [];
    } catch (error) {
      console.error("Error getting conversation messages:", error);
      return [];
    }
  }

  /**
   * Eliminar conversación del servidor
   */
  static async deleteServerConversation(conversationId: string): Promise<boolean> {
    try {
      const response = await apiDeleteConversation(conversationId);
      return response.success;
    } catch (error) {
      console.error("Error deleting server conversation:", error);
      return false;
    }
  }

  /**
   * Actualizar título en servidor
   */
  static async updateServerConversationTitle(conversationId: string, title: string): Promise<boolean> {
    try {
      const response = await apiUpdateTitle(conversationId, title);
      return response.success;
    } catch (error) {
      console.error("Error updating server conversation title:", error);
      return false;
    }
  }

  /**
   * Sincronizar conversaciones locales con servidor
   */
  static async syncWithServer(): Promise<Conversation[]> {
    try {
      const serverConversations = await this.getServerConversations();
      const localConversations = this.getAllConversations();
      
      // Combinar conversaciones (servidor tiene prioridad)
      const merged = new Map<string, Conversation>();
      
      // Agregar locales primero
      localConversations.forEach(conv => merged.set(conv.id, conv));
      
      // Agregar/sobrescribir con las del servidor
      serverConversations.forEach(conv => {
        const existing = merged.get(conv.id);
        if (!existing || new Date(conv.updatedAt) > new Date(existing.updatedAt)) {
          merged.set(conv.id, conv);
        }
      });
      
      const allConversations = Array.from(merged.values());
      
      // Ordenar por fecha de actualización
      allConversations.sort((a, b) => 
        new Date(b.updatedAt).getTime() - new Date(a.updatedAt).getTime()
      );
      
      return allConversations;
    } catch (error) {
      console.error("Error syncing with server:", error);
      return this.getAllConversations();
    }
  }
}
