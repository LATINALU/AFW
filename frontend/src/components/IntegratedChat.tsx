/**
 * Integrated Chat v1.0.0
 * =====================
 * Componente de chat integrado con todas las funcionalidades de ATP.
 */

'use client';

import React, { useState, useEffect } from 'react';
import { Send, Users, Settings, History, Bookmark, Menu, X } from 'lucide-react';
import { useDeviceDetection } from '@/hooks/useDeviceDetection';
import { useSavedResponses } from '@/hooks/useSavedResponses';
import { EnhancedAgentResponse } from '@/components/EnhancedAgentResponse';
import { ConversationSidebar } from '@/components/ConversationSidebar';
import { SavedResponsesLibrary } from '@/components/SavedResponsesLibrary';
import { MobileChatInterface } from '@/components/mobile/MobileChatInterface';
import { MobileActionButtons } from '@/components/mobile/MobileActionButtons';
import { MobileTasksPanel } from '@/components/mobile/MobileTasksPanel';
import { QuickStartGuide } from '@/components/QuickStartGuide';
import { cn } from '@/lib/utils';

interface Message {
  id: string;
  role: 'user' | 'assistant';
  content: string;
  timestamp: string | Date;
  agentId?: string;
  agentName?: string;
  agentEmoji?: string;
  level?: number;
  specialty?: string;
}

interface IntegratedChatProps {
  conversationId?: string;
  onConversationChange?: (id: string) => void;
}

export function IntegratedChat({ 
  conversationId: externalConversationId, 
  onConversationChange 
}: IntegratedChatProps) {
  const device = useDeviceDetection();
  const { saveResponse, isResponseSaved } = useSavedResponses();
  
  const [messages, setMessages] = useState<Message[]>([]);
  const [input, setInput] = useState('');
  const [isLoading, setIsLoading] = useState(false);
  const [sidebarOpen, setSidebarOpen] = useState(!device.isMobile);
  const [libraryOpen, setLibraryOpen] = useState(false);
  const [conversationId, setConversationId] = useState<string | undefined>(externalConversationId);
  const [selectedAgents, setSelectedAgents] = useState(['reasoning', 'synthesis']);
  const [tasksOpen, setTasksOpen] = useState(false);
  const [agentsOpen, setAgentsOpen] = useState(false);
  const [memoryOpen, setMemoryOpen] = useState(false);
  const [quickStartOpen, setQuickStartOpen] = useState(false);
  const [activeView, setActiveView] = useState<'agents' | 'memory' | 'tasks' | null>(null);

  // Mobile: usar componente específico
  if (device.isMobile) {
    return (
      <div className="h-screen flex flex-col bg-background">
        {/* Header móvil */}
        <div className="flex items-center justify-between p-4 border-b border-border">
          <button
            onClick={() => setSidebarOpen(!sidebarOpen)}
            className="p-2 rounded-lg hover:bg-accent transition-colors"
          >
            <Menu className="w-5 h-5" />
          </button>
          
          <h1 className="text-lg font-semibold">ATP Chat</h1>
          
          <div className="flex items-center gap-2">
            <button
              onClick={() => setQuickStartOpen(true)}
              className="p-2 rounded-lg bg-blue-500/10 text-blue-500 hover:bg-blue-500/20 transition-colors"
              title="Configurar API Keys"
            >
              <Settings className="w-5 h-5" />
            </button>
            <button
              onClick={() => setLibraryOpen(true)}
              className="p-2 rounded-lg hover:bg-accent transition-colors"
            >
              <Bookmark className="w-5 h-5" />
            </button>
          </div>
        </div>

        {/* Sidebar móvil */}
        <ConversationSidebar
          isOpen={sidebarOpen}
          onClose={() => setSidebarOpen(false)}
          onNewChat={() => setConversationId(undefined)}
          onSelectConversation={setConversationId}
          currentConversationId={conversationId}
        />

        {/* Chat móvil */}
        <MobileChatInterface
          messages={messages.map(msg => ({
            ...msg,
            timestamp: typeof msg.timestamp === 'string' ? msg.timestamp : msg.timestamp.toISOString()
          }))}
          onSendMessage={handleSendMessage}
          isLoading={isLoading}
          onOpenSettings={() => {}}
          onOpenHistory={() => setSidebarOpen(true)}
          onOpenAgents={() => {}}
        />

        {/* Biblioteca móvil */}
        <SavedResponsesLibrary
          isOpen={libraryOpen}
          onClose={() => setLibraryOpen(false)}
        />

        {/* Panel de Tareas */}
        <MobileTasksPanel
          isOpen={tasksOpen}
          onClose={() => {
            setTasksOpen(false);
            setActiveView(null);
          }}
        />

        {/* Botones de Acción Móvil */}
        <MobileActionButtons
          onOpenAgents={() => {
            setAgentsOpen(true);
            setActiveView('agents');
          }}
          onOpenMemory={() => {
            setMemoryOpen(true);
            setActiveView('memory');
          }}
          onOpenTasks={() => {
            setTasksOpen(true);
            setActiveView('tasks');
          }}
          activeView={activeView}
        />

        {/* Guía Rápida */}
        <QuickStartGuide
          isOpen={quickStartOpen}
          onClose={() => setQuickStartOpen(false)}
        />

        {/* Overlay */}
        {sidebarOpen && (
          <div
            className="fixed inset-0 bg-black/50 z-30"
            onClick={() => setSidebarOpen(false)}
          />
        )}
      </div>
    );
  }

  // Desktop: usar componente completo
  async function handleSendMessage(message: string) {
    if (!message.trim() || isLoading) return;

    const userMessage: Message = {
      id: `user_${Date.now()}`,
      role: 'user',
      content: message,
      timestamp: new Date().toISOString(),
    };

    setMessages(prev => [...prev, userMessage]);
    setInput('');
    setIsLoading(true);

    try {
      // Simular respuesta de agentes (reemplazar con llamada real a API)
      const agentResponses = await simulateAgentResponse(message, selectedAgents);
      
      const assistantMessages: Message[] = agentResponses.map((response, index) => ({
        id: `agent_${Date.now()}_${index}`,
        role: 'assistant',
        content: response.content,
        timestamp: new Date().toISOString(),
        agentId: response.agentId,
        agentName: response.agentName,
        agentEmoji: response.agentEmoji,
        level: response.level,
        specialty: response.specialty,
      }));

      setMessages(prev => [...prev, ...assistantMessages]);
    } catch (error) {
      console.error('Error al enviar mensaje:', error);
      
      const errorMessage: Message = {
        id: `error_${Date.now()}`,
        role: 'assistant',
        content: 'Lo siento, hubo un error al procesar tu mensaje. Por favor, inténtalo de nuevo.',
        timestamp: new Date().toISOString(),
      };
      
      setMessages(prev => [...prev, errorMessage]);
    } finally {
      setIsLoading(false);
    }
  }

  async function simulateAgentResponse(message: string, agents: string[]) {
    // Simulación de respuestas de agentes
    const responses = [];
    
    for (const agentId of agents) {
      await new Promise(resolve => setTimeout(resolve, 1000)); // Simular procesamiento
      
      responses.push({
        agentId,
        agentName: getAgentName(agentId),
        agentEmoji: getAgentEmoji(agentId),
        level: getAgentLevel(agentId),
        specialty: getAgentSpecialty(agentId),
        content: generateResponse(message, agentId),
      });
    }
    
    return responses;
  }

  function getAgentName(agentId: string): string {
    const names: Record<string, string> = {
      reasoning: 'Agente de Razonamiento',
      synthesis: 'Agente de Síntesis',
      analysis: 'Agente de Análisis',
      research: 'Agente de Investigación',
    };
    return names[agentId] || agentId;
  }

  function getAgentEmoji(agentId: string): string {
    const emojis: Record<string, string> = {
      reasoning: '🧠',
      synthesis: '🔗',
      analysis: '📊',
      research: '🔍',
    };
    return emojis[agentId] || '🤖';
  }

  function getAgentLevel(agentId: string): number {
    const levels: Record<string, number> = {
      reasoning: 1,
      synthesis: 1,
      analysis: 2,
      research: 2,
    };
    return levels[agentId] || 1;
  }

  function getAgentSpecialty(agentId: string): string {
    const specialties: Record<string, string> = {
      reasoning: 'Lógica y análisis crítico',
      synthesis: 'Integración de información',
      analysis: 'Análisis de datos',
      research: 'Investigación y búsqueda',
    };
    return specialties[agentId] || 'General';
  }

  function generateResponse(message: string, agentId: string): string {
    const responses: Record<string, string> = {
      reasoning: `Basado en tu pregunta "${message}", he analizado la situación desde una perspectiva lógica. Es importante considerar los siguientes puntos:\n\n1. **Análisis lógico**: Evaluar la validez de los supuestos\n2. **Estructura del problema**: Descomponer en partes manejables\n3. **Solución propuesta**: Ofrecer un enfoque sistemático\n\nEsta metodología permite abordar el problema de manera estructurada y evitar conclusiones precipitadas.`,
      
      synthesis: `He integrado la información sobre "${message}" de las siguientes fuentes:\n\n• **Aspectos principales**: Identificación de elementos clave\n• **Relaciones**: Conexiones entre diferentes componentes\n• **Síntesis**: Consolidación en un panorama completo\n\nEl resultado es una visión holística que captura la esencia del tema.`,
      
      analysis: `El análisis de "${message}" revela los siguientes patrones:\n\n📊 **Datos cuantitativos**: Métricas relevantes y tendencias\n📈 **Cualitativo**: Factores subyacentes e implicancias\n🎯 **Recomendaciones**: Acciones sugeridas basadas en evidencia\n\nEste análisis proporciona una base sólida para la toma de decisiones.`,
      
      research: `Mi investigación sobre "${message}" ha arrojado los siguientes hallazgos:\n\n🔍 **Fuentes primarias**: Documentación y referencias directas\n📚 **Contexto histórico**: Evolución y antecedentes\n🌐 **Estado actual**: Situación contemporánea y tendencias\n\nLa investigación exhaustiva permite una comprensión profunda del tema.`,
    };
    
    return responses[agentId] || `Respuesta del agente ${agentId} sobre: ${message}`;
  }

  return (
    <div className="h-screen flex bg-background">
      {/* Sidebar */}
      <ConversationSidebar
        isOpen={sidebarOpen}
        onClose={() => setSidebarOpen(false)}
        onNewChat={() => setConversationId(undefined)}
        onSelectConversation={setConversationId}
        currentConversationId={conversationId}
      />

      {/* Área Principal */}
      <div className="flex-1 flex flex-col">
        {/* Header */}
        <header className="flex items-center justify-between p-4 border-b border-border bg-background/95 backdrop-blur-sm">
          <div className="flex items-center gap-4">
            <button
              onClick={() => setSidebarOpen(!sidebarOpen)}
              className="p-2 rounded-lg hover:bg-accent transition-colors"
            >
              <Menu className="w-5 h-5" />
            </button>
            
            <div>
              <h1 className="text-xl font-bold">ATP Chat</h1>
              <p className="text-sm text-muted-foreground">
                {selectedAgents.length} agente{selectedAgents.length !== 1 ? 's' : ''} seleccionado{selectedAgents.length !== 1 ? 's' : ''}
              </p>
            </div>
          </div>

          <div className="flex items-center gap-2">
            <button
              onClick={() => setQuickStartOpen(true)}
              className="px-3 py-2 bg-blue-500 text-white rounded-lg hover:bg-blue-600 transition-colors flex items-center gap-2"
              title="Configurar API Keys"
            >
              <Settings className="w-4 h-4" />
              <span className="hidden sm:inline">API Keys</span>
            </button>
            
            <button
              onClick={() => setLibraryOpen(true)}
              className="px-3 py-2 bg-primary text-primary-foreground rounded-lg hover:bg-primary/90 transition-colors flex items-center gap-2"
            >
              <Bookmark className="w-4 h-4" />
              <span className="hidden sm:inline">Guardadas</span>
            </button>
          </div>
        </header>

        {/* Área de Mensajes */}
        <div className="flex-1 overflow-y-auto p-4 space-y-4">
          {messages.length === 0 ? (
            <div className="flex flex-col items-center justify-center h-full text-center">
              <div className="text-6xl mb-4">🤖</div>
              <h2 className="text-2xl font-semibold mb-2">
                Bienvenido a ATP
              </h2>
              <p className="text-muted-foreground max-w-md">
                Selecciona agentes y comienza a chatear con nuestros 30 especialistas en IA
              </p>
            </div>
          ) : (
            messages.map((message) => (
              <div
                key={message.id}
                className={cn(
                  "flex gap-4",
                  message.role === 'user' ? 'justify-end' : 'justify-start'
                )}
              >
                {message.role === 'user' ? (
                  <div className="max-w-[70%]">
                    <div className="bg-primary text-primary-foreground rounded-2xl rounded-br-sm px-4 py-3">
                      <p className="text-sm">{message.content}</p>
                    </div>
                    <div className="text-xs text-muted-foreground mt-1 text-right">
                      {typeof message.timestamp === 'string' 
                        ? new Date(message.timestamp).toLocaleTimeString('es-ES', {
                            hour: '2-digit',
                            minute: '2-digit',
                          })
                        : message.timestamp.toLocaleTimeString('es-ES', {
                            hour: '2-digit',
                            minute: '2-digit',
                          })
                      }
                    </div>
                  </div>
                ) : (
                  <div className="max-w-[85%]">
                    <EnhancedAgentResponse
                      agentId={message.agentId || ''}
                      agentName={message.agentName || 'Agente'}
                      agentEmoji={message.agentEmoji}
                      level={message.level}
                      specialty={message.specialty}
                      content={message.content}
                      timestamp={typeof message.timestamp === 'string' ? new Date(message.timestamp) : message.timestamp}
                      conversationId={conversationId}
                      messageId={message.id}
                      onSaveResponse={saveResponse}
                      isSaved={isResponseSaved(message.content, message.agentId || '')}
                    />
                  </div>
                )}
              </div>
            ))
          )}
          
          {isLoading && (
            <div className="flex justify-center">
              <div className="flex items-center gap-2 text-muted-foreground">
                <div className="w-2 h-2 bg-primary rounded-full animate-bounce" style={{ animationDelay: '0ms' }} />
                <div className="w-2 h-2 bg-primary rounded-full animate-bounce" style={{ animationDelay: '150ms' }} />
                <div className="w-2 h-2 bg-primary rounded-full animate-bounce" style={{ animationDelay: '300ms' }} />
                <span className="text-sm">Procesando...</span>
              </div>
            </div>
          )}
        </div>

        {/* Input */}
        <div className="border-t border-border p-4 bg-background/95 backdrop-blur-sm">
          <div className="flex items-end gap-2 max-w-4xl mx-auto">
            <div className="flex-1">
              <textarea
                value={input}
                onChange={(e) => setInput(e.target.value)}
                onKeyPress={(e) => {
                  if (e.key === 'Enter' && !e.shiftKey) {
                    e.preventDefault();
                    handleSendMessage(input);
                  }
                }}
                placeholder="Escribe tu mensaje..."
                className="w-full px-4 py-3 bg-accent rounded-2xl resize-none focus:outline-none focus:ring-2 focus:ring-primary min-h-[48px] max-h-32"
                rows={1}
                style={{
                  height: 'auto',
                  minHeight: '48px',
                }}
                onInput={(e) => {
                  const target = e.target as HTMLTextAreaElement;
                  target.style.height = 'auto';
                  target.style.height = Math.min(target.scrollHeight, 128) + 'px';
                }}
              />
            </div>
            
            <button
              onClick={() => handleSendMessage(input)}
              disabled={!input.trim() || isLoading}
              className="p-3 bg-primary text-primary-foreground rounded-2xl hover:bg-primary/90 disabled:opacity-50 disabled:cursor-not-allowed transition-all active:scale-95"
            >
              <Send className="w-5 h-5" />
            </button>
          </div>
        </div>
      </div>

      {/* Biblioteca de Respuestas */}
      <SavedResponsesLibrary
        isOpen={libraryOpen}
        onClose={() => setLibraryOpen(false)}
      />

      {/* Guía Rápida */}
      <QuickStartGuide
        isOpen={quickStartOpen}
        onClose={() => setQuickStartOpen(false)}
      />
    </div>
  );
}
