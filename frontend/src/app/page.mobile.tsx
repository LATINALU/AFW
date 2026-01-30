"use client";

/**
 * ATP Mobile/Tablet Version - Optimized for Small Screens
 * =======================================================
 */

import { useState, useEffect } from "react";
import { Sidebar } from "@/components/Sidebar";
import { StreamingChatV2 } from "@/components/StreamingChatV2";
import { AppSettings, ApiProvider } from "@/components/AppSettings";
import { LanguageSelector } from "@/components/LanguageSelector";
import { MobileActionButtons } from "@/components/mobile/MobileActionButtons";
import { MobileTasksPanel } from "@/components/mobile/MobileTasksPanel";
import { QuickStartGuide } from "@/components/QuickStartGuide";
import { Settings, Menu, X, Activity } from "lucide-react";
import { Button } from "@/components/ui/button";
import { cn } from "@/lib/utils";

const AGENTS_CONFIG = [
  { id: "reasoning", level: 1 },
  { id: "planning", level: 1 },
  { id: "research", level: 1 },
  { id: "analysis", level: 1 },
  { id: "synthesis", level: 1 },
  { id: "critical_thinking", level: 1 },
  { id: "coding", level: 2 },
  { id: "data", level: 2 },
  { id: "writing", level: 2 },
  { id: "communication", level: 2 },
  { id: "decision", level: 2 },
  { id: "problem_solving", level: 2 },
  { id: "legal", level: 3 },
  { id: "financial", level: 3 },
  { id: "creative", level: 3 },
  { id: "technical", level: 3 },
  { id: "educational", level: 3 },
  { id: "marketing", level: 3 },
  { id: "qa", level: 4 },
  { id: "documentation", level: 4 },
  { id: "optimization", level: 4 },
  { id: "security", level: 4 },
  { id: "integration", level: 4 },
  { id: "review", level: 4 },
  { id: "translation", level: 5 },
  { id: "summary", level: 5 },
  { id: "formatting", level: 5 },
  { id: "validation", level: 5 },
  { id: "coordination", level: 5 },
  { id: "explanation", level: 5 },
];

const DEFAULT_API_CONFIG: ApiProvider = {
  id: "groq",
  name: "Groq",
  type: "groq",
  apiKey: "",
  baseUrl: "https://api.groq.com/openai/v1",
  models: ["llama-3.3-70b-versatile", "openai/gpt-oss-120b"],
  isActive: true,
};

export default function MobilePage() {
  const [selectedAgents, setSelectedAgents] = useState<string[]>([]);
  const [isSidebarOpen, setIsSidebarOpen] = useState(false);
  const [isSettingsOpen, setIsSettingsOpen] = useState(false);
  const [apiConfig, setApiConfig] = useState<ApiProvider>(DEFAULT_API_CONFIG);
  const [tasksOpen, setTasksOpen] = useState(false);
  const [agentsOpen, setAgentsOpen] = useState(false);
  const [memoryOpen, setMemoryOpen] = useState(false);
  const [quickStartOpen, setQuickStartOpen] = useState(false);
  const [activeView, setActiveView] = useState<'agents' | 'tasks' | 'memory' | null>(null);

  const handleAgentToggle = (agentId: string) => {
    setSelectedAgents(prev => {
      const isSelected = prev.includes(agentId);
      if (isSelected) {
        return prev.filter(id => id !== agentId);
      } else {
        return [...prev, agentId];
      }
    });
  };

  const handleSelectAll = (level?: number) => {
    if (level) {
      const levelAgents = AGENTS_CONFIG.filter(a => a.level === level).map(a => a.id);
      setSelectedAgents(prev => {
        const allSelected = levelAgents.every(id => prev.includes(id));
        if (allSelected) {
          return prev.filter(id => !levelAgents.includes(id));
        } else {
          return Array.from(new Set([...prev, ...levelAgents]));
        }
      });
    } else {
      const allIds = AGENTS_CONFIG.map(a => a.id);
      setSelectedAgents(allIds);
    }
  };

  const handleClearAll = () => {
    setSelectedAgents([]);
  };

  return (
    <div className="h-screen flex flex-col bg-background overflow-hidden">
      {/* Mobile Header */}
      <header className="border-b border-primary/20 bg-card/50 backdrop-blur-sm px-3 py-2 shrink-0">
        <div className="flex items-center justify-between mb-1">
          <div className="h-8 w-8" />

          <h1 className="text-base font-black text-primary">ATP</h1>

          <Button
            variant="outline"
            size="sm"
            onClick={() => setIsSettingsOpen(true)}
            className="gap-2 bg-blue-500/10 border-blue-500/20 text-blue-500 hover:bg-blue-500/20"
          >
            <Settings className="h-4 w-4" />
            <span className="text-xs font-medium">Settings</span>
          </Button>
        </div>
        <div className="text-center">
          <div className="inline-flex items-center gap-2 px-3 py-1.5 bg-gradient-to-r from-blue-500/10 to-purple-500/10 dark:from-blue-500/20 dark:to-purple-500/20 border border-blue-500/20 dark:border-blue-500/30 rounded-full">
            <div className="w-2 h-2 bg-gradient-to-r from-blue-500 to-purple-500 rounded-full animate-pulse" />
            <a 
              href="https://atp-app.duckdns.org" 
              target="_blank" 
              rel="noopener noreferrer"
              className="text-sm font-bold bg-gradient-to-r from-blue-600 to-purple-600 dark:from-blue-400 dark:to-purple-400 bg-clip-text text-transparent hover:from-blue-500 hover:to-purple-500 transition-all duration-300 hover:scale-105"
            >
              atp-app.duckdns.org
            </a>
            <div className="w-2 h-2 bg-gradient-to-r from-purple-500 to-blue-500 rounded-full animate-pulse" />
          </div>
        </div>
      </header>

      {/* Main Content */}
      <main className="flex-1 overflow-hidden">
        <StreamingChatV2
          selectedAgents={selectedAgents}
          model={apiConfig.models[0] || "llama-3.3-70b-versatile"}
          apiConfig={apiConfig}
          onAgentModelChange={() => { }}
          agentInstructions={{}}
          onAgentInstructionsChange={() => { }}
          onShowAgentDetails={(agentId) => console.log('Show agent:', agentId)}
        />
      </main>

      {/* Sidebar Overlay */}
      {isSidebarOpen && (
        <div className="fixed inset-0 z-50 bg-black/50">
          <div
            className="absolute inset-0"
            onClick={() => {
              setIsSidebarOpen(false);
              setActiveView(null);
            }}
          />
          <div className="absolute left-0 top-0 h-full w-[85%] max-w-sm bg-background shadow-2xl">
            <div className="h-full flex flex-col">
              <div className="h-14 border-b border-primary/20 px-4 flex items-center justify-between shrink-0">
                <h2 className="text-lg font-black text-primary">Agentes</h2>
                <Button
                  variant="ghost"
                  size="icon"
                  onClick={() => {
                    setIsSidebarOpen(false);
                    setActiveView(null);
                  }}
                >
                  <X className="h-5 w-5" />
                </Button>
              </div>
              <div className="flex-1 overflow-hidden">
                <Sidebar
                  agents={AGENTS_CONFIG.map(a => ({
                    name: a.id,
                    role: `Level ${a.level} Agent`,
                    level: a.level
                  }))}
                  selectedAgents={selectedAgents}
                  onAgentToggle={handleAgentToggle}
                  onSelectAll={handleSelectAll}
                  onClearAll={handleClearAll}
                  forceExpanded={true}
                />
              </div>
            </div>
          </div>
        </div>
      )}

      {/* Settings Modal */}
      <AppSettings
        isOpen={isSettingsOpen}
        onClose={() => setIsSettingsOpen(false)}
        onProvidersChange={(providers) => {
          const active = providers.find(p => p.isActive);
          if (active) {
            setApiConfig({
              ...active,
              apiKey: active.apiKey || "",
            } as ApiProvider);
          }
        }}
      />

      {/* Mobile Action Buttons */}
      <MobileActionButtons
        onOpenAgents={() => {
          setIsSidebarOpen(true);
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

      {/* Tasks Panel */}
      <MobileTasksPanel
        isOpen={tasksOpen}
        onClose={() => {
          setTasksOpen(false);
          setActiveView(null);
        }}
        onSelectTask={(agents) => {
          setSelectedAgents(agents);
          setTasksOpen(false);
          setActiveView(null);
        }}
      />

      
      {/* Quick Start Guide */}
      <QuickStartGuide
        isOpen={quickStartOpen}
        onClose={() => setQuickStartOpen(false)}
      />

      {/* Floating Agent Counter */}
      {selectedAgents.length > 0 && (
        <div className="fixed bottom-20 right-4 bg-primary text-primary-foreground rounded-full px-4 py-2 shadow-lg">
          <span className="text-sm font-bold">{selectedAgents.length} Agents</span>
        </div>
      )}
    </div>
  );
}
