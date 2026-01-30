"use client";

import { useState, useEffect } from "react";
import { Header } from "@/components/Header";
import { Sidebar } from "@/components/Sidebar";
import { StreamingChatV2 } from "@/components/StreamingChatV2";
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

export default function HomePage() {
  const [isSidebarOpen, setIsSidebarOpen] = useState(false);
  const [selectedAgents, setSelectedAgents] = useState<string[]>(["reasoning", "synthesis"]);
  const [isMobile, setIsMobile] = useState(false);

  useEffect(() => {
    const checkMobile = () => {
      setIsMobile(window.innerWidth < 768);
    };
    checkMobile();
    window.addEventListener('resize', checkMobile);
    return () => window.removeEventListener('resize', checkMobile);
  }, []);

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
    <div className="min-h-screen bg-background text-foreground flex flex-col">
      {/* Main Content */}
      <div className="flex flex-1 h-screen overflow-hidden">
        {/* Sidebar - Desktop always visible, Mobile overlay */}
        {(!isMobile || isSidebarOpen) && (
          <div className={cn(
            "transition-all duration-300 ease-in-out",
            isMobile && "fixed inset-0 z-50 bg-black/50"
          )}>
            {isMobile && (
              <div 
                className="absolute inset-0" 
                onClick={() => setIsSidebarOpen(false)}
              />
            )}
            <div className={cn(
              "h-full bg-background",
              isMobile ? "absolute left-0 top-0 w-[85%] max-w-sm shadow-2xl" : "w-80 border-r"
            )}>
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
              />
            </div>
          </div>
        )}

        {/* Chat Area */}
        <main className="flex-1 flex flex-col overflow-hidden">
          <div className="h-full w-full">
            <StreamingChatV2
              selectedAgents={selectedAgents}
              model="groq-default"
              apiConfig={null}
              onAgentModelChange={() => { }}
              agentInstructions={{}}
              onAgentInstructionsChange={() => { }}
              onShowAgentDetails={() => { }}
              onConnectionChange={() => { }}
              onSelectPreset={() => { }}
            />
          </div>
        </main>
      </div>

      {/* Mobile Menu Toggle */}
      {isMobile && !isSidebarOpen && (
        <button
          onClick={() => setIsSidebarOpen(true)}
          className="fixed bottom-6 right-6 z-40 bg-primary text-primary-foreground rounded-full p-4 shadow-lg hover:bg-primary/90 transition-colors"
        >
          <svg className="h-6 w-6" fill="none" stroke="currentColor" viewBox="0 0 24 24">
            <path strokeLinecap="round" strokeLinejoin="round" strokeWidth={2} d="M4 6h16M4 12h16M4 18h16" />
          </svg>
        </button>
      )}
    </div>
  );
}
