"use client";

/**
 * AFW Desktop Version - Agents For Works
 * 120 Agentes Especializados en 12 Categorías
 * =================================================
 */

import { useState, useEffect } from "react";
import { CategorySidebar } from "@/components/CategorySidebar";
import { getAgents, getCategories, Agent as ApiAgent, Category } from "@/lib/api";
import { StreamingChatV2 } from "@/components/StreamingChatV2";
import { AppSettings, ApiProvider } from "@/components/AppSettings";
import { AgentDetailPanel } from "@/components/AgentDetailPanel";
import { LanguageSelector } from "@/components/LanguageSelector";
import { Settings, Cpu, Activity, Zap, ChevronDown } from "lucide-react";
import { Button } from "@/components/ui/button";
import { SecureStorage } from "@/lib/encryption";
import { Message } from "@/types";
import { cn } from "@/lib/utils";
import { resetForPublicLaunch } from "@/lib/cleanup";

// AFW v0.5.0 - Los agentes se cargan dinámicamente desde la API

const DEFAULT_MODEL = "openai/gpt-oss-120b";

const DEFAULT_API_CONFIG: ApiProvider = {
  id: "groq",
  name: "Groq",
  type: "groq",
  apiKey: "",
  baseUrl: "https://api.groq.com/openai/v1",
  models: [],
  enabledModels: [],
  isActive: false,
};

export default function DesktopPage() {
  const [selectedAgents, setSelectedAgents] = useState<string[]>([]);
  const [isSettingsOpen, setIsSettingsOpen] = useState(false);
  const [providers, setProviders] = useState<ApiProvider[]>([]);
  const [apiConfig, setApiConfig] = useState<ApiProvider>(DEFAULT_API_CONFIG);
  const [selectedModel, setSelectedModel] = useState<string>(DEFAULT_MODEL);
  const [isConnected, setIsConnected] = useState(false);
  const [showModelDropdown, setShowModelDropdown] = useState(false);
  
  // AFW v0.5.0 - Estado para agentes y categorías
  const [agents, setAgents] = useState<ApiAgent[]>([]);
  const [categories, setCategories] = useState<Category[]>([]);

  // Load agents and categories from API
  useEffect(() => {
    const loadAgentsData = async () => {
      try {
        const [agentsRes, categoriesRes] = await Promise.all([
          getAgents(),
          getCategories()
        ]);
        setAgents(agentsRes.agents);
        setCategories(categoriesRes.categories);
      } catch (error) {
        console.error("Error loading agents:", error);
      }
    };
    loadAgentsData();
  }, []);

  // Load saved providers on mount
  useEffect(() => {
    // 🚀 LIMPIEZA PARA LANZAMIENTO PÚBLICO
    resetForPublicLaunch();
    
    const loadProviders = async () => {
      try {
        // Intentar cargar con SecureStorage primero
        let saved = null;
        try {
          saved = await SecureStorage.getItem("api-providers");
        } catch (e) {
          console.error("SecureStorage failed, trying localStorage:", e);
        }
        
        // Fallback a localStorage si SecureStorage falla o no hay datos
        if (!saved) {
          const localStorageData = localStorage.getItem("atp-api-providers");
          if (localStorageData) {
            saved = JSON.parse(localStorageData);
          }
        }
        
        if (saved && Array.isArray(saved)) {
          console.log("✅ Loaded providers:", saved.length);
          setProviders(saved);
          
          // Buscar proveedor activo con API key (más flexible)
          const active = saved.find((p: ApiProvider) => p.isActive && p.apiKey);
          if (active) {
            console.log("✅ Active provider found:", active.name);
            setApiConfig(active);
            
            // Usar primer modelo habilitado o primer modelo disponible
            const modelToUse = (active.enabledModels && active.enabledModels.length > 0) 
              ? active.enabledModels[0] 
              : (active.models && active.models.length > 0 
                ? active.models[0] 
                : DEFAULT_MODEL);
            
            setSelectedModel(modelToUse);
            setIsConnected(true);
          } else {
            console.log("⚠️ No active provider found");
            setIsConnected(false);
          }
        } else {
          console.log("⚠️ No saved providers found");
        }
      } catch (e) {
        console.error("Error loading providers:", e);
      }
    };
    loadProviders();
  }, []);

  // Get all enabled models from all active providers
  const getAllEnabledModels = () => {
    return providers
      .filter(p => p.isActive && (p.enabledModels?.length || 0) > 0)
      .flatMap(p => (p.enabledModels || []).map(m => ({ model: m, provider: p })));
  };

  // Agent Details State
  const [isAgentDetailOpen, setIsAgentDetailOpen] = useState(false);
  const [selectedAgentForDetails, setSelectedAgentForDetails] = useState<string | null>(null);

  const handleAgentToggle = (agentId: string) => {
    setSelectedAgents(prev => {
      const isSelected = prev.includes(agentId);
      if (isSelected) {
        return prev.filter(id => id !== agentId);
      } else {
        if (prev.length >= 5) return prev;
        return [...prev, agentId];
      }
    });
  };

  const handleSelectCategory = (categoryId: string) => {
    // Seleccionar todos los agentes de una categoría (max 10)
    const categoryAgents = agents.filter(a => a.category === categoryId).map(a => a.id);
    setSelectedAgents(prev => {
      // Si ya están todos seleccionados, deseleccionar
      if (categoryAgents.every(id => prev.includes(id))) {
        return prev.filter(id => !categoryAgents.includes(id));
      }
      // Agregar los que faltan (sin límite estricto para categorías)
      const newAgents = categoryAgents.filter(id => !prev.includes(id));
      return [...prev, ...newAgents];
    });
  };

  const handleClearAll = () => {
    setSelectedAgents([]);
  };

  const handlePresetSelect = (agents: string[]) => {
    setSelectedAgents(agents);
  };

  const handleShowAgentDetails = (agentId: string) => {
    setSelectedAgentForDetails(agentId);
    setIsAgentDetailOpen(true);
  };

  return (
    <div className="h-screen flex flex-col bg-background overflow-hidden relative">
      {/* Header Desktop */}
      <header className="h-16 border-b border-primary/20 bg-card/50 backdrop-blur-sm px-6 flex items-center justify-between shrink-0 relative z-20">
        <div className="flex items-center gap-4">
          <div className="h-12 w-12 rounded-xl bg-gradient-to-br from-primary/30 to-cyan-500/30 border border-primary/50 flex items-center justify-center">
            <span className="text-2xl font-black text-primary">🤖</span>
          </div>
          <div>
            <h1 className="text-xl font-black tracking-tight text-primary">AFW - Agents For Works</h1>
            <div className="inline-flex items-center gap-2 px-3 py-1.5 bg-gradient-to-r from-blue-500/10 to-purple-500/10 dark:from-blue-500/20 dark:to-purple-500/20 border border-blue-500/20 dark:border-blue-500/30 rounded-full">
              <div className="w-2 h-2 bg-gradient-to-r from-blue-500 to-purple-500 rounded-full animate-pulse" />
              <span className="text-sm font-bold bg-gradient-to-r from-blue-600 to-purple-600 dark:from-blue-400 dark:to-purple-400 bg-clip-text text-transparent">
                120 Agentes • 12 Categorías
              </span>
              <div className="w-2 h-2 bg-gradient-to-r from-purple-500 to-blue-500 rounded-full animate-pulse" />
            </div>
          </div>
        </div>

        {/* Centered Connection Status + Model Selector */}
        <div className="absolute left-1/2 top-1/2 -translate-x-1/2 -translate-y-1/2 flex items-center gap-4">
          {/* Connection Status */}
          <div className={cn(
            "flex items-center gap-2 px-4 py-1.5 rounded-full border transition-all duration-500",
            isConnected
              ? "bg-green-500/10 border-green-500/30 text-green-500 shadow-[0_0_15px_rgba(34,197,94,0.2)]"
              : "bg-red-500/10 border-red-500/30 text-red-500 cursor-pointer hover:bg-red-500/20"
          )}
            onClick={() => !isConnected && setIsSettingsOpen(true)}
          >
            <Zap className={cn("h-4 w-4", isConnected && "fill-current animate-pulse")} />
            <span className="text-xs font-bold tracking-wider uppercase">
              {isConnected ? "ONLINE" : "DISCONNECTED"}
            </span>
          </div>

          {/* Model Selector Dropdown */}
          <div className="relative">
            <button
              onClick={() => setShowModelDropdown(!showModelDropdown)}
              className={cn(
                "flex items-center gap-2 px-4 py-1.5 rounded-full border transition-all duration-300",
                getAllEnabledModels().length > 0
                  ? "bg-primary/10 border-primary/30 text-primary hover:bg-primary/20"
                  : "bg-muted/30 border-border text-muted-foreground"
              )}
            >
              <Cpu className="h-4 w-4" />
              <span className="text-xs font-mono max-w-32 truncate">
                {selectedModel || "Sin modelo"}
              </span>
              <ChevronDown className={cn("h-3 w-3 transition-transform", showModelDropdown && "rotate-180")} />
            </button>

            {showModelDropdown && getAllEnabledModels().length > 0 && (
              <>
                <div className="fixed inset-0 z-30" onClick={() => setShowModelDropdown(false)} />
                <div className="absolute top-full left-0 mt-2 min-w-64 bg-card border border-border rounded-lg shadow-xl z-40 max-h-64 overflow-y-auto">
                  {providers.filter(p => p.isActive && (p.enabledModels?.length || 0) > 0).map(provider => (
                    <div key={provider.id}>
                      <div className="px-3 py-2 bg-muted/30 text-[10px] font-bold text-muted-foreground uppercase tracking-wider">
                        {provider.name}
                      </div>
                      {(provider.enabledModels || []).map(model => (
                        <button
                          key={model}
                          onClick={() => {
                            setSelectedModel(model);
                            setApiConfig(provider);
                            setShowModelDropdown(false);
                          }}
                          className={cn(
                            "w-full flex items-center justify-between px-3 py-2 hover:bg-primary/10 transition-colors text-left",
                            model === selectedModel && "bg-primary/20 text-primary"
                          )}
                        >
                          <span className="text-xs font-mono truncate">{model}</span>
                          {model === selectedModel && <Zap className="h-3 w-3 text-primary" />}
                        </button>
                      ))}
                    </div>
                  ))}
                </div>
              </>
            )}
          </div>
        </div>

        <div className="flex items-center gap-3">
          <Button
            variant="outline"
            size="sm"
            onClick={() => setIsSettingsOpen(true)}
            className="gap-2"
          >
            <Settings className="h-4 w-4" />
            Settings
          </Button>
        </div>
      </header>

      {/* Main Content */}
      <div className="flex flex-1 overflow-hidden">
        {/* Sidebar - Fixed width for desktop */}
        <div className="w-80 border-r border-primary/20 flex-shrink-0 overflow-hidden">
          <CategorySidebar
            selectedAgents={selectedAgents}
            onAgentToggle={handleAgentToggle}
            onSelectCategory={handleSelectCategory}
            onClearAll={handleClearAll}
            isConnected={isConnected}
          />
        </div>

        {/* Chat Area - Takes remaining space */}
        <main className="flex-1 overflow-hidden">
          <StreamingChatV2
            selectedAgents={selectedAgents}
            model={selectedModel}
            apiConfig={apiConfig}
            onAgentModelChange={() => { }}
            agentInstructions={{}}
            onAgentInstructionsChange={() => { }}
            onShowAgentDetails={handleShowAgentDetails}
            onConnectionChange={setIsConnected}
            onSelectPreset={handlePresetSelect}
          />
        </main>
      </div>

      {/* Settings Modal */}
      <AppSettings
        isOpen={isSettingsOpen}
        onClose={() => setIsSettingsOpen(false)}
        onProvidersChange={(newProviders) => {
          setProviders(newProviders);
          const active = newProviders.find(p => p.isActive && ((p.enabledModels?.length || 0) > 0));
          if (active) {
            setApiConfig(active);
            // Set default model if not already selected from this provider
            if (!active.enabledModels?.includes(selectedModel)) {
              setSelectedModel(active.enabledModels?.[0] || DEFAULT_MODEL);
            }
            setIsConnected(true);
          } else {
            setIsConnected(false);
          }
        }}
      />

      {/* Agent Detail Modal */}
      {isAgentDetailOpen && selectedAgentForDetails && (
        (() => {
          const agentConfig = agents.find(a => a.id === selectedAgentForDetails);
          return (
            <AgentDetailPanel
              agentName={agentConfig?.name || selectedAgentForDetails}
              role={agentConfig ? `${agentConfig.emoji} ${agentConfig.specialization}` : "Agente"}
              level={1}
              selectedModel={undefined}
              availableModels={apiConfig.models.map(m => ({ id: m, name: m }))}
              onModelChange={() => { }}
              instructions=""
              onInstructionsChange={() => { }}
              onClose={() => setIsAgentDetailOpen(false)}
            />
          );
        })()
      )}


    </div>
  );
}
