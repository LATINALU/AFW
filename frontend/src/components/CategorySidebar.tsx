"use client";

import { useState, useEffect } from "react";
import { ScrollArea } from "@/components/ui/scroll-area";
import { Button } from "@/components/ui/button";
import { Badge } from "@/components/ui/badge";
import { Input } from "@/components/ui/input";
import {
  Collapsible,
  CollapsibleContent,
  CollapsibleTrigger,
} from "@/components/ui/collapsible";
import { cn } from "@/lib/utils";
import {
  ChevronLeft,
  ChevronRight,
  ChevronDown,
  Search,
  Sparkles,
  User,
  X,
  Check,
} from "lucide-react";
import { getCurrentLanguage } from "@/lib/i18n";
import { AuthModal } from "@/components/AuthModal";
import { ProfileModal } from "@/components/ProfileModal";
import { useAuth } from "@/components/AuthProvider";
import { Agent, Category, getCategories, getAgents } from "@/lib/api";

interface CategorySidebarProps {
  selectedAgents: string[];
  onAgentToggle: (agentId: string) => void;
  onSelectCategory: (categoryId: string) => void;
  onClearAll: () => void;
  isConnected?: boolean;
  forceExpanded?: boolean;
}

// Colores por categoría
const categoryColors: Record<string, string> = {
  software_development: "from-blue-500/20 to-blue-600/10 border-blue-500/30",
  marketing: "from-pink-500/20 to-pink-600/10 border-pink-500/30",
  finance: "from-emerald-500/20 to-emerald-600/10 border-emerald-500/30",
  legal: "from-violet-500/20 to-violet-600/10 border-violet-500/30",
  human_resources: "from-amber-500/20 to-amber-600/10 border-amber-500/30",
  sales: "from-red-500/20 to-red-600/10 border-red-500/30",
  operations: "from-gray-500/20 to-gray-600/10 border-gray-500/30",
  education: "from-teal-500/20 to-teal-600/10 border-teal-500/30",
  creative: "from-fuchsia-500/20 to-fuchsia-600/10 border-fuchsia-500/30",
  project_management: "from-cyan-500/20 to-cyan-600/10 border-cyan-500/30",
  mercadolibre: "from-yellow-500/20 to-yellow-600/10 border-yellow-500/30",
  youtube: "from-red-600/20 to-red-700/10 border-red-600/30",
};

export function CategorySidebar({
  selectedAgents,
  onAgentToggle,
  onSelectCategory,
  onClearAll,
  isConnected,
  forceExpanded = false,
}: CategorySidebarProps) {
  const [isCollapsed, setIsCollapsed] = useState(false);
  const [categories, setCategories] = useState<Category[]>([]);
  const [agents, setAgents] = useState<Agent[]>([]);
  const [expandedCategories, setExpandedCategories] = useState<string[]>([]);
  const [searchTerm, setSearchTerm] = useState("");
  const [isLoading, setIsLoading] = useState(true);
  const [isMobile, setIsMobile] = useState(false);

  const lang = getCurrentLanguage();
  const { user } = useAuth();
  const [isAuthModalOpen, setIsAuthModalOpen] = useState(false);
  const [isProfileModalOpen, setIsProfileModalOpen] = useState(false);

  // Cargar categorías y agentes
  useEffect(() => {
    const loadData = async () => {
      try {
        setIsLoading(true);
        const [categoriesRes, agentsRes] = await Promise.all([
          getCategories(),
          getAgents(),
        ]);
        setCategories(categoriesRes.categories);
        setAgents(agentsRes.agents);
      } catch (error) {
        console.error("Error loading agents:", error);
      } finally {
        setIsLoading(false);
      }
    };
    loadData();
  }, []);

  // Detectar tamaño de pantalla
  useEffect(() => {
    const checkScreenSize = () => {
      const width = window.innerWidth;
      setIsMobile(width < 768);
      if (width < 768 && !forceExpanded) {
        setIsCollapsed(true);
      } else if (forceExpanded) {
        setIsCollapsed(false);
      }
    };
    checkScreenSize();
    window.addEventListener("resize", checkScreenSize);
    return () => window.removeEventListener("resize", checkScreenSize);
  }, [forceExpanded]);

  // Filtrar agentes por búsqueda
  const filteredAgents = searchTerm
    ? agents.filter(
        (a) =>
          a.name.toLowerCase().includes(searchTerm.toLowerCase()) ||
          a.description.toLowerCase().includes(searchTerm.toLowerCase()) ||
          a.specialization.toLowerCase().includes(searchTerm.toLowerCase())
      )
    : agents;

  // Agrupar agentes por categoría
  const agentsByCategory = filteredAgents.reduce((acc, agent) => {
    if (!acc[agent.category]) acc[agent.category] = [];
    acc[agent.category].push(agent);
    return acc;
  }, {} as Record<string, Agent[]>);

  const toggleCategory = (categoryId: string) => {
    setExpandedCategories((prev) =>
      prev.includes(categoryId)
        ? prev.filter((c) => c !== categoryId)
        : [...prev, categoryId]
    );
  };

  const selectAllInCategory = (categoryId: string) => {
    onSelectCategory(categoryId);
  };

  // Vista colapsada
  if (isCollapsed) {
    return (
      <div
        className={cn(
          "h-full bg-card/50 backdrop-blur-sm border-r border-primary/20 flex flex-col items-center py-4 gap-4",
          isMobile ? "w-14" : "w-16"
        )}
      >
        <Button
          variant="ghost"
          size="icon"
          onClick={() => setIsCollapsed(false)}
          className="text-primary"
        >
          <ChevronRight className="h-5 w-5" />
        </Button>
        <div className="flex flex-col gap-2 items-center">
          <div className="h-8 w-8 rounded-lg bg-primary/20 flex items-center justify-center">
            <Sparkles className="text-primary h-4 w-4" />
          </div>
          <Badge variant="outline" className="text-xs">
            {selectedAgents.length}
          </Badge>
        </div>
        <div className="mt-auto pb-4">
          <Button
            variant="ghost"
            size="icon"
            onClick={() =>
              user ? setIsProfileModalOpen(true) : setIsAuthModalOpen(true)
            }
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
        <AuthModal
          isOpen={isAuthModalOpen}
          onClose={() => setIsAuthModalOpen(false)}
          onLoginSuccess={() => console.log('Login successful')}
        />
        <ProfileModal
          isOpen={isProfileModalOpen}
          onClose={() => setIsProfileModalOpen(false)}
        />
      </div>
    );
  }

  return (
    <div
      className={cn(
        "h-full bg-gradient-to-b from-card/80 to-card/50 backdrop-blur-md border-r border-primary/30 flex flex-col shadow-2xl overflow-hidden",
        isMobile ? "w-full" : "w-80"
      )}
    >
      {/* Header */}
      <div className="p-4 border-b border-primary/30 bg-gradient-to-r from-primary/10 to-transparent">
        <div className="flex items-center justify-between mb-3">
          <div className="flex items-center gap-3">
            <div className="h-10 w-10 rounded-xl bg-gradient-to-br from-primary/30 to-primary/10 flex items-center justify-center shadow-lg">
              <Sparkles className="text-primary h-5 w-5" />
            </div>
            <div>
              <h2 className="font-black text-base text-primary uppercase tracking-tight flex items-center gap-2">
                AFW Agents
                <div
                  className={cn(
                    "h-2 w-2 rounded-full",
                    isConnected
                      ? "bg-green-500 shadow-[0_0_8px_rgba(34,197,94,0.6)]"
                      : "bg-red-500 shadow-[0_0_8px_rgba(239,68,68,0.6)]"
                  )}
                />
              </h2>
              <p className="text-[10px] text-muted-foreground font-bold tracking-wider">
                120 {lang === "es" ? "AGENTES" : "AGENTS"} • 12{" "}
                {lang === "es" ? "CATEGORÍAS" : "CATEGORIES"}
              </p>
            </div>
          </div>
          <Button
            variant="ghost"
            size="icon"
            onClick={() => setIsCollapsed(true)}
            className="text-primary hover:bg-primary/10"
          >
            <ChevronLeft className="h-5 w-5" />
          </Button>
        </div>

        {/* Stats */}
        <div className="flex items-center justify-between gap-2 mb-3">
          <Badge
            variant="outline"
            className="font-black text-[10px] px-3 py-1 bg-primary/10 border-primary/30"
          >
            {selectedAgents.length}{" "}
            {lang === "es" ? "SELECCIONADOS" : "SELECTED"}
          </Badge>
          {selectedAgents.length > 0 && (
            <Button
              variant="ghost"
              size="sm"
              onClick={onClearAll}
              className="text-[10px] h-6 text-muted-foreground hover:text-destructive"
            >
              <X className="h-3 w-3 mr-1" />
              {lang === "es" ? "Limpiar" : "Clear"}
            </Button>
          )}
        </div>

        {/* Search */}
        <div className="relative">
          <Search className="absolute left-3 top-1/2 -translate-y-1/2 h-4 w-4 text-muted-foreground" />
          <Input
            placeholder={
              lang === "es" ? "Buscar agentes..." : "Search agents..."
            }
            value={searchTerm}
            onChange={(e) => setSearchTerm(e.target.value)}
            className="pl-9 h-9 bg-background/50 border-primary/20 focus:border-primary/50 text-sm"
          />
          {searchTerm && (
            <Button
              variant="ghost"
              size="icon"
              className="absolute right-1 top-1/2 -translate-y-1/2 h-6 w-6"
              onClick={() => setSearchTerm("")}
            >
              <X className="h-3 w-3" />
            </Button>
          )}
        </div>
      </div>

      {/* Categories List */}
      <ScrollArea className="flex-1">
        <div className="p-2 space-y-2">
          {isLoading ? (
            <div className="flex items-center justify-center py-8">
              <div className="animate-spin h-6 w-6 border-2 border-primary border-t-transparent rounded-full" />
            </div>
          ) : (
            categories.map((category) => {
              const categoryAgents = agentsByCategory[category.id] || [];
              const selectedInCategory = categoryAgents.filter((a) =>
                selectedAgents.includes(a.id)
              ).length;
              const isExpanded = expandedCategories.includes(category.id);
              const colorClass =
                categoryColors[category.id] || categoryColors.software_development;

              return (
                <Collapsible
                  key={category.id}
                  open={isExpanded}
                  onOpenChange={() => toggleCategory(category.id)}
                >
                  <div
                    className={cn(
                      "rounded-xl border bg-gradient-to-r transition-all duration-200",
                      colorClass,
                      isExpanded && "shadow-lg"
                    )}
                  >
                    <CollapsibleTrigger asChild>
                      <button className="w-full p-3 flex items-center justify-between hover:bg-white/5 rounded-t-xl transition-colors">
                        <div className="flex items-center gap-3">
                          <span className="text-xl">{category.emoji}</span>
                          <div className="text-left">
                            <p className="font-bold text-sm">{category.name}</p>
                            <p className="text-[10px] text-muted-foreground">
                              {categoryAgents.length} agentes
                            </p>
                          </div>
                        </div>
                        <div className="flex items-center gap-2">
                          {selectedInCategory > 0 && (
                            <Badge
                              variant="secondary"
                              className="text-[10px] bg-primary/20"
                            >
                              {selectedInCategory}
                            </Badge>
                          )}
                          <ChevronDown
                            className={cn(
                              "h-4 w-4 transition-transform duration-200",
                              isExpanded && "rotate-180"
                            )}
                          />
                        </div>
                      </button>
                    </CollapsibleTrigger>

                    <CollapsibleContent>
                      <div className="px-2 pb-2 space-y-1">
                        {/* Select all button */}
                        <Button
                          variant="ghost"
                          size="sm"
                          className="w-full justify-start text-xs h-7 text-muted-foreground hover:text-primary"
                          onClick={() => selectAllInCategory(category.id)}
                        >
                          <Check className="h-3 w-3 mr-2" />
                          {lang === "es"
                            ? "Seleccionar todos"
                            : "Select all"}
                        </Button>

                        {/* Agents list */}
                        {categoryAgents.map((agent) => {
                          const isSelected = selectedAgents.includes(agent.id);
                          return (
                            <button
                              key={agent.id}
                              onClick={() => onAgentToggle(agent.id)}
                              className={cn(
                                "w-full p-2 rounded-lg flex items-center gap-2 transition-all text-left",
                                isSelected
                                  ? "bg-primary/20 border border-primary/40"
                                  : "hover:bg-white/5 border border-transparent"
                              )}
                            >
                              <span className="text-sm">{agent.emoji}</span>
                              <div className="flex-1 min-w-0">
                                <p
                                  className={cn(
                                    "text-xs font-semibold truncate",
                                    isSelected && "text-primary"
                                  )}
                                >
                                  {agent.name}
                                </p>
                                <p className="text-[10px] text-muted-foreground truncate">
                                  {agent.specialization}
                                </p>
                              </div>
                              {isSelected && (
                                <Check className="h-3 w-3 text-primary flex-shrink-0" />
                              )}
                            </button>
                          );
                        })}
                      </div>
                    </CollapsibleContent>
                  </div>
                </Collapsible>
              );
            })
          )}
        </div>
      </ScrollArea>

      {/* Footer */}
      <div className="p-3 border-t border-primary/20 bg-card/50">
        <Button
          variant="ghost"
          className="w-full justify-start gap-2"
          onClick={() =>
            user ? setIsProfileModalOpen(true) : setIsAuthModalOpen(true)
          }
        >
          <div className="h-8 w-8 rounded-full bg-primary/20 flex items-center justify-center">
            {user ? (
              <span className="font-bold text-xs text-primary">
                {user.username?.[0]?.toUpperCase() || "U"}
              </span>
            ) : (
              <User className="h-4 w-4 text-muted-foreground" />
            )}
          </div>
          <div className="text-left">
            <p className="text-xs font-semibold">
              {user?.username || (lang === "es" ? "Iniciar sesión" : "Sign in")}
            </p>
            <p className="text-[10px] text-muted-foreground">
              {user
                ? lang === "es"
                  ? "Ver perfil"
                  : "View profile"
                : lang === "es"
                ? "Acceder a tu cuenta"
                : "Access your account"}
            </p>
          </div>
        </Button>
      </div>

      <AuthModal
        isOpen={isAuthModalOpen}
        onClose={() => setIsAuthModalOpen(false)}
      />
      <ProfileModal
        isOpen={isProfileModalOpen}
        onClose={() => setIsProfileModalOpen(false)}
      />
    </div>
  );
}
