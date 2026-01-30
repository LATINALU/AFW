"use client";

/**
 * StreamingChat Component v0.7.2
 * ==============================
 * Componente de chat con streaming en tiempo real.
 * 
 * Características:
 * - WebSocket para comunicación bidireccional
 * - SSE como fallback
 * - Visualización de respuestas en tiempo real
 * - Tarjetas separadas por agente con colores por nivel
 * - Indicadores de progreso animados
 */

import React, { useState, useEffect, useRef, useCallback } from "react";
import { cn } from "@/lib/utils";
import { Button } from "@/components/ui/button";
import { Badge } from "@/components/ui/badge";
import { Card, CardContent, CardHeader, CardTitle } from "@/components/ui/card";
import { Progress } from "@/components/ui/progress";
import ReactMarkdown from "react-markdown";
import {
  Brain, Loader2, Send, Wifi, WifiOff, Clock,
  CheckCircle2, AlertCircle, Zap
} from "lucide-react";

// Configuración de colores por nivel - EN ESPAÑOL
const LEVEL_CONFIG: Record<number, {
  color: string;
  bgColor: string;
  borderColor: string;
  textColor: string;
  name: string;
  emoji: string;
}> = {
  1: {
    color: "blue",
    bgColor: "bg-blue-500/10",
    borderColor: "border-l-blue-500",
    textColor: "text-blue-400",
    name: "Lógica y Fundamentos",
    emoji: "🧠"
  },
  2: {
    color: "emerald",
    bgColor: "bg-emerald-500/10",
    borderColor: "border-l-emerald-500",
    textColor: "text-emerald-400",
    name: "Producción Profesional",
    emoji: "💼"
  },
  3: {
    color: "amber",
    bgColor: "bg-amber-500/10",
    borderColor: "border-l-amber-500",
    textColor: "text-amber-400",
    name: "Dominios Especializados",
    emoji: "🎓"
  },
  4: {
    color: "rose",
    bgColor: "bg-rose-500/10",
    borderColor: "border-l-rose-500",
    textColor: "text-rose-400",
    name: "Soporte Operacional",
    emoji: "🔧"
  },
  5: {
    color: "violet",
    bgColor: "bg-violet-500/10",
    borderColor: "border-l-violet-500",
    textColor: "text-violet-400",
    name: "Auxiliares Estratégicos",
    emoji: "✨"
  }
};

// Tipos para respuestas de agentes
interface AgentResponse {
  agent_id: string;
  agent_name: string;
  agent_emoji: string;
  level: number;
  level_name: string;
  specialty: string;
  response_type: string;
  title: string;
  sections: Array<{
    title: string;
    type: string;
    items?: string[];
    content?: string;
    language?: string;
  }>;
  key_points: string[];
  summary: string;
  raw_content: string;
  step: number;
  total_steps: number;
  progress: number;
  timestamp: string;
}

interface PipelineSummary {
  type: string;
  title: string;
  status: string;
  agents_count: number;
  processing_time_formatted: string;
  summary_points: string[];
}

interface StreamingChatProps {
  selectedAgents: string[];
  apiConfig?: {
    type: string;
    apiKey: string;
    baseUrl?: string;
  };
  model: string;
}

export function StreamingChat({
  selectedAgents,
  apiConfig,
  model
}: StreamingChatProps) {
  const [input, setInput] = useState("");
  const [isConnected, setIsConnected] = useState(false);
  const [isProcessing, setIsProcessing] = useState(false);
  const [responses, setResponses] = useState<AgentResponse[]>([]);
  const [currentAgent, setCurrentAgent] = useState<string | null>(null);
  const [currentProgress, setCurrentProgress] = useState(0);
  const [pipelineSummary, setPipelineSummary] = useState<PipelineSummary | null>(null);
  const [error, setError] = useState<string | null>(null);
  
  const wsRef = useRef<WebSocket | null>(null);
  const clientIdRef = useRef<string>(`client_${Date.now()}_${Math.random().toString(36).substr(2, 9)}`);
  const scrollRef = useRef<HTMLDivElement>(null);

  // Conectar WebSocket al montar
  useEffect(() => {
    connectWebSocket();
    
    return () => {
      if (wsRef.current) {
        wsRef.current.close();
      }
    };
  }, []);

  // Auto-scroll cuando hay nuevas respuestas
  useEffect(() => {
    if (scrollRef.current) {
      scrollRef.current.scrollTop = scrollRef.current.scrollHeight;
    }
  }, [responses, currentAgent]);

  const connectWebSocket = useCallback(() => {
    const wsUrl = `ws://${window.location.hostname}:8001/ws/${clientIdRef.current}`;
    
    try {
      const ws = new WebSocket(wsUrl);
      
      ws.onopen = () => {
        console.log("✅ WebSocket conectado");
        setIsConnected(true);
        setError(null);
      };
      
      ws.onclose = () => {
        console.log("📴 WebSocket desconectado");
        setIsConnected(false);
        // Reintentar conexión después de 3 segundos
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
        setResponses([]);
        setPipelineSummary(null);
        setIsProcessing(true);
        break;
        
      case "agent_start":
        setCurrentAgent(data.agent);
        setCurrentProgress(0);
        break;
        
      case "agent_progress":
        setCurrentProgress(data.progress);
        break;
        
      case "agent_response":
        setResponses(prev => [...prev, data.data]);
        setCurrentAgent(null);
        break;
        
      case "agent_error":
        setError(`Error en ${data.agent}: ${data.error}`);
        break;
        
      case "pipeline_complete":
        setPipelineSummary(data.data);
        setIsProcessing(false);
        setCurrentAgent(null);
        break;
        
      case "pong":
        // Heartbeat response
        break;
        
      default:
        console.log("Mensaje desconocido:", data);
    }
  };

  const sendMessage = async () => {
    if (!input.trim() || !isConnected || isProcessing) return;
    
    setError(null);
    setResponses([]);
    setPipelineSummary(null);
    
    const message = {
      action: "start_pipeline",
      message: input,
      agents: selectedAgents,
      model: model,
      apiConfig: apiConfig
    };
    
    if (wsRef.current && wsRef.current.readyState === WebSocket.OPEN) {
      wsRef.current.send(JSON.stringify(message));
      setIsProcessing(true);
      setInput("");
    } else {
      // Fallback a SSE si WebSocket no está disponible
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
              
              if (data.type === "stream_complete") {
                setIsProcessing(false);
              } else if (data.type === "pipeline_summary") {
                setPipelineSummary(data);
                setIsProcessing(false);
              } else if (data.agent_id) {
                setResponses(prev => [...prev, data]);
              }
            } catch (e) {
              // Ignorar líneas mal formadas
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

  const renderAgentResponse = (response: AgentResponse, index: number) => {
    const levelConfig = LEVEL_CONFIG[response.level] || LEVEL_CONFIG[3];
    
    return (
      <Card
        key={`${response.agent_id}-${index}`}
        className={cn(
          "border-l-4 transition-all duration-300 animate-in fade-in-0 slide-in-from-bottom-4",
          levelConfig.borderColor,
          levelConfig.bgColor,
          "hover:shadow-lg"
        )}
      >
        <CardHeader className="pb-2">
          <div className="flex items-center justify-between">
            <div className="flex items-center gap-2">
              <span className="text-2xl">{response.agent_emoji}</span>
              <div>
                <CardTitle className={cn("text-lg", levelConfig.textColor)}>
                  {response.agent_name}
                </CardTitle>
                <p className="text-xs text-muted-foreground">
                  {response.specialty}
                </p>
              </div>
            </div>
            <div className="flex items-center gap-2">
              <Badge variant="outline" className={levelConfig.textColor}>
                Nivel {response.level}
              </Badge>
              <Badge variant="secondary" className="text-xs">
                {response.step}/{response.total_steps}
              </Badge>
            </div>
          </div>
        </CardHeader>
        
        <CardContent className="space-y-4">
          {/* Secciones de contenido */}
          {response.sections.map((section, sIdx) => (
            <div key={sIdx} className="space-y-2">
              {section.title && section.title !== "Contenido" && (
                <h4 className="font-semibold text-sm text-foreground/80">
                  {section.title}
                </h4>
              )}
              
              {section.type === "code" && section.content ? (
                <pre className="bg-black/50 p-3 rounded-md overflow-x-auto text-xs">
                  <code className="text-green-400">{section.content}</code>
                </pre>
              ) : section.items ? (
                <ul className="space-y-1 text-sm">
                  {section.items.map((item, iIdx) => (
                    <li key={iIdx} className="text-foreground/80">
                      <ReactMarkdown className="inline">{item}</ReactMarkdown>
                    </li>
                  ))}
                </ul>
              ) : section.content ? (
                <div className="prose prose-sm prose-invert max-w-none">
                  <ReactMarkdown>{section.content}</ReactMarkdown>
                </div>
              ) : null}
            </div>
          ))}
          
          {/* Puntos clave */}
          {response.key_points && response.key_points.length > 0 && (
            <div className="border-t border-primary/10 pt-3 mt-3">
              <div className="flex flex-wrap gap-2">
                {response.key_points.slice(0, 3).map((point, pIdx) => (
                  <Badge key={pIdx} variant="outline" className="text-xs">
                    {point}
                  </Badge>
                ))}
              </div>
            </div>
          )}
          
          {/* Footer */}
          <div className="flex items-center justify-between text-xs text-muted-foreground pt-2 border-t border-primary/5">
            <div className="flex items-center gap-1">
              <Clock className="h-3 w-3" />
              {new Date(response.timestamp).toLocaleTimeString()}
            </div>
            <span className="font-mono">@{response.agent_id}</span>
          </div>
        </CardContent>
      </Card>
    );
  };

  return (
    <div className="flex flex-col h-full">
      {/* Header con estado de conexión */}
      <div className="flex items-center justify-between p-3 border-b border-primary/20 bg-background/50">
        <div className="flex items-center gap-2">
          <Brain className="h-5 w-5 text-primary" />
          <span className="font-bold text-sm">AFW Streaming v0.7.2</span>
        </div>
        <div className="flex items-center gap-2">
          {isConnected ? (
            <Badge variant="outline" className="text-green-400 border-green-400/50">
              <Wifi className="h-3 w-3 mr-1" />
              En línea
            </Badge>
          ) : (
            <Badge variant="outline" className="text-red-400 border-red-400/50">
              <WifiOff className="h-3 w-3 mr-1" />
              Sin conexión
            </Badge>
          )}
          <Badge variant="secondary">
            {selectedAgents.length} {selectedAgents.length === 1 ? 'agente' : 'agentes'}
          </Badge>
        </div>
      </div>

      {/* Área de respuestas */}
      <div 
        ref={scrollRef}
        className="flex-1 overflow-y-auto p-4 space-y-4"
      >
        {/* Error message */}
        {error && (
          <div className="flex items-center gap-2 p-3 rounded-lg bg-red-500/10 border border-red-500/20 text-red-400">
            <AlertCircle className="h-4 w-4" />
            {error}
          </div>
        )}

        {/* Respuestas de agentes */}
        {responses.map((response, index) => renderAgentResponse(response, index))}

        {/* Indicador de agente actual procesando */}
        {currentAgent && (
          <Card className="border-primary/30 bg-primary/5 animate-pulse">
            <CardContent className="py-4">
              <div className="flex items-center gap-3">
                <Loader2 className="h-5 w-5 animate-spin text-primary" />
                <div className="flex-1">
                  <p className="font-medium text-sm">{currentAgent}</p>
                  <p className="text-xs text-muted-foreground">Analizando y generando respuesta...</p>
                </div>
                <span className="text-xs text-primary">{currentProgress}%</span>
              </div>
              <Progress value={currentProgress} className="mt-2 h-1" />
            </CardContent>
          </Card>
        )}

        {/* Resumen del pipeline */}
        {pipelineSummary && (
          <Card className="border-green-500/30 bg-green-500/5">
            <CardContent className="py-4">
              <div className="flex items-center gap-2 mb-3">
                <CheckCircle2 className="h-5 w-5 text-green-400" />
                <span className="font-bold text-green-400">{pipelineSummary.title}</span>
              </div>
              <div className="space-y-1">
                {pipelineSummary.summary_points.map((point, idx) => (
                  <p key={idx} className="text-sm text-muted-foreground">{point}</p>
                ))}
              </div>
            </CardContent>
          </Card>
        )}

        {/* Estado vacío */}
        {!isProcessing && responses.length === 0 && !error && (
          <div className="flex flex-col items-center justify-center h-full text-center text-muted-foreground">
            <Zap className="h-12 w-12 mb-4 opacity-50" />
            <p className="text-lg font-medium">Sistema Multi-Agente en Tiempo Real</p>
            <p className="text-sm">Selecciona una tarea o agentes y envía tu consulta para recibir respuestas especializadas</p>
          </div>
        )}
      </div>

      {/* Input de mensaje */}
      <div className="p-4 border-t border-primary/20 bg-background/80">
        <div className="flex gap-2">
          <input
            type="text"
            value={input}
            onChange={(e) => setInput(e.target.value)}
            onKeyDown={(e) => e.key === "Enter" && !e.shiftKey && sendMessage()}
            placeholder="Escribe tu mensaje..."
            disabled={!isConnected || isProcessing}
            className={cn(
              "flex-1 px-4 py-2 rounded-lg border bg-background/50",
              "focus:outline-none focus:ring-2 focus:ring-primary/50",
              "disabled:opacity-50 disabled:cursor-not-allowed"
            )}
          />
          <Button
            onClick={sendMessage}
            disabled={!isConnected || isProcessing || !input.trim()}
            className="px-4"
          >
            {isProcessing ? (
              <Loader2 className="h-4 w-4 animate-spin" />
            ) : (
              <Send className="h-4 w-4" />
            )}
          </Button>
        </div>
      </div>
    </div>
  );
}

export default StreamingChat;
