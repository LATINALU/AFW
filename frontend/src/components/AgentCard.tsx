"use client";

import { Card, CardContent, CardHeader, CardTitle } from "@/components/ui/card";
import { Badge } from "@/components/ui/badge";
import { cn } from "@/lib/utils";
import {
  Brain,
  Target,
  Search,
  BarChart3,
  Layers,
  AlertTriangle,
  Code2,
  PenTool,
  Database,
  MessageSquare,
  Scale,
  Lightbulb,
  Gavel,
  DollarSign,
  Palette,
  Cpu,
  GraduationCap,
  Megaphone,
  CheckCircle2,
  FileText,
  Zap,
  Shield,
  Link2,
  Eye,
  Languages,
  FileSearch,
  Layout,
  CheckSquare,
  Users,
  HelpCircle
} from "lucide-react";
import { AGENT_DETAILS } from "@/data/agentDetails";

interface AgentCardProps {
  name: string;
  internalName?: string;
  role: string;
  level: number;
  goal?: string;
  backstory?: string;
  isSelected?: boolean;
  isActive?: boolean;
  onClick?: () => void;
}


const levelVariants: Record<number, string> = {
  1: "level1",
  2: "level2",
  3: "level3",
  4: "level4",
  5: "level5",
};

const levelColors: Record<number, string> = {
  1: "border-red-500/50 hover:border-red-500 hover:shadow-[0_0_20px_rgba(255,0,64,0.3)]",
  2: "border-orange-500/50 hover:border-orange-500 hover:shadow-[0_0_20px_rgba(255,102,0,0.3)]",
  3: "border-yellow-500/50 hover:border-yellow-500 hover:shadow-[0_0_20px_rgba(255,255,0,0.3)]",
  4: "border-cyan-500/50 hover:border-cyan-500 hover:shadow-[0_0_20px_rgba(0,212,255,0.3)]",
  5: "border-purple-500/50 hover:border-purple-500 hover:shadow-[0_0_20px_rgba(189,0,255,0.3)]",
};

const agentIcons: Record<string, React.ComponentType<{ className?: string }>> = {
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
  innovation: Lightbulb,
  summary: FileSearch,
  formatting: Layout,
  validation: CheckSquare,
  coordination: Users,
  explanation: HelpCircle,
};

interface AgentModel {
  id: string;
  name: string;
}

interface AgentCardPropsExtended extends AgentCardProps {
  availableModels?: AgentModel[];
  selectedModel?: string;
  onModelChange?: (agentName: string, modelId: string) => void;
  customInstructions?: string;
  onInstructionsChange?: (agentName: string, instructions: string) => void;
  onShowDetails?: (agentName: string) => void;
}

export function AgentCard({
  name,
  internalName,
  role,
  level,
  isSelected,
  isActive,
  onClick,
  availableModels = [],
  selectedModel,
  onModelChange,
  customInstructions = "",
  onInstructionsChange,
  onShowDetails,
}: AgentCardPropsExtended) {
  const agentKey = internalName || name;
  const Icon = agentIcons[agentKey] || Brain;
  const levelColor = levelColors[level] || levelColors[1];
  const badgeVariant = levelVariants[level] as "level1" | "level2" | "level3" | "level4" | "level5";
  const details = AGENT_DETAILS[agentKey];

  return (
    <Card
      className={cn(
        "cursor-pointer transition-all duration-300 relative overflow-hidden group w-full min-w-0 max-w-full mx-auto text-[13px]",
        levelColor,
        isSelected
          ? "ring-2 ring-primary shadow-[0_0_25px_rgba(0,255,65,0.4)] bg-primary/10 border-primary"
          : "hover:shadow-xl",
        isActive && "animate-pulse"
      )}
      onClick={onClick}
    >
      {/* Selected indicator - Top bar */}
      {isSelected && (
        <div className="absolute top-0 left-0 right-0 h-1 bg-gradient-to-r from-primary via-green-400 to-primary animate-pulse" />
      )}

      {/* Scan line effect on hover */}
      <div className="absolute inset-0 opacity-0 group-hover:opacity-100 transition-opacity pointer-events-none">
        <div className="absolute inset-0 bg-gradient-to-b from-transparent via-primary/5 to-transparent animate-scan-line" />
      </div>

      <CardHeader className="pb-1 pt-2">
        <div className="flex items-center justify-between">
          <div className={cn(
            "p-2 rounded-xl border-2 transition-all",
            isSelected
              ? "bg-primary/30 border-primary shadow-lg"
              : "bg-primary/10 border-primary/30"
          )}>
            <Icon className={cn(
              "h-5 w-5 transition-all",
              isSelected ? "text-primary animate-pulse" : "text-primary"
            )} />
          </div>
          <Badge
            variant={badgeVariant}
            className={cn(
              "transition-all",
              isSelected && "ring-2 ring-primary shadow-lg"
            )}
          >
            L{level}
          </Badge>
        </div>
        <CardTitle className={cn(
          "text-[13px] mt-2 line-clamp-1 transition-all",
          isSelected && "text-primary font-bold"
        )}>
          {name?.replace(/_/g, " ").replace(/agent/i, "").trim() || name}
        </CardTitle>
      </CardHeader>

      <CardContent className="pb-2 space-y-2">
        {/* Role */}
        <p className="text-[11px] text-muted-foreground line-clamp-1">{role}</p>

        {/* Goal - Always visible */}
        {details && (
          <div className={cn(
            "p-2 rounded-lg transition-all",
            isSelected ? "bg-primary/20 border border-primary/40" : "bg-primary/5 border border-primary/20"
          )}>
            <p className="text-[11px] text-foreground line-clamp-2">{details.goal}</p>
          </div>
        )}

        {/* Skills - Always visible */}
        {details && (
          <div>
            <div className="flex flex-wrap gap-1">
              {details.skills.slice(0, 2).map((skill) => (
                <span
                  key={skill}
                  className={cn(
                    "px-2 py-0.5 text-[9px] font-medium rounded-full border transition-all",
                    isSelected
                      ? "bg-primary/30 text-primary border-primary/60"
                      : "bg-primary/10 text-primary border-primary/30"
                  )}
                >
                  {skill}
                </span>
              ))}
              {details.skills.length > 2 && (
                <span className="text-[9px] text-muted-foreground px-1">+{details.skills.length - 2}</span>
              )}
            </div>
          </div>
        )}

        {/* Resumen de configuración */}
        {(selectedModel || customInstructions) && (
          <div className="text-[10px] text-muted-foreground space-y-1">
            {selectedModel && (
              <p className="truncate">
                <span className="font-semibold text-primary">Modelo:</span>{" "}
                {availableModels.find((m) => m.id === selectedModel)?.name || "Custom"}
              </p>
            )}
            {customInstructions && (
              <p className="line-clamp-2">
                <span className="font-semibold text-primary">Notas:</span>{" "}
                {customInstructions}
              </p>
            )}
          </div>
        )}

        {/* Status indicators */}
        {isActive && (
          <div className="flex items-center gap-1 mb-2">
            <div className="h-2 w-2 rounded-full bg-green-500 animate-pulse" />
            <span className="text-xs text-green-400">Procesando...</span>
          </div>
        )}

        {/* Config toggle button */}
        <button
          onClick={(e) => {
            e.stopPropagation();
            onShowDetails?.(agentKey);
          }}
          className={cn(
            "w-full px-2 py-1 text-[11px] font-semibold border rounded transition-all flex items-center justify-center gap-1",
            isSelected
              ? "bg-primary/20 hover:bg-primary/30 text-primary border-primary shadow-md"
              : "bg-primary/10 hover:bg-primary/20 text-primary border-primary/30"
          )}
        >
          <Eye className="h-3 w-3" />
          Ver más / Configurar
        </button>
      </CardContent>
    </Card>
  );
}
