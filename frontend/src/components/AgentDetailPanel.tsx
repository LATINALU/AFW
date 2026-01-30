"use client";

import { useEffect, useState } from "react";
import { AGENT_DETAILS } from "@/data/agentDetails";
import { X } from "lucide-react";

interface AgentDetailPanelProps {
  agentName: string;
  role: string;
  level: number;
  selectedModel?: string;
  availableModels?: { id: string; name: string }[];
  instructions?: string;
  onClose: () => void;
  onModelChange?: (agentName: string, modelId: string) => void;
  onInstructionsChange?: (agentName: string, instructions: string) => void;
}

export function AgentDetailPanel({
  agentName,
  role,
  level,
  selectedModel,
  availableModels = [],
  instructions = "",
  onClose,
  onModelChange,
  onInstructionsChange,
}: AgentDetailPanelProps) {
  const [localInstructions, setLocalInstructions] = useState(instructions);
  const details = AGENT_DETAILS[agentName];

  useEffect(() => {
    setLocalInstructions(instructions);
  }, [instructions]);

  return (
    <div className="fixed inset-0 z-[1000] flex items-center justify-center p-4 pointer-events-none">
      <div
        className="absolute inset-0 bg-gradient-to-b from-background/20 via-background/10 to-background/20 backdrop-blur-sm pointer-events-auto"
        onClick={onClose}
      />
      <div className="relative z-10 w-full max-w-3xl max-h-[95vh] overflow-y-auto rounded-3xl border border-primary/30 bg-card/95 shadow-[0_0_60px_rgba(0,0,0,0.45)] pointer-events-auto">
        <div className="flex items-start justify-between gap-4 border-b border-primary/20 px-6 py-5 sticky top-0 bg-card/95 backdrop-blur">
          <div>
            <p className="text-xs text-muted-foreground uppercase tracking-[0.3em]">Agente L{level}</p>
            <h2 className="text-2xl font-semibold text-primary capitalize">
              {agentName.replace(/_/g, " ")}
            </h2>
            <p className="text-sm text-muted-foreground mt-1 max-w-2xl">{role}</p>
          </div>
          <button
            className="p-2 rounded-full border border-border hover:border-primary hover:text-primary transition-colors"
            onClick={onClose}
            aria-label="Cerrar"
          >
            <X className="h-4 w-4" />
          </button>
        </div>

        <div className="px-6 py-6 space-y-6">
          {details && (
            <div className="space-y-4">
              <section>
                <h3 className="text-sm font-semibold text-primary mb-2">Objetivo</h3>
                <p className="text-sm text-foreground leading-relaxed">{details.goal}</p>
              </section>
              <section>
                <h3 className="text-sm font-semibold text-primary mb-2">Historia</h3>
                <p className="text-sm text-muted-foreground leading-relaxed">
                  {details.backstory}
                </p>
              </section>
              <section>
                <h3 className="text-sm font-semibold text-primary mb-2">Habilidades clave</h3>
                <div className="flex flex-wrap gap-1.5">
                  {details.skills.map((skill) => (
                    <span
                      key={skill}
                      className="px-3 py-1 text-[11px] font-medium rounded-full border border-primary/30 bg-primary/5 text-primary"
                    >
                      {skill}
                    </span>
                  ))}
                </div>
              </section>
            </div>
          )}

          <section className="space-y-4">
            <div>
              <h3 className="text-sm font-semibold text-primary mb-2">Modelo preferido</h3>
              {availableModels.length > 0 ? (
                <select
                  value={selectedModel || ""}
                  onChange={(e) => onModelChange?.(agentName, e.target.value)}
                  className="w-full text-sm px-3 py-2 rounded-lg border border-border bg-background text-foreground focus:outline-none focus:ring-1 focus:ring-primary/50"
                >
                  <option value="">🤖 Usar modelo por defecto</option>
                  {availableModels.map((model) => (
                    <option key={model.id} value={model.id}>
                      {model.name}
                    </option>
                  ))}
                </select>
              ) : (
                <p className="text-xs text-muted-foreground">
                  No hay modelos adicionales configurados.
                </p>
              )}
            </div>

            <div>
              <h3 className="text-sm font-semibold text-primary mb-2">Instrucciones específicas</h3>
              <textarea
                value={localInstructions}
                onChange={(e) => {
                  setLocalInstructions(e.target.value);
                  onInstructionsChange?.(agentName, e.target.value);
                }}
                placeholder="Define estilo, tono, pasos o restricciones para este agente..."
                className="w-full text-sm px-3 py-2 rounded-lg border border-border bg-background text-foreground focus:outline-none focus:ring-1 focus:ring-primary/50 min-h-[140px]"
              />
            </div>
          </section>
        </div>
      </div>
    </div>
  );
}
