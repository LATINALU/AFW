"use client";

import { useState } from "react";
import { ScrollArea } from "@/components/ui/scroll-area";
import { Button } from "@/components/ui/button";
import {
    MessageSquare,
    Trash2,
    Clock,
    Plus,
    Search,
    ChevronLeft,
    ChevronRight,
    MoreVertical,
    Edit2
} from "lucide-react";
import { cn } from "@/lib/utils";
import { Conversation } from "@/lib/userStorage";
import {
    DropdownMenu,
    DropdownMenuContent,
    DropdownMenuItem,
    DropdownMenuTrigger
} from "@/components/ui/dropdown-menu";

interface HistorySidebarProps {
    history: Conversation[];
    activeId?: string;
    onSelect: (id: string) => void;
    onDelete: (id: string) => void;
    onNewChat: () => void;
    onUpdateTitle: (id: string, title: string) => void;
    isLoading?: boolean;
}

export function HistorySidebar({
    history,
    activeId,
    onSelect,
    onDelete,
    onNewChat,
    onUpdateTitle,
    isLoading
}: HistorySidebarProps) {
    const [isCollapsed, setIsCollapsed] = useState(false);
    const [searchQuery, setSearchQuery] = useState("");

    const filteredHistory = history.filter(item =>
        item.title.toLowerCase().includes(searchQuery.toLowerCase()) ||
        item.model.toLowerCase().includes(searchQuery.toLowerCase())
    );

    if (isCollapsed) {
        return (
            <div className="h-full bg-card/60 backdrop-blur-md border-r border-primary/20 flex flex-col items-center py-4 gap-4 w-16 transition-all duration-300 ease-in-out">
                <Button variant="ghost" size="icon" onClick={() => setIsCollapsed(false)} className="text-primary hover:bg-primary/20">
                    <ChevronRight className="h-5 w-5" />
                </Button>
                <Button variant="outline" size="icon" onClick={onNewChat} className="rounded-full border-primary/40 hover:bg-primary/20">
                    <Plus className="h-5 w-5 text-primary" />
                </Button>
                <div className="flex-1 overflow-hidden flex flex-col items-center gap-3">
                    {history.slice(0, 5).map(item => (
                        <Button
                            key={item.id}
                            variant="ghost"
                            size="icon"
                            onClick={() => onSelect(item.id)}
                            className={cn(
                                "rounded-lg transition-all",
                                activeId === item.id ? "bg-primary/30 text-primary shadow-lg" : "text-muted-foreground hover:bg-primary/10"
                            )}
                        >
                            <MessageSquare className="h-5 w-5" />
                        </Button>
                    ))}
                </div>
            </div>
        );
    }

    return (
        <div className="h-full bg-gradient-to-b from-card/80 to-card/40 backdrop-blur-xl border-r border-primary/20 flex flex-col w-72 shadow-2xl transition-all duration-300 ease-in-out overflow-hidden">
            {/* Header */}
            <div className="p-4 border-b border-primary/10 bg-primary/5">
                <div className="flex items-center justify-between mb-4">
                    <div className="flex items-center gap-2">
                        <div className="h-8 w-8 rounded-lg bg-primary/20 flex items-center justify-center">
                            <Clock className="h-4 w-4 text-primary" />
                        </div>
                        <h2 className="font-bold text-sm text-primary uppercase tracking-wider">Historial</h2>
                    </div>
                    <Button variant="ghost" size="icon" onClick={() => setIsCollapsed(true)} className="text-muted-foreground hover:text-primary transition-colors">
                        <ChevronLeft className="h-5 w-5" />
                    </Button>
                </div>

                <Button
                    onClick={onNewChat}
                    className="w-full bg-primary hover:bg-primary/90 text-primary-foreground font-bold shadow-lg shadow-primary/20 transition-all active:scale-95 flex items-center gap-2 py-5 rounded-xl"
                >
                    <Plus className="h-4 w-4" />
                    Nuevo Chat
                </Button>
            </div>

            {/* Search */}
            <div className="px-4 py-3">
                <div className="relative group">
                    <Search className="absolute left-3 top-1/2 -translate-y-1/2 h-3.5 w-3.5 text-muted-foreground group-focus-within:text-primary transition-colors" />
                    <input
                        type="text"
                        placeholder="Buscar conversaciones..."
                        value={searchQuery}
                        onChange={(e) => setSearchQuery(e.target.value)}
                        className="w-full bg-muted/30 border border-primary/10 hover:border-primary/30 focus:border-primary/50 focus:ring-1 focus:ring-primary/20 rounded-lg pl-9 pr-3 py-2 text-xs transition-all outline-none"
                    />
                </div>
            </div>

            {/* List */}
            <ScrollArea className="flex-1 px-2 pb-4">
                <div className="space-y-1 py-2">
                    {isLoading && (
                        <div className="flex flex-col items-center justify-center py-20 gap-4">
                            <div className="h-8 w-8 border-2 border-primary border-t-transparent rounded-full animate-spin" />
                            <p className="text-xs text-muted-foreground animate-pulse">Cargando...</p>
                        </div>
                    )}

                    {!isLoading && filteredHistory.length === 0 && (
                        <div className="text-center py-20 px-4">
                            <MessageSquare className="h-10 w-10 text-muted-foreground/30 mx-auto mb-3" />
                            <p className="text-xs text-muted-foreground">No tienes conversaciones {searchQuery ? "que coincidan" : "aún"}.</p>
                        </div>
                    )}

                    {filteredHistory.map((item) => (
                        <div
                            key={item.id}
                            className={cn(
                                "group relative flex items-center gap-2 p-3 rounded-xl cursor-pointer select-none transition-all duration-200 border border-transparent",
                                activeId === item.id
                                    ? "bg-primary/15 border-primary/20 text-primary shadow-inner"
                                    : "hover:bg-muted/50 text-muted-foreground"
                            )}
                            onClick={() => onSelect(item.id)}
                        >
                            <MessageSquare className={cn(
                                "h-4 w-4 shrink-0 transition-transform group-hover:scale-110",
                                activeId === item.id ? "text-primary" : "text-muted-foreground/60"
                            )} />

                            <div className="flex-1 min-w-0 overflow-hidden">
                                <p className="text-sm font-medium truncate leading-tight">
                                    {item.title || "Sin título"}
                                </p>
                                <div className="flex items-center gap-2 mt-1 opacity-70">
                                    <span className="text-[10px] font-mono uppercase bg-primary/10 px-1 rounded">
                                        {item.model.split('/').pop()?.split('-')[0] || "IA"}
                                    </span>
                                    <span className="text-[10px] truncate">
                                        {new Date(item.updatedAt).toLocaleDateString()}
                                    </span>
                                </div>
                            </div>

                            <div className="opacity-0 group-hover:opacity-100 transition-opacity flex items-center">
                                <DropdownMenu>
                                    <DropdownMenuTrigger asChild onClick={(e: React.MouseEvent) => e.stopPropagation()}>
                                        <Button variant="ghost" size="icon" className="h-7 w-7 rounded-lg hover:bg-primary/20">
                                            <MoreVertical className="h-3.5 w-3.5" />
                                        </Button>
                                    </DropdownMenuTrigger>
                                    <DropdownMenuContent align="end" className="bg-card/95 backdrop-blur-sm border-primary/20 shadow-2xl">
                                        <DropdownMenuItem
                                            className="text-xs flex items-center gap-2 cursor-pointer focus:bg-primary/10"
                                            onClick={(e: React.MouseEvent) => {
                                                e.stopPropagation();
                                                // Implementación futura de edición rápida
                                                const newTitle = prompt("Nuevo título:", item.title);
                                                if (newTitle) onUpdateTitle(item.id, newTitle);
                                            }}
                                        >
                                            <Edit2 className="h-3 w-3" />
                                            Renombrar
                                        </DropdownMenuItem>
                                        <DropdownMenuItem
                                            className="text-xs text-destructive flex items-center gap-2 cursor-pointer focus:bg-destructive/10"
                                            onClick={(e: React.MouseEvent) => {
                                                e.stopPropagation();
                                                if (confirm("¿Eliminar esta conversación?")) onDelete(item.id);
                                            }}
                                        >
                                            <Trash2 className="h-3 w-3" />
                                            Eliminar
                                        </DropdownMenuItem>
                                    </DropdownMenuContent>
                                </DropdownMenu>
                            </div>
                        </div>
                    ))}
                </div>
            </ScrollArea>

            {/* Footer Info */}
            <div className="p-4 bg-muted/10 border-t border-primary/5">
                <div className="flex items-center gap-3 px-2">
                    <div className="h-2 w-2 rounded-full bg-success animate-pulse"></div>
                    <p className="text-[10px] text-muted-foreground font-medium uppercase tracking-tighter">
                        Cloud Sync v0.8.0 Activo
                    </p>
                </div>
            </div>
        </div>
    );
}
