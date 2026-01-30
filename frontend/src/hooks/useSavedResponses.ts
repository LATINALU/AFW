/**
 * useSavedResponses Hook v1.0.0
 * ==============================
 * Hook para gestionar el guardado de respuestas de agentes.
 */

import { useState, useCallback } from 'react';

interface SavedResponse {
  response_id: string;
  agent_id: string;
  agent_name: string;
  content: string;
  title: string;
  tags: string[];
  category: string;
  created_at: string;
  is_favorite: boolean;
}

interface SaveResponseData {
  agentId: string;
  agentName: string;
  content: string;
  conversationId?: string;
  messageId?: string;
  title?: string;
  tags?: string[];
  category?: string;
}

export function useSavedResponses() {
  const [savedResponses, setSavedResponses] = useState<SavedResponse[]>([]);
  const [loading, setLoading] = useState(false);
  const [error, setError] = useState<string | null>(null);

  const saveResponse = useCallback(async (data: SaveResponseData) => {
    setLoading(true);
    setError(null);

    try {
      const token = localStorage.getItem('token');
      const response = await fetch('/api/conversations/responses/save', {
        method: 'POST',
        headers: {
          'Authorization': `Bearer ${token}`,
          'Content-Type': 'application/json',
        },
        body: JSON.stringify({
          agent_id: data.agentId,
          agent_name: data.agentName,
          content: data.content,
          title: data.title || `Respuesta de ${data.agentName}`,
          conversation_id: data.conversationId,
          message_id: data.messageId,
          tags: data.tags || [],
          category: data.category || 'General',
        }),
      });

      if (!response.ok) {
        throw new Error('Error al guardar respuesta');
      }

      const result = await response.json();
      
      if (result.success) {
        // Actualizar estado local
        const newResponse: SavedResponse = {
          response_id: result.response_id,
          agent_id: data.agentId,
          agent_name: data.agentName,
          content: data.content,
          title: result.title || `Respuesta de ${data.agentName}`,
          tags: data.tags || [],
          category: data.category || 'General',
          created_at: new Date().toISOString(),
          is_favorite: false,
        };

        setSavedResponses(prev => [newResponse, ...prev]);
        return result.response_id;
      } else {
        throw new Error(result.message || 'Error desconocido');
      }
    } catch (err) {
      const errorMessage = err instanceof Error ? err.message : 'Error desconocido';
      setError(errorMessage);
      throw err;
    } finally {
      setLoading(false);
    }
  }, []);

  const getSavedResponses = useCallback(async (category?: string) => {
    setLoading(true);
    setError(null);

    try {
      const token = localStorage.getItem('token');
      const url = category 
        ? `/api/conversations/responses/list?category=${encodeURIComponent(category)}`
        : '/api/conversations/responses/list';

      const response = await fetch(url, {
        headers: {
          'Authorization': `Bearer ${token}`,
        },
      });

      if (!response.ok) {
        throw new Error('Error al obtener respuestas guardadas');
      }

      const result = await response.json();
      
      if (result.success) {
        setSavedResponses(result.responses || []);
        return result.responses;
      } else {
        throw new Error(result.message || 'Error desconocido');
      }
    } catch (err) {
      const errorMessage = err instanceof Error ? err.message : 'Error desconocido';
      setError(errorMessage);
      throw err;
    } finally {
      setLoading(false);
    }
  }, []);

  const deleteSavedResponse = useCallback(async (responseId: string) => {
    setLoading(true);
    setError(null);

    try {
      const token = localStorage.getItem('token');
      const response = await fetch(`/api/conversations/responses/${responseId}`, {
        method: 'DELETE',
        headers: {
          'Authorization': `Bearer ${token}`,
        },
      });

      if (!response.ok) {
        throw new Error('Error al eliminar respuesta');
      }

      const result = await response.json();
      
      if (result.success) {
        setSavedResponses(prev => prev.filter(r => r.response_id !== responseId));
        return true;
      } else {
        throw new Error(result.message || 'Error desconocido');
      }
    } catch (err) {
      const errorMessage = err instanceof Error ? err.message : 'Error desconocido';
      setError(errorMessage);
      throw err;
    } finally {
      setLoading(false);
    }
  }, []);

  const isResponseSaved = useCallback((content: string, agentId: string) => {
    return savedResponses.some(
      response => response.content === content && response.agent_id === agentId
    );
  }, [savedResponses]);

  return {
    savedResponses,
    loading,
    error,
    saveResponse,
    getSavedResponses,
    deleteSavedResponse,
    isResponseSaved,
    clearError: () => setError(null),
  };
}
