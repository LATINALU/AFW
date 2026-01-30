"use client";

/**
 * StreamingChat v0.9.0 - Sistema de Respuestas Especializadas
 * ==========================================================
 * Interfaz de chat con streaming en tiempo real y diseño responsive.
 * Diseño limpio y conversacional similar a Gemini y ChatGPT.
 * + Persistencia de conversaciones con SecureStorage
 * + Memoria contextual entre preguntas
 * + Historial de conversaciones con exportación
 * + Diseño responsive para móviles y tablets
 * + Indicador de conexión en tiempo real
 * + **NUEVO**: Respuestas especializadas por tipo de agente (10 tipos)
 * + **NUEVO**: Visualización diferenciada por categoría
 */

import React, { useState, useEffect, useRef, useCallback } from "react";
import { cn } from "@/lib/utils";
import { getCurrentLanguage } from "@/lib/i18n";
import { Button } from "@/components/ui/button";
import { Badge } from "@/components/ui/badge";
import ReactMarkdown from "react-markdown";
import {
  ChevronLeft,
  ChevronRight,
  Layers,
  User,
  Sparkles,
  Wifi,
  WifiOff,
  X,
  Menu,
  Brain,
  Save,
  Send,
  Loader2,
  AlertCircle,
} from "lucide-react";
import { AgentCard } from "@/components/AgentCard";
import { ConversationHistory } from "@/components/ConversationHistory";
import { TaskSelector } from "@/components/TaskSelector";
import { ConversationStorage } from "@/lib/conversationStorage";
import userStorage from "@/lib/userStorage";
// === NUEVO: Componente de respuesta especializada por tipo de agente ===
import { SpecializedAgentResponse } from "@/components/SpecializedAgentResponse";

interface Agent {
  id: string;
  name: string;
  role: string;
  level: number;
  emoji?: string;
  specialty?: string;
  description?: string;
}

interface Message {
  role: "user" | "assistant" | "agent";
  content: string;
  timestamp: Date;
  agentResponse?: any;
  agentName?: string;
  agentEmoji?: string;
}

interface AgentResponse {
  agent_id: string;
  agent_name: string;
  agent_emoji?: string;
  level?: number;
  specialty?: string;
  raw_content?: string;
  summary?: string;
  sections?: Array<{
    type: string;
    title?: string;
    content?: string;
    items?: string[];
  }>;
  timestamp: string;
  // === NUEVO: Metadatos de formato especializado ===
  category?: string;      // software_development, marketing, legal, etc.
  format_type?: string;   // code, document, analysis, creative, etc.
  min_words?: number;     // mínimo de palabras esperado
}

interface Conversation {
  id: string;
  title: string;
  messages: Array<{
    role: string;
    content: string;
    timestamp: string;
    agentResponses?: AgentResponse[];
  }>;
  createdAt: string;
  updatedAt: string;
  model: string;
  agents: string[];
}

interface StreamingChatProps {
  selectedAgents: string[];
  model: string;
  apiConfig: any;
  onAgentModelChange: (agentId: string, model: string) => void;
  agentInstructions: Record<string, string>;
  onAgentInstructionsChange: (agentId: string, instructions: string) => void;
  onShowAgentDetails: (agentId: string) => void;
  conversationId?: string | null;
  initialMessages?: any[];
  onConversationSaved?: (id: string, title: string) => void;
  onConnectionChange?: (connected: boolean) => void;
  onSelectPreset?: (agents: string[]) => void;
}

export function StreamingChatV2({
  selectedAgents,
  model,
  apiConfig,
  onAgentModelChange = () => { },
  agentInstructions = {},
  onAgentInstructionsChange = () => { },
  onShowAgentDetails = () => { },
  conversationId = null,
  initialMessages = [],
  onConversationSaved,
  onConnectionChange,
  onSelectPreset,
}: StreamingChatProps) {
  const [input, setInput] = useState("");
  const [isConnected, setIsConnected] = useState(false);
  const [isProcessing, setIsProcessing] = useState(false);
  const [messages, setMessages] = useState<Message[]>([]);
  const [currentAgent, setCurrentAgent] = useState<string | null>(null);
  const [currentProgress, setCurrentProgress] = useState(0);
  const [error, setError] = useState<string | null>(null);
  const [processingAgents, setProcessingAgents] = useState<Set<string>>(new Set());

  // Sistema de persistencia v0.8.0
  const [currentConversationId, setCurrentConversationId] = useState<string | null>(null);
  const [showHistory, setShowHistory] = useState(true);
  const [showMobilePanel, setShowMobilePanel] = useState(false);
  const [autoSave, setAutoSave] = useState(true);

  // Responsive states
  const [isMobile, setIsMobile] = useState(false);
  const [isTablet, setIsTablet] = useState(false);

  const wsRef = useRef<WebSocket | null>(null);
  const clientIdRef = useRef<string>(`client_${Date.now()}_${Math.random().toString(36).substr(2, 9)}`);
  const scrollRef = useRef<HTMLDivElement>(null);

  // Detectar tamaño de pantalla para responsive
  useEffect(() => {
    const checkScreenSize = () => {
      const width = window.innerWidth;
      setIsMobile(width < 768);
      setIsTablet(width >= 768 && width < 1024);
    };

    checkScreenSize();
    window.addEventListener('resize', checkScreenSize);
    return () => window.removeEventListener('resize', checkScreenSize);
  }, []);

  // Efecto para cargar mensajes iniciales (historial) - ELIMINADO para evitar bucle infinito
  // Los mensajes iniciales se cargan en el useEffect de carga de conversación

  // Funciones de gestión de conversaciones (ANTES de useEffect para evitar errores)
  const createNewConversation = useCallback(() => {
    // Limpiar conversación actual del localStorage
    localStorage.removeItem("afw_current_conversation");
    
    // Crear nueva conversación vacía
    const newConversation = {
      id: `conv_${Date.now()}_${Math.random().toString(36).substr(2, 9)}`,
      title: `Nueva conversación - ${new Date().toLocaleString()}`,
      messages: [],
      createdAt: new Date().toISOString(),
      updatedAt: new Date().toISOString(),
      model: model,
      agents: selectedAgents
    };

    setCurrentConversationId(newConversation.id);
    setMessages([]);
    
    console.log('🆕 Nueva conversación creada:', newConversation.id);
  }, [model, selectedAgents]);

  const loadConversationMessages = useCallback((conversation: Conversation) => {
    const loadedMessages: Message[] = conversation.messages.map(msg => ({
      role: msg.role as "user" | "assistant" | "agent",
      content: msg.content,
      agentResponse: msg.agentResponses?.[0],
      agentName: msg.agentResponses?.[0]?.agent_name,
      agentEmoji: msg.agentResponses?.[0]?.agent_emoji,
      timestamp: new Date(msg.timestamp)
    }));
    setMessages(loadedMessages);
  }, []);

  const saveCurrentConversation = useCallback(() => {
    if (!currentConversationId || messages.length === 0) return;

    try {
      // Guardar en localStorage
      const storedMessages: any[] = messages
        .filter(msg => msg.role !== "agent" || msg.agentResponse)
        .map(msg => ({
          role: msg.role,
          content: msg.content,
          timestamp: msg.timestamp.toISOString(),
          agentResponses: msg.agentResponse ? [msg.agentResponse] : undefined
        }));

      const conversation = {
        id: currentConversationId,
        title: messages[0]?.content?.substring(0, 50) || "Nueva conversación",
        messages: storedMessages,
        createdAt: new Date().toISOString(),
        updatedAt: new Date().toISOString(),
        model: model,
        agents: selectedAgents
      };

      // Guardar en localStorage
      const stored = localStorage.getItem("afw_conversations");
      const conversations = stored ? JSON.parse(stored) : [];
      const existingIndex = conversations.findIndex((c: any) => c.id === currentConversationId);
      
      if (existingIndex >= 0) {
        conversations[existingIndex] = conversation;
      } else {
        conversations.push(conversation);
      }
      
      localStorage.setItem("afw_conversations", JSON.stringify(conversations));
      console.log('💾 Conversación guardada en localStorage:', currentConversationId);
    } catch (error) {
      console.error("Error saving conversation:", error);
    }
  }, [currentConversationId, messages, model, selectedAgents]);

  // Auto-save conversación (DESPUÉS de declarar funciones)
  useEffect(() => {
    if (autoSave && currentConversationId && messages.length > 0) {
      const saveTimer = setTimeout(() => {
        saveCurrentConversation();
      }, 2000);

      return () => clearTimeout(saveTimer);
    }
  }, [messages, currentConversationId, saveCurrentConversation, autoSave]);

  // Cargar conversación guardada al montar (si existe)
  useEffect(() => {
    const savedConversationId = localStorage.getItem("afw_current_conversation");
    
    if (savedConversationId) {
      // Intentar cargar conversación guardada
      try {
        const stored = localStorage.getItem("afw_conversations");
        const conversations = stored ? JSON.parse(stored) : [];
        const savedConversation = conversations.find((c: any) => c.id === savedConversationId);
        
        if (savedConversation) {
          setCurrentConversationId(savedConversationId);
          loadConversationMessages(savedConversation);
          console.log('📂 Conversación guardada cargada:', savedConversationId);
        } else {
          // No se encontró la conversación, crear nueva
          createNewConversation();
        }
      } catch (error) {
        console.error("Error loading saved conversation:", error);
        createNewConversation();
      }
    } else {
      // No hay conversación guardada, crear nueva
      createNewConversation();
    }
  }, []); // Sin dependencias para evitar bucle infinito

  const handleSelectConversation = (conversation: Conversation) => {
    setCurrentConversationId(conversation.id);
    localStorage.setItem("afw_current_conversation", conversation.id);
    loadConversationMessages(conversation);
    // On desktop we might want to keep it open, but for now let's not auto-close unless needed
    // setShowHistory(false); 
  };

  const handleDeleteConversation = (id: string) => {
    if (id === currentConversationId) {
      createNewConversation();
    }

    try {
      const stored = localStorage.getItem("afw_conversations");
      const conversations = stored ? JSON.parse(stored) : [];
      const filtered = conversations.filter((c: any) => c.id !== id);
      localStorage.setItem("afw_conversations", JSON.stringify(filtered));
    } catch (error) {
      console.error("Error deleting conversation:", error);
    }
  };

  const connectWebSocket = useCallback(() => {
    const token = localStorage.getItem("afw_ws_token") || localStorage.getItem("afw_token");
    const wsUrl = `ws://${window.location.hostname}:8001/ws/${clientIdRef.current}${token ? `?token=${token}` : ""}`;

    try {
      const ws = new WebSocket(wsUrl);

      ws.onopen = () => {
        console.log("✅ WebSocket conectado");
        setIsConnected(true);
        onConnectionChange?.(true);
        setError(null);
      };

      ws.onclose = () => {
        console.log("📴 WebSocket desconectado");
        setIsConnected(false);
        onConnectionChange?.(false);
        setTimeout(connectWebSocket, 3000);
      };

      ws.onerror = (err) => {
        console.error("❌ WebSocket error:", err);
        setError("Error de conexión. Reintentando...");
      };

      ws.onmessage = (event) => {
        try {
          const data = JSON.parse(event.data);
          handleWebSocketMessage(data);
        } catch (e) {
          console.error("Error parsing WebSocket message:", e);
        }
      };

      wsRef.current = ws;
    } catch (err) {
      console.error("Error conectando WebSocket:", err);
      setError("No se pudo conectar al servidor");
    }
  }, []);

  const handleWebSocketMessage = (data: any) => {
    switch (data.type) {
      case "pipeline_start":
        setIsProcessing(true);
        setProcessingAgents(new Set());
        console.log('🚀 Pipeline iniciado');
        break;

      case "agent_start":
        setCurrentAgent(data.agent);
        setCurrentProgress(0);
        setProcessingAgents(prev => new Set(prev).add(data.agent));
        console.log(`🤖 Agente ${data.agent} iniciando...`);
        break;

      case "agent_progress":
        setCurrentProgress(data.progress);
        break;

      case "agent_response":
        const agentResponse: AgentResponse = data.data;

        setMessages(prev => {
          const newMessage: Message = {
            role: "agent",
            content: agentResponse.raw_content || agentResponse.summary || 'Sin contenido disponible.',
            agentResponse: agentResponse,
            agentName: agentResponse.agent_name,
            agentEmoji: agentResponse.agent_emoji,
            timestamp: new Date()
          };

          return [...prev, newMessage];
        });

        setProcessingAgents(prev => {
          const newSet = new Set(prev);
          newSet.delete(agentResponse.agent_id);
          return newSet;
        });

        setCurrentAgent(null);
        break;

      case "agent_error":
        setError(`Error en ${data.agent}: ${data.error}`);
        setProcessingAgents(prev => {
          const newSet = new Set(prev);
          newSet.delete(data.agent);
          return newSet;
        });
        break;

      case "pipeline_complete":
        console.log('✅ Pipeline completado');
        setIsProcessing(false);
        setCurrentAgent(null);
        setProcessingAgents(new Set());
        break;

      case "conversation_saved":
        if (onConversationSaved) {
          onConversationSaved(data.conversation_id, data.title);
        }
        break;

      default:
        console.log("Mensaje desconocido:", data);
    }
  };

  const sendMessage = async () => {
    if (!input.trim() || !isConnected || isProcessing) return;

    const userMessage: Message = {
      role: "user",
      content: input,
      timestamp: new Date()
    };
    setMessages(prev => [...prev, userMessage]);

    setError(null);

    const message = {
      action: "start_pipeline",
      message: input,
      agents: selectedAgents,
      model: model,
      apiConfig: apiConfig,
      conversation_id: conversationId,
      language: getCurrentLanguage()
    };

    if (wsRef.current && wsRef.current.readyState === WebSocket.OPEN) {
      wsRef.current.send(JSON.stringify(message));
      setIsProcessing(true);
      setInput("");
    } else {
      await sendMessageViaSSE();
    }
  };

  const sendMessageViaSSE = async () => {
    setIsProcessing(true);

    try {
      const response = await fetch("/api/chat-stream", {
        method: "POST",
        headers: { "Content-Type": "application/json" },
        body: JSON.stringify({
          message: input,
          agents: selectedAgents,
          model: model,
          apiConfig: apiConfig
        })
      });

      const reader = response.body?.getReader();
      const decoder = new TextDecoder();

      if (!reader) {
        throw new Error("No se pudo iniciar el streaming");
      }

      while (true) {
        const { done, value } = await reader.read();
        if (done) break;

        const text = decoder.decode(value);
        const lines = text.split("\n");

        for (const line of lines) {
          if (line.startsWith("data: ")) {
            try {
              const data = JSON.parse(line.slice(6));
              handleWebSocketMessage(data);
            } catch (e) {
              console.error("Error parsing SSE data:", e);
            }
          }
        }
      }

      setInput("");
    } catch (err) {
      setError("Error en streaming: " + (err as Error).message);
      setIsProcessing(false);
    }
  };

  const renderAgentResponse = (response: AgentResponse) => {
    const getMainContent = () => {
      if (!response.sections || response.sections.length === 0) {
        return response.raw_content || response.summary || "Sin contenido disponible.";
      }

      const mainSection = response.sections.find(section =>
        section.content && section.content.trim().length > 0
      ) || response.sections[0];

      if (mainSection.content) {
        return mainSection.content;
      }

      if (mainSection.items && mainSection.items.length > 0) {
        return mainSection.items.join('\n\n');
      }

      return response.summary || response.raw_content || "Sin contenido disponible.";
    };

    return (
      <div key={`${response.agent_id}-${response.timestamp}`} className="text-sm leading-relaxed">
        <ReactMarkdown className="prose prose-sm prose-invert max-w-none">
          {getMainContent()}
        </ReactMarkdown>

        {response.sections?.map((section, idx) => (
          section.type === "code" && section.content ? (
            <pre key={idx} className="bg-black/30 p-3 rounded-md overflow-x-auto text-xs my-2 mt-3">
              <code className="text-green-400">{section.content}</code>
            </pre>
          ) : null
        ))}
      </div>
    );
  };

  const renderMessage = (message: Message, index: number) => {
    const isUser = message.role === "user";

    return (
      <div
        key={index}
        className={cn(
          "flex gap-3 mb-6 animate-in fade-in-0 slide-in-from-bottom-2",
          isUser ? "justify-end" : "justify-start"
        )}
      >
        {!isUser && (
          <div className="flex-shrink-0 w-8 h-8 rounded-full bg-gradient-to-br from-primary/30 to-purple-500/30 flex items-center justify-center">
            <Sparkles className="h-4 w-4 text-primary" />
          </div>
        )}

        <div className={cn(
          "flex-1",
          isUser ? "max-w-[85%] flex justify-end" : "max-w-full"
        )}>
          <div className={cn(
            isUser
              ? "rounded-2xl px-4 py-3 max-w-[85%] shadow-sm bg-gradient-to-r from-blue-600 to-blue-700 text-white ml-auto shadow-blue-500/20"
              : message.role === "agent" && message.agentResponse
                ? "w-full" // El componente SpecializedAgentResponse tiene su propio estilo
                : "rounded-2xl px-4 py-3 max-w-[85%] shadow-sm bg-gradient-to-r from-gray-50 to-gray-100 dark:from-gray-800 dark:to-gray-900 text-gray-900 dark:text-gray-100 border border-gray-200 dark:border-gray-700"
          )}>
            {isUser ? (
              <p className="text-sm whitespace-pre-wrap">{message.content}</p>
            ) : message.role === "agent" && message.agentResponse ? (
              /* === NUEVO: Usar componente especializado por tipo de agente === */
              <SpecializedAgentResponse
                response={{
                  agent_id: message.agentResponse.agent_id || "unknown",
                  agent_name: message.agentName || message.agentResponse.agent_name || "Agente",
                  agent_emoji: message.agentEmoji || message.agentResponse.agent_emoji,
                  level: message.agentResponse.level,
                  specialty: message.agentResponse.specialty,
                  category: message.agentResponse.category || "analysis",
                  raw_content: message.content || message.agentResponse.raw_content,
                  summary: message.agentResponse.summary,
                  sections: message.agentResponse.sections,
                  timestamp: message.agentResponse.timestamp || message.timestamp.toISOString(),
                }}
                conversationId={currentConversationId || undefined}
                isExpanded={true}
              />
            ) : message.role === "agent" ? (
              /* Fallback para mensajes de agente sin agentResponse completo */
              <div className="rounded-xl border border-primary/20 bg-gradient-to-r from-primary/5 to-transparent p-4">
                <div className="flex items-center gap-2 mb-3 pb-2 border-b border-primary/10">
                  <span className="text-2xl">{message.agentEmoji || "🤖"}</span>
                  <span className="font-semibold text-primary">{message.agentName || "Agente"}</span>
                </div>
                <div className="text-sm leading-relaxed">
                  <ReactMarkdown className="prose prose-sm prose-invert max-w-none">
                    {message.content}
                  </ReactMarkdown>
                </div>
              </div>
            ) : (
              <div className="text-sm leading-relaxed">
                <ReactMarkdown className="prose prose-sm prose-invert max-w-none">
                  {message.content}
                </ReactMarkdown>
              </div>
            )}
          </div>

          <div className={cn(
            "flex items-center gap-2 mt-1 px-2 text-xs text-muted-foreground",
            isUser && "justify-end"
          )}>
            <span>{message.timestamp.toLocaleTimeString()}</span>
          </div>
        </div>

        {isUser && (
          <div className="flex-shrink-0 w-8 h-8 rounded-full bg-gradient-to-br from-blue-500/30 to-cyan-500/30 flex items-center justify-center">
            <User className="h-4 w-4 text-blue-400" />
          </div>
        )}
      </div>
    );
  };

  // Conectar WebSocket al montar
  useEffect(() => {
    connectWebSocket();

    return () => {
      if (wsRef.current) {
        wsRef.current.close();
      }
    };
  }, []);

  // Auto-scroll al final cuando hay nuevos mensajes
  useEffect(() => {
    if (scrollRef.current) {
      scrollRef.current.scrollTop = scrollRef.current.scrollHeight;
    }
  }, [messages]);

  return (
    <div className="flex flex-col h-full bg-background overflow-hidden w-full">
      {/* Mobile Header */}
      {isMobile && (
        <div className="flex items-center justify-between p-3 border-b border-primary/10 bg-muted/30">
          <div className="flex items-center gap-2">
            <Button
              size="sm"
              variant="ghost"
              onClick={() => setShowMobilePanel(!showMobilePanel)}
              className="h-8 w-8 p-0"
            >
              {showMobilePanel ? <X className="h-4 w-4" /> : <Menu className="h-4 w-4" />}
            </Button>
            <Brain className="h-4 w-4 text-primary" />
            <span className="font-semibold text-sm">AFW v0.5.0</span>
            <Badge variant="outline" className="text-xs">
              {messages.length}
            </Badge>
          </div>
          <div className="flex items-center gap-2">
            {isConnected ? (
              <Badge variant="outline" className="text-xs text-green-400 border-green-400/50">
                <Wifi className="h-3 w-3 mr-1" />
                <span className="hidden sm:inline">Conectado</span>
              </Badge>
            ) : (
              <Badge variant="outline" className="text-xs text-red-400 border-red-400/50">
                <WifiOff className="h-3 w-3 mr-1" />
                <span className="hidden sm:inline">Desconectado</span>
              </Badge>
            )}
          </div>
        </div>
      )}

      {/* Mobile Panel Overlay */}
      {isMobile && showMobilePanel && (
        <div
          className="fixed inset-0 z-50 bg-black/50"
          onClick={() => setShowMobilePanel(false)}
        />
      )}

      {/* Mobile Sidebar */}
      {isMobile && showMobilePanel && (
        <div className="fixed inset-y-0 left-0 z-50 w-80 bg-background border-r border-primary/10 overflow-hidden">
          <div className="flex items-center justify-between p-3 border-b border-primary/10 bg-muted/30">
            <div className="flex items-center gap-2">
              <Button
                size="sm"
                variant="ghost"
                onClick={() => setShowMobilePanel(false)}
                className="h-8 w-8 p-0"
              >
                <X className="h-4 w-4" />
              </Button>
              <Brain className="h-4 w-4 text-primary" />
              <span className="font-semibold text-sm">AFW v0.5.0</span>
            </div>
            <div className="flex items-center gap-2">
              <Button
                size="sm"
                variant="ghost"
                onClick={saveCurrentConversation}
                disabled={messages.length === 0}
                className="h-8 px-2 text-xs"
                title="Guardar conversación"
              >
                <Save className="h-3 w-3 mr-1" />
                <span className="hidden sm:inline">Guardar</span>
              </Button>
            </div>
          </div>
          <ConversationHistory
            currentConversationId={currentConversationId}
            onSelectConversation={handleSelectConversation}
            onNewConversation={createNewConversation}
            onDeleteConversation={handleDeleteConversation}
          />
        </div>
      )}

      {/* Main Layout */}
      <div className="flex flex-1 h-full overflow-hidden relative">
        {/* Chat Principal */}
        <div className="flex flex-col flex-1 min-w-0 bg-background h-full overflow-hidden relative">
          {/* Desktop Header */}
          {/* Desktop Header */}
          {!isMobile && (
            <div className="flex items-center justify-between p-3 md:p-4 border-b border-primary/10 bg-muted/30">
              <div className="flex items-center gap-2">
                <div className="p-2 rounded-xl bg-primary/20 border border-primary/40 shadow-lg">
                  <Layers className="h-6 w-6 text-primary animate-pulse" />
                </div>
                <div>
                  <span className="font-bold text-lg text-primary block leading-none">
                    Agentes
                  </span>
                </div>
              </div>
              <div className="flex items-center gap-2">
                <Button
                  variant="ghost"
                  size="sm"
                  onClick={createNewConversation}
                  className="text-xs font-semibold border-primary/40 hover:bg-primary/20 hover:border-primary transition-all"
                >
                  Nuevo
                </Button>
                <Badge variant="outline" className="text-xs">
                  {messages.length} mensajes
                </Badge>

                {/* Botón para colapsar historial a la derecha */}
                <div className="flex items-center gap-2 border-l border-primary/10 pl-2 ml-2">
                  <Button
                    size="sm"
                    variant="ghost"
                    onClick={() => setShowHistory(!showHistory)}
                    title={showHistory ? "Ocultar Historial" : "Mostrar Historial"}
                    className={cn("text-primary p-0 h-8 w-8 hover:bg-primary/10", showHistory && "bg-primary/10")}
                  >
                    <ChevronLeft className={cn(
                      "h-4 w-4 transition-transform",
                      showHistory && "rotate-180"
                    )} />
                  </Button>
                </div>
              </div>
            </div>
          )}

          {/* Chat Messages Area */}
          <div className="flex-1 overflow-y-auto p-4 scroll-smooth" ref={scrollRef}>
            {error && (
              <div className="flex items-center gap-2 p-3 rounded-lg bg-red-500/10 border border-red-500/20 text-red-400 mb-4 mx-auto max-w-2xl animate-in slide-in-from-top-2">
                <AlertCircle className="h-4 w-4" />
                {error}
              </div>
            )}

            {messages.length === 0 ? (
              <div className="h-full flex items-center justify-center p-8">
                <div className="flex flex-col items-center justify-center text-center max-w-md">
                  <div className="bg-gradient-to-br from-primary/20 to-cyan-500/20 rounded-full p-8 mb-8 shadow-2xl ring-1 ring-primary/30 relative">
                    <div className="absolute inset-0 rounded-full bg-primary/10 animate-ping opacity-20" />
                    <Brain className="h-16 w-16 text-primary animate-pulse relative z-10" />
                  </div>
                  <h3 className="text-2xl font-black mb-3 tracking-tight bg-gradient-to-r from-primary to-cyan-400 bg-clip-text text-transparent">
                    Sistema Multi-Agente Inteligente
                  </h3>
                  <p className="text-sm text-muted-foreground mb-6 leading-relaxed">
                    Selecciona una de las 60 tareas predefinidas o elige agentes específicos de 12 categorías profesionales. Cada tarea activa mínimo 5 agentes especializados para resultados completos.
                  </p>
                  <div className="px-4 py-2 rounded-full bg-primary/5 border border-primary/10 text-xs font-mono text-primary/70">
                    TheosKek Software 2026
                  </div>
                </div>
              </div>
            ) : (
              messages.map((message, index) => renderMessage(message, index))
            )}

            {/* Indicador de agente procesando */}
            {isProcessing && (
              <div className="flex justify-start mb-6 px-4">
                <div className="rounded-2xl px-4 py-3 bg-muted/30 border border-primary/10 flex items-center gap-3 shadow-sm">
                  <Loader2 className="h-4 w-4 animate-spin text-primary" />
                  <span className="text-sm font-medium animate-pulse text-primary">
                    {currentAgent ? `Agente ${currentAgent} procesando...` : "Orquestando respuesta..."}
                  </span>
                  {currentProgress > 0 && (
                    <span className="text-xs text-muted-foreground ml-2 font-mono">{currentProgress}%</span>
                  )}
                  <div className="w-24 bg-primary/10 h-1.5 rounded-full overflow-hidden ml-2">
                    <div
                      className="bg-primary h-full transition-all duration-300 ease-out"
                      style={{ width: `${currentProgress}%` }}
                    />
                  </div>
                </div>
              </div>
            )}
            <div ref={scrollRef} />
          </div>

          {/* Input Area */}
          <div className="p-4 border-t border-primary/10 bg-background/95 backdrop-blur supports-[backdrop-filter]:bg-background/60">
            <div className="relative flex items-end gap-2 max-w-6xl mx-auto">
              <div className="relative flex-1 group">
                <div className="absolute inset-0 bg-primary/5 rounded-xl blur-sm group-focus-within:bg-primary/10 transition-all" />
                <textarea
                  value={input}
                  onChange={(e) => setInput(e.target.value)}
                  onKeyDown={(e) => {
                    if (e.key === "Enter" && !e.shiftKey) {
                      e.preventDefault();
                      sendMessage();
                    }
                  }}
                  placeholder="Describe tu tarea compleja aquí..."
                  className="relative w-full min-h-[60px] max-h-[200px] p-4 pr-12 rounded-xl bg-background border border-primary/20 focus:border-primary focus:ring-1 focus:ring-primary/50 resize-none font-medium text-sm scrollbar-hide shadow-inner"
                  disabled={isProcessing}
                />
                <div className="absolute right-3 bottom-3 text-[10px] text-muted-foreground font-mono bg-background/80 px-1 rounded">
                  {input.length}/2000
                </div>
              </div>
              <Button
                onClick={sendMessage}
                disabled={!input.trim() || isProcessing || !isConnected}
                className={cn(
                  "h-[60px] w-[60px] rounded-xl shadow-lg transition-all border border-primary/20",
                  isProcessing
                    ? "bg-muted cursor-not-allowed text-muted-foreground"
                    : "bg-primary hover:bg-primary/90 hover:scale-105 active:scale-95 text-primary-foreground shadow-primary/25"
                )}
              >
                {isProcessing ? (
                  <Loader2 className="h-6 w-6 animate-spin" />
                ) : (
                  <Send className="h-6 w-6 ml-0.5" />
                )}
              </Button>
            </div>
            <div className="mt-2 text-center">
              <span className="text-[10px] text-muted-foreground/50">
                © TheosKek Software 2026
              </span>
            </div>
          </div>
        </div>

        {/* Right Sidebar - Tasks */}
        {!isMobile && (
          <TaskSelector
            onSelect={(agents) => onSelectPreset && onSelectPreset(agents)}
            className="h-full shrink-0"
          />
        )}

        {/* Right Sidebar - History (Memory) */}
        {!isMobile && showHistory && (
          <div className={cn(
            "border-l border-primary/10 h-full flex-shrink-0 bg-card overflow-hidden transition-all duration-300 ease-in-out",
            isTablet ? "w-60" : "w-72"
          )}>
            <div className="h-full flex flex-col">
              <div className="flex-1 overflow-hidden">
                <ConversationHistory
                  currentConversationId={currentConversationId}
                  onSelectConversation={handleSelectConversation}
                  onNewConversation={createNewConversation}
                  onDeleteConversation={handleDeleteConversation}
                  onSave={saveCurrentConversation}
                />
              </div>
            </div>
          </div>
        )}
      </div>
    </div>
  );
}

export default StreamingChatV2;
