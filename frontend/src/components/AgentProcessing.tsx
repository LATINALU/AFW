"use client";

import { useState, useEffect } from "react";
import { cn } from "@/lib/utils";
import {
  Brain,
  Zap,
  MessageSquare,
  ArrowRight,
  CheckCircle,
  Loader2,
  Sparkles,
} from "lucide-react";

interface AgentStep {
  agentName: string;
  status: "waiting" | "thinking" | "communicating" | "done";
  message?: string;
}

interface AgentProcessingProps {
  agents: string[];
  isProcessing: boolean;
  currentStep?: number;
}

const agentDisplayNames: Record<string, string> = {
  reasoning_agent: "Razonamiento",
  planning_agent: "Planificación",
  research_agent: "Investigación",
  analysis_agent: "Análisis",
  synthesis_agent: "Síntesis",
  critical_thinking_agent: "Pensamiento Crítico",
  coding_agent: "Programación",
  writing_agent: "Escritura",
  data_agent: "Datos",
  communication_agent: "Comunicación",
  decision_agent: "Decisiones",
  problem_solving_agent: "Resolución",
  legal_agent: "Legal",
  financial_agent: "Finanzas",
  creative_agent: "Creatividad",
  technical_agent: "Técnico",
  educational_agent: "Educación",
  marketing_agent: "Marketing",
  qa_agent: "QA",
  documentation_agent: "Documentación",
  optimization_agent: "Optimización",
  security_agent: "Seguridad",
  integration_agent: "Integración",
  review_agent: "Revisión",
  translation_agent: "Traducción",
  summary_agent: "Resumen",
  formatting_agent: "Formato",
  validation_agent: "Validación",
  coordination_agent: "Coordinación",
  explanation_agent: "Explicación",
};

const thinkingMessages = [
  "Analizando la solicitud...",
  "Procesando información...",
  "Evaluando opciones...",
  "Razonando profundamente...",
  "Considerando perspectivas...",
  "Sintetizando datos...",
  "Formulando respuesta...",
];

const communicatingMessages = [
  "Compartiendo hallazgos con otros agentes...",
  "Consultando con el equipo...",
  "Integrando perspectivas...",
  "Colaborando en la solución...",
  "Validando conclusiones...",
];

export function AgentProcessing({ agents, isProcessing, currentStep = 0 }: AgentProcessingProps) {
  const [steps, setSteps] = useState<AgentStep[]>([]);
  const [currentMessage, setCurrentMessage] = useState("");
  const [dots, setDots] = useState("");

  useEffect(() => {
    if (isProcessing && agents.length > 0) {
      // Initialize steps
      const initialSteps: AgentStep[] = agents.slice(0, 5).map((agent, idx) => ({
        agentName: agent,
        status: idx === 0 ? "thinking" : "waiting",
      }));
      setSteps(initialSteps);
    } else {
      setSteps([]);
    }
  }, [isProcessing, agents]);

  // Animate dots
  useEffect(() => {
    if (!isProcessing) return;
    const interval = setInterval(() => {
      setDots(prev => prev.length >= 3 ? "" : prev + ".");
    }, 500);
    return () => clearInterval(interval);
  }, [isProcessing]);

  // Cycle through messages
  useEffect(() => {
    if (!isProcessing) return;
    const messages = [...thinkingMessages, ...communicatingMessages];
    let idx = 0;
    setCurrentMessage(messages[0]);
    const interval = setInterval(() => {
      idx = (idx + 1) % messages.length;
      setCurrentMessage(messages[idx]);
    }, 3000);
    return () => clearInterval(interval);
  }, [isProcessing]);

  // Simulate agent progress
  useEffect(() => {
    if (!isProcessing || steps.length === 0) return;
    
    const progressInterval = setInterval(() => {
      setSteps(prev => {
        const newSteps = [...prev];
        const thinkingIdx = newSteps.findIndex(s => s.status === "thinking");
        const communicatingIdx = newSteps.findIndex(s => s.status === "communicating");
        
        if (communicatingIdx !== -1) {
          // Move from communicating to done
          newSteps[communicatingIdx].status = "done";
          // Start next agent thinking
          const nextWaiting = newSteps.findIndex(s => s.status === "waiting");
          if (nextWaiting !== -1) {
            newSteps[nextWaiting].status = "thinking";
          }
        } else if (thinkingIdx !== -1) {
          // Move from thinking to communicating
          newSteps[thinkingIdx].status = "communicating";
        }
        
        return newSteps;
      });
    }, 2500);

    return () => clearInterval(progressInterval);
  }, [isProcessing, steps.length]);

  if (!isProcessing) return null;

  return (
    <div className="w-full p-4 rounded-lg border border-[var(--color-border)] bg-[var(--color-surface)]/50 backdrop-blur-sm">
      {/* Header */}
      <div className="flex items-center gap-3 mb-4">
        <div className="relative">
          <Brain className="h-6 w-6 text-[var(--color-primary)] animate-pulse" />
          <Sparkles className="h-3 w-3 text-[var(--color-accent)] absolute -top-1 -right-1 animate-ping" />
        </div>
        <div>
          <h3 className="font-bold text-[var(--color-text)]">
            Agentes Procesando{dots}
          </h3>
          <p className="text-xs text-[var(--color-text-muted)]">
            {currentMessage}
          </p>
        </div>
      </div>

      {/* Agent Pipeline */}
      <div className="space-y-2">
        {steps.map((step, idx) => (
          <div key={step.agentName} className="flex items-center gap-2">
            {/* Status Icon */}
            <div className={cn(
              "w-8 h-8 rounded-full flex items-center justify-center transition-all duration-300",
              step.status === "waiting" && "bg-[var(--color-border)]",
              step.status === "thinking" && "bg-[var(--color-primary)]/20 animate-pulse",
              step.status === "communicating" && "bg-[var(--color-accent)]/20",
              step.status === "done" && "bg-green-500/20"
            )}>
              {step.status === "waiting" && (
                <div className="w-2 h-2 rounded-full bg-[var(--color-text-muted)]" />
              )}
              {step.status === "thinking" && (
                <Loader2 className="h-4 w-4 text-[var(--color-primary)] animate-spin" />
              )}
              {step.status === "communicating" && (
                <MessageSquare className="h-4 w-4 text-[var(--color-accent)] animate-bounce" />
              )}
              {step.status === "done" && (
                <CheckCircle className="h-4 w-4 text-green-500" />
              )}
            </div>

            {/* Agent Name */}
            <div className="flex-1">
              <span className={cn(
                "text-sm font-medium transition-colors",
                step.status === "waiting" && "text-[var(--color-text-muted)]",
                step.status === "thinking" && "text-[var(--color-primary)]",
                step.status === "communicating" && "text-[var(--color-accent)]",
                step.status === "done" && "text-green-500"
              )}>
                {agentDisplayNames[step.agentName] || step.agentName}
              </span>
              {step.status === "thinking" && (
                <span className="text-xs text-[var(--color-text-muted)] ml-2">
                  Pensando...
                </span>
              )}
              {step.status === "communicating" && (
                <span className="text-xs text-[var(--color-text-muted)] ml-2">
                  Comunicando con otros agentes...
                </span>
              )}
            </div>

            {/* Connection Line */}
            {idx < steps.length - 1 && (
              <div className={cn(
                "hidden sm:flex items-center gap-1",
                step.status === "done" ? "text-green-500" : "text-[var(--color-border)]"
              )}>
                <div className={cn(
                  "w-8 h-0.5",
                  step.status === "done" ? "bg-green-500" : "bg-[var(--color-border)]",
                  step.status === "communicating" && "animate-pulse bg-[var(--color-accent)]"
                )} />
                <ArrowRight className="h-3 w-3" />
              </div>
            )}
          </div>
        ))}
      </div>

      {/* Progress Bar */}
      <div className="mt-4 h-1 bg-[var(--color-border)] rounded-full overflow-hidden">
        <div 
          className="h-full bg-gradient-to-r from-[var(--color-primary)] to-[var(--color-accent)] transition-all duration-500"
          style={{ 
            width: `${(steps.filter(s => s.status === "done").length / steps.length) * 100}%` 
          }}
        />
      </div>

      {/* Matrix Effect for Hacker Theme */}
      <div className="mt-3 font-mono text-[10px] text-[var(--color-primary)]/50 overflow-hidden h-4">
        <div className="animate-pulse">
          {Array.from({ length: 50 }, () => Math.random() > 0.5 ? "1" : "0").join("")}
        </div>
      </div>
    </div>
  );
}

// Componente de mensaje de agente en el chat
export function AgentMessage({ 
  agentName, 
  content, 
  isThinking 
}: { 
  agentName: string; 
  content: string; 
  isThinking?: boolean;
}) {
  return (
    <div className="flex gap-3 p-3 rounded-lg bg-[var(--color-surface)]/30 border border-[var(--color-border)]">
      <div className={cn(
        "w-8 h-8 rounded-full flex items-center justify-center shrink-0",
        "bg-[var(--color-primary)]/20 border border-[var(--color-primary)]/50"
      )}>
        {isThinking ? (
          <Loader2 className="h-4 w-4 text-[var(--color-primary)] animate-spin" />
        ) : (
          <Zap className="h-4 w-4 text-[var(--color-primary)]" />
        )}
      </div>
      <div className="flex-1 min-w-0">
        <div className="flex items-center gap-2 mb-1">
          <span className="font-bold text-sm text-[var(--color-primary)]">
            {agentDisplayNames[agentName] || agentName}
          </span>
          {isThinking && (
            <span className="text-xs text-[var(--color-text-muted)] animate-pulse">
              pensando...
            </span>
          )}
        </div>
        <p className="text-sm text-[var(--color-text)] whitespace-pre-wrap">
          {content}
        </p>
      </div>
    </div>
  );
}
