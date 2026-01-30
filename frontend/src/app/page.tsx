"use client";

/**
 * AFW v0.8.0 - Agents For Works
 * 120 Agentes Especializados en 12 Categorías
 * ==========================================
 */

import { useState, useEffect } from "react";
import { StreamingChatV2 } from "@/components/StreamingChatV2";
import { AppSettings } from "@/components/AppSettings";
import { LanguageSelector } from "@/components/LanguageSelector";
import { Settings, Cpu, Activity, Zap, ChevronDown } from "lucide-react";
import { Button } from "@/components/ui/button";
import { cn } from "@/lib/utils";

export default function HomePage() {
  const [isSettingsOpen, setIsSettingsOpen] = useState(false);
  const [selectedAgents, setSelectedAgents] = useState<string[]>([]);
  const [model, setModel] = useState("groq-default");
  const [apiConfig, setApiConfig] = useState({
    id: "groq",
    name: "Groq",
    type: "groq",
    apiKey: "",
    baseUrl: "https://api.groq.com/openai/v1",
    models: ["llama-3.3-70b-versatile"],
    isActive: true,
  });
  const [agentInstructions, setAgentInstructions] = useState<Record<string, string>>({});

  return (
    <div className="min-h-screen bg-background">
      {/* Header */}
      <header className="border-b border-border bg-background/95 backdrop-blur supports-[backdrop-filter:blur(0)]">
        <div className="container mx-auto px-4 py-4">
          <div className="flex items-center justify-between">
            <div className="flex items-center gap-3">
              <div className="h-8 w-8 rounded-lg bg-gradient-to-br from-blue-500 to-cyan-500 flex items-center justify-center">
                <span className="text-white font-bold text-sm">A</span>
              </div>
              <div>
                <h1 className="text-xl font-bold text-foreground">AFW</h1>
                <p className="text-xs text-muted-foreground">Agents For Work</p>
              </div>
            </div>
            
            <div className="flex items-center gap-2">
              <LanguageSelector />
              <Button
                variant="outline"
                size="sm"
                onClick={() => setIsSettingsOpen(true)}
              >
                <Settings className="h-4 w-4" />
              </Button>
            </div>
          </div>
        </div>
      </header>

      {/* Main Content */}
      <main className="container mx-auto px-4 py-8">
        <div className="text-center mb-8">
          <h2 className="text-3xl font-bold text-foreground mb-4">
            120 Agentes de IA Especializados
          </h2>
          <p className="text-lg text-muted-foreground max-w-2xl mx-auto">
            Plataforma de agentes de IA con capacidad extrema de razonamiento para desarrollo, marketing, finanzas y más.
          </p>
        </div>

        {/* Chat Interface */}
        <div className="max-w-4xl mx-auto">
          <StreamingChatV2
            selectedAgents={selectedAgents}
            model={model}
            apiConfig={apiConfig}
            onAgentModelChange={(agent, newModel) => setModel(newModel)}
            agentInstructions={agentInstructions}
            onAgentInstructionsChange={(agentId, instructions) => setAgentInstructions(prev => ({...prev, [agentId]: instructions}))}
            onShowAgentDetails={() => {}}
          />
        </div>
      </main>

      {/* Settings Modal */}
      <AppSettings
        isOpen={isSettingsOpen}
        onClose={() => setIsSettingsOpen(false)}
        onProvidersChange={() => {}}
      />
    </div>
  );
}
