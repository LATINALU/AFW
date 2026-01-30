"use client";

import { useState, useEffect } from "react";
import { Button } from "@/components/ui/button";
import { Badge } from "@/components/ui/badge";
import {
  Select,
  SelectContent,
  SelectItem,
  SelectTrigger,
  SelectValue,
} from "@/components/ui/select";
import { cn } from "@/lib/utils";
import {
  Terminal,
  Settings,
  Cpu,
  Activity,
  Wifi,
  Shield,
} from "lucide-react";
import { MinimalConnectionStatus } from "./ConnectionStatus";

interface AvailableModel {
  id: string;
  name: string;
  provider: string;
}

interface HeaderProps {
  model: string;
  onModelChange: (model: string) => void;
  isConnected: boolean;
  availableModels?: AvailableModel[];
  children?: React.ReactNode;
  onSettingsClick?: () => void;
  onSidebarToggle?: () => void;
  selectedAgents?: string[];
  onAgentSelect?: (agentId: string) => void;
  onClearChat?: () => void;
  isMobile?: boolean;
  isTablet?: boolean;
  onLanguageClick?: () => void;
}

export function Header({ 
  model, 
  onModelChange, 
  isConnected, 
  availableModels = [], 
  children,
  onSettingsClick,
  onSidebarToggle,
  selectedAgents,
  onAgentSelect,
  onClearChat,
  isMobile,
  isTablet,
  onLanguageClick
}: HeaderProps) {
  const [mounted, setMounted] = useState(false);

  useEffect(() => {
    setMounted(true);
  }, []);

  return (
    <header className="h-16 border-b border-primary/20 bg-card/50 backdrop-blur-sm px-4 py-2 flex items-center justify-between gap-2 overflow-hidden">
      {/* Logo & Platform Info */}
      <div className="flex items-center gap-3">
        <div className="relative shrink-0">
          <div className="h-10 w-10 md:h-12 md:w-12 rounded-xl bg-gradient-to-br from-primary/30 to-cyber-blue/30 border border-primary/50 flex items-center justify-center">
            <Terminal className="h-5 w-5 md:h-6 md:w-6 text-primary" />
          </div>
          <div className="absolute -bottom-0.5 -right-0.5 h-3 w-3 rounded-full bg-green-500 border-2 border-background" />
        </div>
        <div className="hidden sm:block">
          <h1 className="text-lg font-black tracking-tight leading-none">
            <span className="text-primary glow-text-subtle">ATP PLATFORM</span>
          </h1>
          <div className="flex items-center gap-2 mt-1">
            <Badge variant="outline" className="text-[10px] font-bold px-1.5 py-0 border-primary/30">v0.8.2</Badge>
            <span className="text-[10px] text-muted-foreground uppercase font-black">Enterprise</span>
          </div>
        </div>
      </div>

      {/* Model Selection - Compact on Mobile */}
      <div className="flex items-center gap-2 flex-1 md:flex-initial justify-center">
        <Select value={model || ""} onValueChange={onModelChange}>
          <SelectTrigger className="w-full max-w-[140px] md:max-w-[240px] h-9 bg-muted/30 border-primary/20 text-xs font-bold">
            <div className="flex items-center gap-2 truncate">
              <Cpu size={14} className="text-primary shrink-0" />
              <SelectValue placeholder="Configura API" />
            </div>
          </SelectTrigger>
          <SelectContent>
            {availableModels.length > 0 ? (
              availableModels.map((m) => (
                <SelectItem key={m.id} value={m.id}>
                  <div className="flex items-center gap-2">
                    <span className="text-xs">{m.name?.split("/")?.pop() || m.name}</span>
                    <Badge variant="outline" className="scale-75 origin-left">{m.provider}</Badge>
                  </div>
                </SelectItem>
              ))
            ) : (
              <SelectItem value="none" disabled>Requiere API Key</SelectItem>
            )}
          </SelectContent>
        </Select>

        <div className="hidden md:flex items-center gap-2 px-3 py-1.5 rounded-lg bg-muted/50 border border-primary/10">
          <Activity className={cn("h-4 w-4", availableModels.length > 0 ? "text-green-500" : "text-yellow-500")} />
          <span className="text-[10px] font-mono font-bold uppercase">
            {availableModels.length > 0 ? `${availableModels.length} Modelos` : "Sin Conexión"}
          </span>
        </div>
      </div>

      {/* Right Actions */}
      <div className="flex items-center gap-2 shrink-0">
        {/* Settings Button */}
        {onSettingsClick && (
          <Button
            variant="ghost"
            size="icon"
            onClick={onSettingsClick}
            className="text-muted-foreground hover:text-primary"
          >
            <Settings className="h-4 w-4" />
          </Button>
        )}
        
        {/* Sidebar Toggle for Mobile */}
        {onSidebarToggle && isMobile && (
          <Button
            variant="ghost"
            size="icon"
            onClick={onSidebarToggle}
            className="text-muted-foreground hover:text-primary"
          >
            <svg className="h-4 w-4" fill="none" stroke="currentColor" viewBox="0 0 24 24">
              <path strokeLinecap="round" strokeLinejoin="round" strokeWidth={2} d="M4 6h16M4 12h16M4 18h16" />
            </svg>
          </Button>
        )}
        
        {children}
      </div>
    </header>
  );
}
