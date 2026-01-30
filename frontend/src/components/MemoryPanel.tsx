"use client";

import { useState, useEffect, useMemo } from "react";
import {
  Brain,
  Trash2,
  Save,
  Search,
  Clock,
  MessageSquare,
  Users,
  Star,
  Filter,
  Sparkles,
} from "lucide-react";
import { Message } from "@/types";

interface MemoryEntry {
  id: string;
  timestamp: Date;
  messages: Message[];
  agents: string[];
  summary: string;
  tags: string[];
  favorite?: boolean;
}

interface MemoryPanelProps {
  messages: Message[];
  currentAgents: string[];
  onSaveMemory?: (entry: MemoryEntry) => void;
  onLoadMemory?: (entry: MemoryEntry) => void;
}

export function MemoryPanel({ messages, currentAgents, onSaveMemory, onLoadMemory }: MemoryPanelProps) {
  const [memories, setMemories] = useState<MemoryEntry[]>([]);
  const [searchTerm, setSearchTerm] = useState("");
  const [isExpanded, setIsExpanded] = useState(false);
  const [summary, setSummary] = useState("");
  const [tags, setTags] = useState("");
  const [viewFilter, setViewFilter] = useState<"all" | "favorites" | "recent">("all");

  // Load memories from localStorage
  useEffect(() => {
    const saved = localStorage.getItem("atp-memories");
    if (saved) {
      try {
        const parsedMemories = JSON.parse(saved).map((m: any) => ({
          ...m,
          timestamp: new Date(m.timestamp),
          favorite: Boolean(m.favorite),
        }));
        setMemories(parsedMemories);
      } catch (e) {
        console.error("Error loading memories:", e);
      }
    }
  }, []);

  // Save memories to localStorage
  useEffect(() => {
    localStorage.setItem("atp-memories", JSON.stringify(memories));
  }, [memories]);

  const handleSaveMemory = () => {
    if (messages.length === 0) return;

    const newMemory: MemoryEntry = {
      id: Date.now().toString(),
      timestamp: new Date(),
      messages: [...messages],
      agents: [...currentAgents],
      summary: summary || generateAutoSummary(),
      tags: tags ? tags.split(",").map(t => t.trim()).filter(t => t) : generateAutoTags(),
      favorite: false,
    };

    const updatedMemories = [newMemory, ...memories];
    setMemories(updatedMemories);
    setSummary("");
    setTags("");
    
    if (onSaveMemory) {
      onSaveMemory(newMemory);
    }
  };

  const handleDeleteMemory = (id: string) => {
    setMemories(prev => prev.filter(m => m.id !== id));
  };

  const toggleFavorite = (id: string) => {
    setMemories(prev =>
      prev.map(memory =>
        memory.id === id ? { ...memory, favorite: !memory.favorite } : memory
      )
    );
  };

  const handleLoadMemory = (memory: MemoryEntry) => {
    if (onLoadMemory) {
      onLoadMemory(memory);
    }
  };

  const generateAutoSummary = (): string => {
    if (messages.length === 0) return "";
    const userMessage = messages.find(m => m.role === "user");
    return userMessage ? userMessage.content.substring(0, 100) + "..." : "Conversación sin título";
  };

  const generateAutoTags = (): string[] => {
    const tags = new Set<string>();
    currentAgents.forEach(agent => {
      tags.add(agent.replace("_agent", ""));
    });
    if (messages.some(m => m.content.toLowerCase().includes("codigo"))) tags.add("programación");
    if (messages.some(m => m.content.toLowerCase().includes("análisis"))) tags.add("análisis");
    if (messages.some(m => m.content.toLowerCase().includes("plan"))) tags.add("planificación");
    return Array.from(tags);
  };

  const recentThreshold = useMemo(() => Date.now() - 1000 * 60 * 60 * 24, []);

  const filteredMemories = memories
    .filter(memory => {
      if (!searchTerm) return true;
      const term = searchTerm.toLowerCase();
      return (
        memory.summary.toLowerCase().includes(term) ||
        memory.tags.some(tag => tag.toLowerCase().includes(term))
      );
    })
    .filter(memory => {
      if (viewFilter === "favorites") {
        return Boolean(memory.favorite);
      }
      if (viewFilter === "recent") {
        return memory.timestamp.getTime() >= recentThreshold;
      }
      return true;
    });

  const totalMemories = memories.length;
  const favoriteCount = memories.filter(m => m.favorite).length;
  const lastMemory = memories[0];
  const currentAgentSnapshot = useMemo(
    () =>
      currentAgents.slice(0, 6).map(agent =>
        agent.replace(/_/g, " ").replace(/\b\w/g, letter => letter.toUpperCase())
      ),
    [currentAgents]
  );

  return (
    <div
      className={`bg-card border-l border-border transition-all duration-300 ${
        isExpanded ? "w-96" : "w-12"
      }`}
    >
      {/* Toggle Button */}
      <button
        onClick={() => setIsExpanded(!isExpanded)}
        className="w-full p-3 hover:bg-muted transition-colors border-b border-border"
        title="Panel de Memoria"
      >
        <Brain className={`h-5 w-5 text-primary transition-transform ${isExpanded ? "rotate-180" : ""}`} />
      </button>

      {isExpanded && (
        <div className="p-4 h-full overflow-y-auto space-y-4">
          <div className="flex items-center justify-between">
            <h3 className="text-lg font-semibold flex items-center gap-2">
              <Brain className="h-5 w-5 text-primary" />
              Memoria Conversacional
            </h3>
            <span className="text-xs uppercase tracking-wide text-muted-foreground">
              {totalMemories} memorias
            </span>
          </div>

          {/* Stats */}
          <div className="grid grid-cols-2 gap-2">
            <div className="p-3 rounded-xl border border-primary/20 bg-primary/5">
              <p className="text-[11px] uppercase text-muted-foreground">Favoritas</p>
              <p className="text-xl font-semibold text-primary">{favoriteCount}</p>
              <p className="text-[11px] text-muted-foreground mt-1">de {totalMemories}</p>
            </div>
            <div className="p-3 rounded-xl border border-border">
              <p className="text-[11px] uppercase text-muted-foreground">Última memoria</p>
              {lastMemory ? (
                <p className="text-sm font-medium line-clamp-2">{lastMemory.summary}</p>
              ) : (
                <p className="text-sm text-muted-foreground">Sin registros</p>
              )}
            </div>
          </div>

          {/* Current conversation snapshot */}
          {messages.length > 0 && (
            <div className="rounded-xl border border-border/80 bg-muted/60 p-3 space-y-2">
              <div className="flex items-center gap-2 text-xs font-semibold text-muted-foreground uppercase">
                <Sparkles className="h-3 w-3" />
                Conversación en curso
              </div>
              <p className="text-sm text-muted-foreground line-clamp-2">
                {summary || generateAutoSummary()}
              </p>
              {currentAgentSnapshot.length > 0 && (
                <div className="flex flex-wrap gap-1">
                  {currentAgentSnapshot.map((agent, idx) => (
                    <span
                      key={`${agent}-${idx}`}
                      className="px-2 py-0.5 rounded-full bg-primary/10 text-primary text-[11px]"
                    >
                      {agent}
                    </span>
                  ))}
                </div>
              )}
            </div>
          )}

          {/* Save Current Memory */}
          {messages.length > 0 && (
            <div className="p-3 bg-background/80 rounded-xl border border-border/80 space-y-2">
              <h4 className="font-semibold text-sm flex items-center gap-2">
                <Save className="h-4 w-4 text-primary" />
                Guardar Conversación
              </h4>
              <input
                type="text"
                placeholder="Resumen (opcional)"
                value={summary}
                onChange={(e) => setSummary(e.target.value)}
                className="w-full p-2 text-sm bg-card border border-border rounded"
              />
              <input
                type="text"
                placeholder="Tags (separados por comas)"
                value={tags}
                onChange={(e) => setTags(e.target.value)}
                className="w-full p-2 text-sm bg-card border border-border rounded"
              />
              <button
                onClick={handleSaveMemory}
                className="w-full p-2 bg-primary text-primary-foreground rounded-lg hover:bg-primary/90 transition-colors flex items-center justify-center gap-2 text-sm font-medium"
              >
                <Save className="h-4 w-4" />
                Guardar memoria
              </button>
            </div>
          )}

          {/* Search */}
          <div className="space-y-3">
            <div className="relative">
              <Search className="absolute left-3 top-1/2 transform -translate-y-1/2 h-4 w-4 text-muted-foreground" />
              <input
                type="text"
                placeholder="Buscar memorias por resumen o tag..."
                value={searchTerm}
                onChange={(e) => setSearchTerm(e.target.value)}
                className="w-full p-2 pl-10 bg-background border border-border rounded-lg text-sm"
              />
            </div>
            <div className="flex items-center gap-2">
              {(
                [
                  { key: "all", label: "Todas" },
                  { key: "recent", label: "Últimas 24h" },
                  { key: "favorites", label: "Favoritas" },
                ] as const
              ).map(filter => (
                <button
                  key={filter.key}
                  onClick={() => setViewFilter(filter.key)}
                  className={`flex-1 flex items-center justify-center gap-1 text-xs rounded-full border px-2 py-1 transition-colors ${
                    viewFilter === filter.key
                      ? "bg-primary text-primary-foreground border-primary"
                      : "border-border text-muted-foreground hover:bg-muted"
                  }`}
                >
                  <Filter className="h-3 w-3" />
                  {filter.label}
                </button>
              ))}
            </div>
          </div>

          {/* Memories List */}
          <div className="space-y-3">
            {filteredMemories.map((memory) => (
              <div
                key={memory.id}
                className="p-3 bg-muted rounded-lg hover:bg-muted/80 transition-colors border border-border/60"
              >
                <div className="flex justify-between items-start mb-2">
                  <div className="flex-1">
                    <h5 className="font-medium text-sm truncate">{memory.summary}</h5>
                    <div className="flex items-center gap-2 text-xs text-muted-foreground mt-1">
                      <Clock className="h-3 w-3" />
                      {memory.timestamp.toLocaleDateString()}
                    </div>
                  </div>
                  <div className="flex gap-1">
                    <button
                      onClick={() => toggleFavorite(memory.id)}
                      className={`p-1 rounded transition-colors ${
                        memory.favorite
                          ? "bg-amber-500/20 text-amber-400"
                          : "hover:bg-background text-muted-foreground"
                      }`}
                      title={memory.favorite ? "Quitar de favoritos" : "Marcar como favorita"}
                    >
                      <Star className={`h-3.5 w-3.5 ${memory.favorite ? "fill-current" : ""}`} />
                    </button>
                    <button
                      onClick={() => handleLoadMemory(memory)}
                      className="p-1 hover:bg-background rounded transition-colors text-muted-foreground"
                      title="Cargar memoria"
                    >
                      <MessageSquare className="h-3 w-3" />
                    </button>
                    <button
                      onClick={() => handleDeleteMemory(memory.id)}
                      className="p-1 hover:bg-background rounded transition-colors text-muted-foreground"
                      title="Eliminar memoria"
                    >
                      <Trash2 className="h-3 w-3" />
                    </button>
                  </div>
                </div>
                
                <div className="flex items-center gap-2 text-xs text-muted-foreground mb-2">
                  <Users className="h-3 w-3" />
                  {memory.agents.length} agentes
                </div>

                {memory.tags.length > 0 && (
                  <div className="flex flex-wrap gap-1">
                    {memory.tags.map((tag, index) => (
                      <span
                        key={index}
                        className="px-2 py-1 bg-primary/10 text-primary text-[11px] rounded-full"
                      >
                        {tag}
                      </span>
                    ))}
                  </div>
                )}
              </div>
            ))}
          </div>

          {filteredMemories.length === 0 && (
            <div className="text-center text-muted-foreground py-8">
              <Brain className="h-12 w-12 mx-auto mb-2 opacity-50" />
              <p className="text-sm">No hay memorias guardadas</p>
            </div>
          )}
        </div>
      )}
    </div>
  );
}
