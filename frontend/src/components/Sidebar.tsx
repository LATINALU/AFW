"use client";

import { useState, useEffect } from "react";
import { ScrollArea } from "@/components/ui/scroll-area";
import { Button } from "@/components/ui/button";
import { Badge } from "@/components/ui/badge";
import { Tabs, TabsContent, TabsList, TabsTrigger } from "@/components/ui/tabs";
import { AgentCard } from "@/components/AgentCard";
import { cn } from "@/lib/utils";
import {
  ChevronLeft,
  ChevronRight,
  Cpu,
  Zap,
  User,
  LogOut,
} from "lucide-react";
import { getCurrentLanguage } from "@/lib/i18n";
import { AuthModal } from "@/components/AuthModal";
import { ProfileModal } from "@/components/ProfileModal";
import { useAuth } from "@/components/AuthProvider";

interface Agent {
  name: string;
  displayName?: string;
  role: string;
  level: number;
}

interface AvailableModel {
  id: string;
  name: string;
  provider: string;
}

interface SidebarProps {
  agents: Agent[];
  selectedAgents: string[];
  onAgentToggle: (agentName: string) => void;
  onSelectAll: (level?: number) => void;
  onClearAll: () => void;
  availableModels?: AvailableModel[];
  agentModels?: Record<string, string>;
  onAgentModelChange?: (agentName: string, modelId: string) => void;
  agentInstructions?: Record<string, string>;
  onAgentInstructionsChange?: (agentName: string, instructions: string) => void;
  onShowAgentDetails?: (agentName: string) => void;
  isConnected?: boolean;
}

const levelNames: Record<string, Record<number, string>> = {
  es: {
    1: "Críticos",
    2: "Esenciales",
    3: "Especializados",
    4: "Soporte",
    5: "Auxiliares",
  },
  en: {
    1: "Critical",
    2: "Essential",
    3: "Specialized",
    4: "Support",
    5: "Auxiliary",
  }
};

const levelDescriptions: Record<string, Record<number, string>> = {
  es: {
    1: "Núcleo de razonamiento",
    2: "Capacidades fundamentales",
    3: "Dominios específicos",
    4: "Calidad y mantenimiento",
    5: "Funciones complementarias",
  },
  en: {
    1: "Reasoning core",
    2: "Fundamental capabilities",
    3: "Specific domains",
    4: "Quality & maintenance",
    5: "Complementary functions",
  }
};

export function Sidebar({
  agents,
  selectedAgents,
  onAgentToggle,
  onSelectAll,
  onClearAll,
  availableModels = [],
  agentModels = {},
  onAgentModelChange,
  agentInstructions = {},
  onAgentInstructionsChange,
  onShowAgentDetails,
  isConnected,
  forceExpanded = false,
}: SidebarProps & { forceExpanded?: boolean }) {
  // Default to false (open) on Desktop. Logic: !false = true (collapsed). 
  // We want it OPEN by default. So default should be FALSE.
  // If forceExpanded is true (mobile overlay), we want it OPEN.
  const [isCollapsed, setIsCollapsed] = useState(false);
  const [activeLevel, setActiveLevel] = useState("all");
  const [isMobile, setIsMobile] = useState(false);
  const [isTablet, setIsTablet] = useState(false);

  const lang = getCurrentLanguage();
  const currentLevelNames = levelNames[lang] || levelNames.es;
  const currentLevelDescriptions = levelDescriptions[lang] || levelDescriptions.es;

  // Detectar tamaño de pantalla
  useEffect(() => {
    const checkScreenSize = () => {
      const width = window.innerWidth;
      setIsMobile(width < 768);
      setIsTablet(width >= 768 && width < 1024);

      if (width < 768 && !forceExpanded) {
        setIsCollapsed(true);
      } else if (forceExpanded) {
        setIsCollapsed(false);
      }
    };

    checkScreenSize();
    window.addEventListener('resize', checkScreenSize);
    return () => window.removeEventListener('resize', checkScreenSize);
  }, []);

  const filteredAgents =
    activeLevel === "all"
      ? agents
      : agents.filter((a) => a.level === parseInt(activeLevel));

  const agentsByLevel = agents.reduce((acc, agent) => {
    if (!acc[agent.level]) acc[agent.level] = [];
    acc[agent.level].push(agent);
    return acc;
  }, {} as Record<number, Agent[]>);

  // State for Auth Modal
  const [isAuthModalOpen, setIsAuthModalOpen] = useState(false);
  const [isProfileModalOpen, setIsProfileModalOpen] = useState(false);
  const { user, login, logout } = useAuth();

  if (isCollapsed) {
    // ... collapsed view render
    return (
      <div className={cn(
        "h-full bg-card/50 backdrop-blur-sm border-r border-primary/20 flex flex-col items-center py-4 gap-4",
        isMobile ? "w-14" : "w-16"
      )}>
        <Button
          variant="ghost"
          size="icon"
          onClick={() => setIsCollapsed(false)}
          className="text-primary"
        >
          <ChevronRight className="h-5 w-5" />
        </Button>
        <div className="flex flex-col gap-2">
          <div className={cn(
            "rounded-lg bg-primary/20 flex items-center justify-center",
            isMobile ? "h-7 w-7" : "h-8 w-8"
          )}>
            <Cpu className={cn(
              "text-primary",
              isMobile ? "h-3 w-3" : "h-4 w-4"
            )} />
          </div>
          <Badge variant="outline" className={cn(
            "text-xs",
            isMobile && "text-[10px]"
          )}>
            {selectedAgents.length}
          </Badge>
        </div>

        {/* User Avatar in Collapsed Mode */}
        <div className="mt-auto pb-4">
          <Button
            variant="ghost"
            size="icon"
            onClick={() => user ? setIsProfileModalOpen(true) : setIsAuthModalOpen(true)}
            className="rounded-full overflow-hidden h-8 w-8 border border-primary/20"
          >
            {user ? (
              <div className="h-full w-full bg-primary/20 flex items-center justify-center font-bold text-xs text-primary">
                {user.username?.[0]?.toUpperCase() || "U"}
              </div>
            ) : (
              <User className="h-4 w-4 text-muted-foreground" />
            )}
          </Button>
        </div>
      </div>
    );
  }

  // Local state for user removed (handled by AuthContext)
  // useEffect for checking token removed (handled by AuthProvider)

  return (
    <div className={cn(
      "h-full bg-gradient-to-b from-card/80 to-card/50 backdrop-blur-md border-r border-primary/30 flex flex-col shadow-2xl overflow-hidden",
      isMobile ? "w-full" : isTablet ? "w-64" : "w-full"
    )}>
      <div className="p-4 border-b border-primary/30 bg-gradient-to-r from-primary/10 to-transparent">
        <div className="flex items-center justify-between mb-4">
          <div className="flex items-center gap-3">
            <div className="h-10 w-10 rounded-lg bg-primary/20 flex items-center justify-center">
              <Cpu className="text-primary h-5 w-5" />
            </div>
            <div>
              <h2 className="font-bold text-base text-primary uppercase tracking-tighter flex items-center gap-2">
                {lang === "es" ? "Agentes" : "Agents"}
                <div className={cn("h-2 w-2 rounded-full", isConnected ? "bg-green-500 shadow-[0_0_8px_rgba(34,197,94,0.6)]" : "bg-red-500 shadow-[0_0_8px_rgba(239,68,68,0.6)]")} />
              </h2>
              <p className="text-[10px] text-muted-foreground uppercase font-black tracking-widest">
                {lang === "es" ? "30 Especialistas" : "30 Specialists"}
              </p>
            </div>
          </div>
          <Button
            variant="ghost"
            size="icon"
            onClick={() => setIsCollapsed(true)}
            className="text-primary"
          >
            <ChevronLeft className="h-5 w-5" />
          </Button>
        </div>

        <div className="flex items-center justify-between gap-2">
          <Badge variant="success" className="font-black text-[10px] px-2 py-1 shadow-md uppercase">
            {selectedAgents.length} / 5 {lang === "es" ? "Activos" : "Active"}
          </Badge>
          <div className="flex gap-1">
            <Button
              variant="outline"
              size="sm"
              onClick={() => onSelectAll()}
              className="text-[10px] h-7 font-black uppercase border-primary/40 hover:bg-primary/20 transition-all"
            >
              <Zap className="h-3 w-3 mr-1" />
              {lang === "es" ? "Todos" : "All"}
            </Button>
            <Button
              variant="outline"
              size="sm"
              onClick={onClearAll}
              className="text-[10px] h-7 font-black uppercase border-destructive/40 hover:bg-destructive/20 transition-all"
            >
              {lang === "es" ? "Limpiar" : "Clear"}
            </Button>
          </div>
        </div>
      </div>

      <Tabs value={activeLevel} onValueChange={setActiveLevel} className="flex-1 flex flex-col overflow-hidden">
        <TabsList className="mx-4 mt-4 grid grid-cols-6 bg-muted/40 p-1 rounded-xl border border-primary/20">
          <TabsTrigger value="all" className="text-[10px] font-black uppercase data-[state=active]:bg-primary">
            {lang === "es" ? "Todos" : "All"}
          </TabsTrigger>
          {[1, 2, 3, 4, 5].map((level) => (
            <TabsTrigger
              key={level}
              value={level.toString()}
              className="text-[10px] font-black uppercase data-[state=active]:bg-primary"
            >
              L{level}
            </TabsTrigger>
          ))}
        </TabsList>

        <TabsContent value={activeLevel} className="flex-1 mt-0 overflow-hidden">
          <div className="flex-1 h-full px-3 py-4">
            <div className="h-full w-full pr-1 overflow-y-auto">
              <div className="space-y-6">
                {(activeLevel === "all"
                  ? (Object.entries(agentsByLevel) as [string, Agent[]][])
                  : [[activeLevel, filteredAgents]] as [string, Agent[]][]
                ).map(([level, levelAgents]) => (
                  <div key={level}>
                    <div className="flex items-center justify-between mb-3 p-2 rounded-lg bg-gradient-to-r from-primary/10 to-transparent border-l-4 border-primary">
                      <div>
                        <h3 className="text-[11px] font-black text-primary flex items-center gap-2 uppercase tracking-tighter">
                          {lang === "es" ? "Nivel" : "Level"} {level} - {currentLevelNames[parseInt(level)]}
                        </h3>
                        <p className="text-[10px] text-muted-foreground uppercase opacity-70">
                          {currentLevelDescriptions[parseInt(level)]}
                        </p>
                      </div>
                      <Button
                        variant="outline"
                        size="sm"
                        onClick={() => onSelectAll(parseInt(level))}
                        className="text-[9px] h-6 font-black uppercase border-primary/40"
                      >
                        <Zap className="h-2 w-2 mr-1" />
                        {lang === "es" ? "Todos" : "All"}
                      </Button>
                    </div>
                    <div className="flex flex-col gap-3">
                      {(levelAgents as Agent[]).map((agent) => (
                        <AgentCard
                          key={agent.name}
                          name={agent.displayName || agent.name}
                          role={agent.role}
                          level={agent.level}
                          isSelected={selectedAgents.includes(agent.name)}
                          onClick={() => onAgentToggle(agent.name)}
                          availableModels={availableModels}
                          selectedModel={agentModels[agent.name]}
                          onModelChange={onAgentModelChange}
                          customInstructions={agentInstructions[agent.name]}
                          onInstructionsChange={onAgentInstructionsChange}
                          onShowDetails={onShowAgentDetails}
                        />
                      ))}
                    </div>
                  </div>
                ))}
              </div>
            </div>
          </div>
        </TabsContent>
      </Tabs>

      {/* Footer / User Profile */}
      <div className="p-4 border-t border-border bg-muted/30">
        {user ? (
          <div className="flex items-center gap-3">
            <button
              className="flex items-center gap-3 flex-1 min-w-0 hover:bg-muted/50 p-1 -ml-1 rounded-lg transition-colors text-left"
              onClick={() => setIsProfileModalOpen(true)}
            >
              <div className="h-10 w-10 rounded-full bg-primary/20 flex items-center justify-center border border-primary/30">
                <span className="font-bold text-primary">{user.username ? user.username[0].toUpperCase() : "U"}</span>
              </div>
              <div className="flex-1 min-w-0">
                <p className="text-sm font-medium truncate">{user.username}</p>
                <p className="text-xs text-green-500 flex items-center gap-1">
                  <span className="block h-1.5 w-1.5 rounded-full bg-green-500" />
                  Online
                </p>
              </div>
            </button>
            <Button variant="ghost" size="icon" onClick={logout} title="Cerrar Sessión">
              <LogOut className="h-4 w-4 text-muted-foreground hover:text-destructive" />
            </Button>
          </div>
        ) : (
          <Button
            onClick={() => setIsAuthModalOpen(true)}
            className="w-full bg-primary/10 hover:bg-primary/20 text-primary border border-primary/20 shadow-sm"
          >
            <User className="h-4 w-4 mr-2" />
            Conectar Cuenta
          </Button>
        )}
      </div>

      <AuthModal
        isOpen={isAuthModalOpen}
        onClose={() => setIsAuthModalOpen(false)}
        onLoginSuccess={(userData) => {
          // Token should be handled by AuthModal saving it to localStorage, verify AuthProvider picks it up or we pass it
          // For now let's assume AuthModal doesn't pass token back, so we read it or fix AuthModal.
          // Actually AuthModal.tsx saves to localStorage 'atp_token'.
          login(localStorage.getItem("atp_token") || "", userData)
        }}
      />

      <ProfileModal
        isOpen={isProfileModalOpen}
        onClose={() => setIsProfileModalOpen(false)}
      />
    </div >
  );
}
