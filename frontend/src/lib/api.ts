"use client";

const API_URL = process.env.NEXT_PUBLIC_API_URL || "http://localhost:8001";

// ============================================================================
// TIPOS AFW v0.5.0 - 120 Agentes en 12 Categorías
// ============================================================================

export interface Agent {
    id: string;
    name: string;
    category: string;
    description: string;
    emoji: string;
    capabilities: string[];
    specialization: string;
    complexity: string;
}

export interface Category {
    id: string;
    name: string;
    emoji: string;
    description: string;
    color: string;
    agents_count: number;
    agents?: Agent[];
}

export interface AgentsResponse {
    agents: Agent[];
    total: number;
}

export interface CategoriesResponse {
    categories: Category[];
    total: number;
}

/**
 * Fetch wrapper handling Authentication headers and 401 Expiration
 */
export const fetchWithAuth = async (endpoint: string, options: RequestInit = {}) => {
    const token = localStorage.getItem("atp_token");

    const headers = {
        "Content-Type": "application/json",
        ...(token ? { "Authorization": `Bearer ${token}` } : {}),
        ...options.headers,
    };

    const response = await fetch(`${API_URL}${endpoint}`, {
        ...options,
        headers,
    });

    if (response.status === 401) {
        window.dispatchEvent(new Event("auth:logout"));
        throw new Error("Session expired");
    }

    return response;
};

// ============================================================================
// API FUNCTIONS - AFW v0.5.0
// ============================================================================

/**
 * Get all 120 agents, optionally filtered by category
 */
export const getAgents = async (category?: string): Promise<AgentsResponse> => {
    const url = category ? `/api/agents?category=${category}` : "/api/agents";
    const response = await fetchWithAuth(url);
    return response.json();
};

/**
 * Get all 12 categories
 */
export const getCategories = async (): Promise<CategoriesResponse> => {
    const response = await fetchWithAuth("/api/categories");
    return response.json();
};

/**
 * Get a specific category with its agents
 */
export const getCategory = async (categoryId: string): Promise<Category> => {
    const response = await fetchWithAuth(`/api/categories/${categoryId}`);
    return response.json();
};

/**
 * Get a specific agent
 */
export const getAgent = async (agentId: string): Promise<Agent> => {
    const response = await fetchWithAuth(`/api/agents/${agentId}`);
    return response.json();
};

// ============================================================================
// CONVERSATION API - AFW v0.8.0 (Persistencia de Chat)
// ============================================================================

export interface Conversation {
    conversation_id: string;
    title: string;
    created_at: string;
    updated_at: string;
    message_count: number;
    model?: string;
    agents?: string;
    is_pinned: boolean;
    is_archived: boolean;
}

export interface Message {
    message_id: string;
    role: 'user' | 'assistant';
    content: string;
    agent_id?: string;
    timestamp: string;
    metadata?: {
        agent_name?: string;
        level?: number;
        sections?: any[];
    };
}

export interface ConversationsResponse {
    success: boolean;
    conversations: Conversation[];
    total: number;
}

export interface ConversationMessagesResponse {
    success: boolean;
    conversation_id: string;
    messages: Message[];
    total_messages: number;
}

/**
 * Get conversations for a client
 */
export const getConversations = async (clientId: string, limit = 50, offset = 0): Promise<ConversationsResponse> => {
    const response = await fetch(`${API_URL}/api/chat/conversations?client_id=${clientId}&limit=${limit}&offset=${offset}`);
    return response.json();
};

/**
 * Get a specific conversation with messages
 */
export const getConversation = async (conversationId: string): Promise<ConversationMessagesResponse> => {
    const response = await fetch(`${API_URL}/api/chat/conversations/${conversationId}`);
    return response.json();
};

/**
 * Delete a conversation
 */
export const deleteConversation = async (conversationId: string): Promise<{ success: boolean }> => {
    const response = await fetch(`${API_URL}/api/chat/conversations/${conversationId}`, {
        method: 'DELETE'
    });
    return response.json();
};

/**
 * Archive a conversation
 */
export const archiveConversation = async (conversationId: string, archived = true): Promise<{ success: boolean }> => {
    const response = await fetch(`${API_URL}/api/chat/conversations/${conversationId}/archive?archived=${archived}`, {
        method: 'POST'
    });
    return response.json();
};

/**
 * Update conversation title
 */
export const updateConversationTitle = async (conversationId: string, title: string): Promise<{ success: boolean }> => {
    const response = await fetch(`${API_URL}/api/chat/conversations/${conversationId}/title?title=${encodeURIComponent(title)}`, {
        method: 'PUT'
    });
    return response.json();
};

/**
 * Search conversations
 */
export const searchConversations = async (clientId: string, query: string, limit = 20): Promise<{ success: boolean; results: Conversation[]; total: number }> => {
    const response = await fetch(`${API_URL}/api/chat/search?client_id=${clientId}&q=${encodeURIComponent(query)}&limit=${limit}`);
    return response.json();
};
