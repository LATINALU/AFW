"use client";

import { useState, useEffect } from "react";
import { cn } from "@/lib/utils";
import {
  Brain,
  Lightbulb,
  MessageSquare,
  CheckCircle2,
  ChevronDown,
  ChevronRight,
  Zap,
  Clock,
  ArrowRight,
} from "lucide-react";

interface ReasoningStep {
  agent: string;
  thought: string;
  action?: string;
  result?: string;
  timestamp: Date;
  status: "thinking" | "acting" | "done";
}

interface AgentReasoningProps {
  steps: ReasoningStep[];
  isExpanded?: boolean;
}

const agentColors: Record<string, string> = {
  reasoning_agent: "text-yellow-500",
  planning_agent: "text-blue-500",
  research_agent: "text-purple-500",
  analysis_agent: "text-green-500",
  synthesis_agent: "text-cyan-500",
  critical_thinking_agent: "text-red-500",
  coding_agent: "text-orange-500",
  writing_agent: "text-pink-500",
  data_agent: "text-indigo-500",
  default: "text-primary",
};

const agentNames: Record<string, string> = {
  reasoning_agent: "🧠 Razonamiento",
  planning_agent: "📋 Planificación",
  research_agent: "🔍 Investigación",
  analysis_agent: "📊 Análisis",
  synthesis_agent: "🔗 Síntesis",
  critical_thinking_agent: "⚖️ Pensamiento Crítico",
  coding_agent: "💻 Programación",
  writing_agent: "✍️ Escritura",
  data_agent: "📈 Datos",
  communication_agent: "💬 Comunicación",
  decision_agent: "🎯 Decisiones",
  problem_solving_agent: "🧩 Resolución",
};

export function AgentReasoning({ steps, isExpanded = true }: AgentReasoningProps) {
  const [expanded, setExpanded] = useState(isExpanded);
  const [expandedSteps, setExpandedSteps] = useState<Set<number>>(new Set([0]));

  const toggleStep = (index: number) => {
    setExpandedSteps(prev => {
      const newSet = new Set(prev);
      if (newSet.has(index)) {
        newSet.delete(index);
      } else {
        newSet.add(index);
      }
      return newSet;
    });
  };

  if (steps.length === 0) return null;

  return (
    <div className="rounded-lg border border-border bg-card/50 overflow-hidden">
      {/* Header */}
      <button
        onClick={() => setExpanded(!expanded)}
        className="w-full flex items-center justify-between p-3 hover:bg-muted/50 transition-colors"
      >
        <div className="flex items-center gap-2">
          <Brain className="h-5 w-5 text-primary" />
          <span className="font-semibold text-foreground">
            Razonamiento de Agentes
          </span>
          <span className="text-xs text-muted-foreground">
            ({steps.length} pasos)
          </span>
        </div>
        {expanded ? (
          <ChevronDown className="h-4 w-4 text-muted-foreground" />
        ) : (
          <ChevronRight className="h-4 w-4 text-muted-foreground" />
        )}
      </button>

      {/* Steps */}
      {expanded && (
        <div className="border-t border-border">
          {steps.map((step, index) => (
            <div
              key={index}
              className={cn(
                "border-b border-border last:border-b-0",
                step.status === "thinking" && "bg-yellow-500/5",
                step.status === "acting" && "bg-blue-500/5",
                step.status === "done" && "bg-green-500/5"
              )}
            >
              {/* Step Header */}
              <button
                onClick={() => toggleStep(index)}
                className="w-full flex items-center gap-3 p-3 hover:bg-muted/30 transition-colors"
              >
                {/* Status Icon */}
                <div className={cn(
                  "w-6 h-6 rounded-full flex items-center justify-center shrink-0",
                  step.status === "thinking" && "bg-yellow-500/20",
                  step.status === "acting" && "bg-blue-500/20",
                  step.status === "done" && "bg-green-500/20"
                )}>
                  {step.status === "thinking" && (
                    <Lightbulb className="h-3 w-3 text-yellow-500 animate-pulse" />
                  )}
                  {step.status === "acting" && (
                    <Zap className="h-3 w-3 text-blue-500 animate-bounce" />
                  )}
                  {step.status === "done" && (
                    <CheckCircle2 className="h-3 w-3 text-green-500" />
                  )}
                </div>

                {/* Agent Name */}
                <span className={cn(
                  "font-medium text-sm",
                  agentColors[step.agent] || agentColors.default
                )}>
                  {agentNames[step.agent] || step.agent.replace(/_/g, " ")}
                </span>

                {/* Arrow */}
                <ArrowRight className="h-3 w-3 text-muted-foreground" />

                {/* Thought Preview */}
                <span className="text-sm text-muted-foreground truncate flex-1 text-left">
                  {step.thought.substring(0, 60)}...
                </span>

                {/* Time */}
                <span className="text-xs text-muted-foreground flex items-center gap-1">
                  <Clock className="h-3 w-3" />
                  {step.timestamp.toLocaleTimeString()}
                </span>

                {/* Expand Icon */}
                {expandedSteps.has(index) ? (
                  <ChevronDown className="h-4 w-4 text-muted-foreground" />
                ) : (
                  <ChevronRight className="h-4 w-4 text-muted-foreground" />
                )}
              </button>

              {/* Step Content */}
              {expandedSteps.has(index) && (
                <div className="px-4 pb-4 space-y-3">
                  {/* Thought */}
                  <div className="pl-9">
                    <div className="flex items-center gap-2 mb-1">
                      <Lightbulb className="h-4 w-4 text-yellow-500" />
                      <span className="text-xs font-medium text-yellow-500">PENSAMIENTO</span>
                    </div>
                    <p className="text-sm text-foreground bg-yellow-500/10 rounded-lg p-3 border border-yellow-500/20">
                      {step.thought}
                    </p>
                  </div>

                  {/* Action */}
                  {step.action && (
                    <div className="pl-9">
                      <div className="flex items-center gap-2 mb-1">
                        <Zap className="h-4 w-4 text-blue-500" />
                        <span className="text-xs font-medium text-blue-500">ACCIÓN</span>
                      </div>
                      <p className="text-sm text-foreground bg-blue-500/10 rounded-lg p-3 border border-blue-500/20 font-mono">
                        {step.action}
                      </p>
                    </div>
                  )}

                  {/* Result */}
                  {step.result && (
                    <div className="pl-9">
                      <div className="flex items-center gap-2 mb-1">
                        <MessageSquare className="h-4 w-4 text-green-500" />
                        <span className="text-xs font-medium text-green-500">RESULTADO</span>
                      </div>
                      <p className="text-sm text-foreground bg-green-500/10 rounded-lg p-3 border border-green-500/20">
                        {step.result}
                      </p>
                    </div>
                  )}
                </div>
              )}
            </div>
          ))}
        </div>
      )}
    </div>
  );
}

// Componente para mostrar el razonamiento en tiempo real durante el procesamiento
export function LiveReasoning({ 
  agents, 
  isProcessing 
}: { 
  agents: string[]; 
  isProcessing: boolean;
}) {
  const [currentAgent, setCurrentAgent] = useState(0);
  const [currentPhase, setCurrentPhase] = useState<"thinking" | "analyzing" | "communicating">("thinking");
  const [thoughts, setThoughts] = useState<string[]>([]);

  const thinkingPhrases = [
    "Analizando la solicitud del usuario...",
    "Identificando los puntos clave del problema...",
    "Considerando múltiples perspectivas...",
    "Evaluando posibles soluciones...",
    "Aplicando razonamiento lógico...",
    "Sintetizando información relevante...",
    "Verificando consistencia de conclusiones...",
    "Preparando respuesta estructurada...",
  ];

  useEffect(() => {
    if (!isProcessing) {
      setCurrentAgent(0);
      setCurrentPhase("thinking");
      setThoughts([]);
      return;
    }

    // Cycle through agents
    const agentInterval = setInterval(() => {
      setCurrentAgent(prev => (prev + 1) % Math.min(agents.length, 5));
    }, 4000);

    // Cycle through phases
    const phaseInterval = setInterval(() => {
      setCurrentPhase(prev => {
        if (prev === "thinking") return "analyzing";
        if (prev === "analyzing") return "communicating";
        return "thinking";
      });
    }, 1500);

    // Add thoughts
    const thoughtInterval = setInterval(() => {
      const randomThought = thinkingPhrases[Math.floor(Math.random() * thinkingPhrases.length)];
      setThoughts(prev => [...prev.slice(-4), randomThought]);
    }, 2000);

    return () => {
      clearInterval(agentInterval);
      clearInterval(phaseInterval);
      clearInterval(thoughtInterval);
    };
  }, [isProcessing, agents.length]);

  if (!isProcessing || agents.length === 0) return null;

  const activeAgent = agents[currentAgent] || agents[0];

  return (
    <div className="rounded-lg border border-primary/30 bg-card/80 backdrop-blur-sm overflow-hidden">
      {/* Header */}
      <div className="flex items-center gap-3 p-3 border-b border-border bg-primary/5">
        <div className="relative">
          <Brain className="h-6 w-6 text-primary" />
          <div className="absolute -top-1 -right-1 w-3 h-3 bg-green-500 rounded-full animate-ping" />
        </div>
        <div>
          <h3 className="font-bold text-foreground">Agentes Razonando en Tiempo Real</h3>
          <p className="text-xs text-muted-foreground">
            {agents.length} agentes colaborando en tu solicitud
          </p>
        </div>
      </div>

      {/* Current Agent */}
      <div className="p-4">
        <div className="flex items-center gap-3 mb-3">
          <div className={cn(
            "w-10 h-10 rounded-full flex items-center justify-center",
            "bg-primary/20 border-2 border-primary animate-pulse"
          )}>
            <span className="text-lg">
              {agentNames[activeAgent]?.split(" ")[0] || "🤖"}
            </span>
          </div>
          <div>
            <p className="font-semibold text-primary">
              {agentNames[activeAgent] || activeAgent.replace(/_/g, " ")}
            </p>
            <p className="text-xs text-muted-foreground">
              {currentPhase === "thinking" && "💭 Pensando..."}
              {currentPhase === "analyzing" && "🔍 Analizando..."}
              {currentPhase === "communicating" && "💬 Comunicando con otros agentes..."}
            </p>
          </div>
        </div>

        {/* Thought Stream */}
        <div className="space-y-2 max-h-32 overflow-y-auto">
          {thoughts.map((thought, idx) => (
            <div
              key={idx}
              className={cn(
                "text-sm p-2 rounded bg-muted/50 border-l-2 border-primary/50",
                "animate-in fade-in slide-in-from-left-2 duration-300"
              )}
              style={{ opacity: 0.5 + (idx / thoughts.length) * 0.5 }}
            >
              <span className="text-primary mr-2">▸</span>
              {thought}
            </div>
          ))}
        </div>

        {/* Agent Pipeline */}
        <div className="flex items-center gap-2 mt-4 pt-3 border-t border-border overflow-x-auto">
          {agents.slice(0, 5).map((agent, idx) => (
            <div
              key={agent}
              className={cn(
                "flex items-center gap-1 px-2 py-1 rounded-full text-xs whitespace-nowrap",
                idx === currentAgent
                  ? "bg-primary text-primary-foreground"
                  : idx < currentAgent
                  ? "bg-green-500/20 text-green-500"
                  : "bg-muted text-muted-foreground"
              )}
            >
              {idx < currentAgent && <CheckCircle2 className="h-3 w-3" />}
              {idx === currentAgent && <div className="w-2 h-2 bg-current rounded-full animate-pulse" />}
              {agentNames[agent]?.split(" ")[1] || agent.split("_")[0]}
            </div>
          ))}
        </div>
      </div>

      {/* Progress Bar */}
      <div className="h-1 bg-muted">
        <div 
          className="h-full bg-gradient-to-r from-primary to-accent transition-all duration-1000"
          style={{ width: `${((currentAgent + 1) / Math.min(agents.length, 5)) * 100}%` }}
        />
      </div>
    </div>
  );
}
