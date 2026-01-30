"use client";

import { cn } from "@/lib/utils";
import { 
  Brain, Target, Search, BarChart3, Layers, AlertTriangle,
  Code2, PenTool, Database, MessageSquare, Scale, Lightbulb,
  Gavel, DollarSign, Palette, Cpu, GraduationCap, Megaphone,
  CheckCircle2, FileText, Zap, Shield, Link2, Eye,
  Languages, FileSearch, Layout, CheckSquare, Users, HelpCircle,
  Clock
} from "lucide-react";
import { Badge } from "@/components/ui/badge";
import ReactMarkdown from "react-markdown";

interface AgentResponseCardProps {
  agentId: string;
  agentName: string;
  level: number;
  specialty: string;
  content: string;
  timestamp: Date;
  isLatest?: boolean;
  conversationId?: string;
  messageId?: string;
  onSaveResponse?: (data: {
    agentId: string;
    agentName: string;
    content: string;
    conversationId?: string;
    messageId?: string;
  }) => void;
}

const LEVEL_CONFIG: Record<number, { 
  color: string; 
  bgColor: string; 
  borderColor: string;
  glowColor: string;
  label: string;
  emoji: string;
}> = {
  1: { 
    color: "text-blue-400", 
    bgColor: "bg-blue-500/10", 
    borderColor: "border-l-blue-500",
    glowColor: "shadow-blue-500/20",
    label: "Logic & Foundation",
    emoji: "🧠"
  },
  2: { 
    color: "text-emerald-400", 
    bgColor: "bg-emerald-500/10", 
    borderColor: "border-l-emerald-500",
    glowColor: "shadow-emerald-500/20",
    label: "Production Professional",
    emoji: "💼"
  },
  3: { 
    color: "text-amber-400", 
    bgColor: "bg-amber-500/10", 
    borderColor: "border-l-amber-500",
    glowColor: "shadow-amber-500/20",
    label: "Specialized Domains",
    emoji: "🎓"
  },
  4: { 
    color: "text-rose-400", 
    bgColor: "bg-rose-500/10", 
    borderColor: "border-l-rose-500",
    glowColor: "shadow-rose-500/20",
    label: "Operational Support",
    emoji: "🔧"
  },
  5: { 
    color: "text-violet-400", 
    bgColor: "bg-violet-500/10", 
    borderColor: "border-l-violet-500",
    glowColor: "shadow-violet-500/20",
    label: "Strategic Auxiliaries",
    emoji: "✨"
  },
};

const AGENT_ICONS: Record<string, React.ComponentType<{ className?: string }>> = {
  reasoning: Brain,
  planning: Target,
  research: Search,
  analysis: BarChart3,
  synthesis: Layers,
  critical_thinking: AlertTriangle,
  coding: Code2,
  writing: PenTool,
  data: Database,
  communication: MessageSquare,
  decision: Scale,
  problem_solving: Lightbulb,
  legal: Gavel,
  financial: DollarSign,
  creative: Palette,
  technical: Cpu,
  educational: GraduationCap,
  marketing: Megaphone,
  qa: CheckCircle2,
  documentation: FileText,
  optimization: Zap,
  security: Shield,
  integration: Link2,
  review: Eye,
  translation: Languages,
  summary: FileSearch,
  formatting: Layout,
  validation: CheckSquare,
  coordination: Users,
  explanation: HelpCircle,
};

export function AgentResponseCard({
  agentId,
  agentName,
  level,
  specialty,
  content,
  timestamp,
  isLatest = false,
  conversationId,
  messageId,
  onSaveResponse,
}: AgentResponseCardProps) {
  const config = LEVEL_CONFIG[level] || LEVEL_CONFIG[3];
  const Icon = AGENT_ICONS[agentId] || Brain;
  const displayName = agentName.replace(/_/g, " ").replace(/agent/i, "").trim();

  return (
    <div 
      className={cn(
        "agent-response-card relative rounded-xl border-l-4 overflow-hidden transition-all duration-300",
        config.borderColor,
        config.bgColor,
        "hover:shadow-lg",
        isLatest && `shadow-lg ${config.glowColor}`,
        "animate-in fade-in slide-in-from-left-2"
      )}
      data-level={level}
      data-agent={agentId}
    >
      {/* Header */}
      <div className={cn(
        "flex items-center justify-between px-4 py-3 border-b border-white/10",
        config.bgColor
      )}>
        <div className="flex items-center gap-3">
          {/* Agent Icon */}
          <div className={cn(
            "p-2 rounded-lg border",
            config.bgColor,
            `border-${config.color.replace('text-', '')}/30`
          )}>
            <Icon className={cn("h-5 w-5", config.color)} />
          </div>
          
          {/* Agent Info */}
          <div className="flex flex-col">
            <div className="flex items-center gap-2">
              <span className={cn("font-bold text-base", config.color)}>
                {config.emoji} {displayName}
              </span>
              <Badge 
                variant="outline" 
                className={cn(
                  "text-xs font-semibold",
                  config.color,
                  "border-current/50 bg-transparent"
                )}
              >
                Nivel {level}
              </Badge>
            </div>
            <span className="text-xs text-muted-foreground italic">
              {specialty}
            </span>
          </div>
        </div>

        {/* Level Category */}
        <div className="hidden sm:flex items-center gap-2">
          <span className={cn("text-xs font-medium px-2 py-1 rounded-full", config.bgColor, config.color)}>
            {config.label}
          </span>
        </div>
      </div>

      {/* Content */}
      <div className="px-4 py-4">
        <div className="prose prose-invert prose-sm max-w-none">
          <ReactMarkdown
            components={{
              h1: ({ children }) => <h1 className={cn("text-xl font-bold mb-3", config.color)}>{children}</h1>,
              h2: ({ children }) => <h2 className={cn("text-lg font-semibold mb-2", config.color)}>{children}</h2>,
              h3: ({ children }) => <h3 className={cn("text-base font-medium mb-2", config.color)}>{children}</h3>,
              p: ({ children }) => <p className="text-foreground/90 leading-relaxed mb-3">{children}</p>,
              ul: ({ children }) => <ul className="list-disc list-inside space-y-1 mb-3">{children}</ul>,
              ol: ({ children }) => <ol className="list-decimal list-inside space-y-1 mb-3">{children}</ol>,
              li: ({ children }) => <li className="text-foreground/85">{children}</li>,
              code: ({ children, className }) => {
                const isInline = !className;
                return isInline ? (
                  <code className={cn("px-1.5 py-0.5 rounded text-xs sm:text-sm font-mono", config.bgColor, config.color)}>
                    {children}
                  </code>
                ) : (
                  <code className="block p-2 sm:p-3 rounded-lg bg-black/30 text-xs sm:text-sm font-mono overflow-x-auto whitespace-pre-wrap break-words">
                    {children}
                  </code>
                );
              },
              blockquote: ({ children }) => (
                <blockquote className={cn("border-l-2 pl-4 italic my-3", config.borderColor, "text-foreground/80")}>
                  {children}
                </blockquote>
              ),
              strong: ({ children }) => <strong className={cn("font-bold", config.color)}>{children}</strong>,
            }}
          >
            {content}
          </ReactMarkdown>
        </div>
      </div>

      {/* Footer */}
      <div className={cn(
        "flex items-center justify-between px-4 py-2 border-t border-white/5",
        "bg-black/20"
      )}>
        <div className="flex items-center gap-1 text-xs text-muted-foreground">
          <Clock className="h-3 w-3" />
          <span>{timestamp.toLocaleTimeString()}</span>
        </div>
        <div className="flex items-center gap-2">
          {onSaveResponse && (
            <button
              onClick={() => onSaveResponse({
                agentId,
                agentName,
                content,
                conversationId,
                messageId
              })}
              className={cn(
                "px-3 py-1 rounded-md text-xs font-medium transition-all",
                "hover:scale-105 active:scale-95",
                config.bgColor,
                config.color,
                "border border-current/30"
              )}
              title="Guardar respuesta"
            >
              💾 Guardar
            </button>
          )}
          <span className={cn("text-xs font-mono", config.color)}>
            @{agentId}
          </span>
        </div>
      </div>
    </div>
  );
}

export function AgentResponseList({ 
  responses 
}: { 
  responses: Array<{
    agent_id: string;
    agent_name: string;
    level: number;
    specialty: string;
    content: string;
    timestamp: Date;
  }> 
}) {
  if (!responses || responses.length === 0) return null;

  // Sort by level for hierarchical display
  const sortedResponses = [...responses].sort((a, b) => a.level - b.level);

  return (
    <div className="space-y-4">
      {/* Header */}
      <div className="flex items-center justify-between">
        <h3 className="text-lg font-bold text-primary flex items-center gap-2">
          🎯 Respuesta Multi-Experto
          <Badge variant="outline" className="text-xs">
            {responses.length} agente{responses.length > 1 ? 's' : ''}
          </Badge>
        </h3>
        <span className="text-xs text-muted-foreground italic">
          Análisis jerárquico por niveles de expertise
        </span>
      </div>

      {/* Level Status Indicators */}
      <div className="flex flex-wrap gap-2 pb-2 border-b border-primary/20">
        {[1, 2, 3, 4, 5].map((level) => {
          const config = LEVEL_CONFIG[level];
          const hasAgent = sortedResponses.some(r => r.level === level);
          return (
            <div 
              key={level}
              className={cn(
                "flex items-center gap-1.5 px-2 py-1 rounded-full text-xs transition-all",
                hasAgent 
                  ? cn(config.bgColor, config.color, "ring-1 ring-current/30")
                  : "bg-muted/30 text-muted-foreground opacity-50"
              )}
            >
              <div className={cn(
                "h-2 w-2 rounded-full",
                hasAgent ? "bg-current animate-pulse" : "bg-muted-foreground/30"
              )} />
              <span className="font-medium">N{level}</span>
            </div>
          );
        })}
      </div>

      {/* Response Cards */}
      <div className="space-y-4">
        {sortedResponses.map((response, index) => (
          <AgentResponseCard
            key={`${response.agent_id}-${index}`}
            agentId={response.agent_id}
            agentName={response.agent_name}
            level={response.level}
            specialty={response.specialty}
            content={response.content}
            timestamp={response.timestamp}
            isLatest={index === sortedResponses.length - 1}
          />
        ))}
      </div>
    </div>
  );
}

export { LEVEL_CONFIG, AGENT_ICONS };
