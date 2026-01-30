/**
 * Enhanced Agent Response v1.0.0
 * ==============================
 * Componente mejorado para mostrar respuestas de agentes con botón de guardar.
 */

'use client';

import React, { useState } from 'react';
import { 
  Bookmark, 
  Copy, 
  Download, 
  Check, 
  MoreVertical,
  Star,
  Share2
} from 'lucide-react';
import ReactMarkdown from 'react-markdown';
import { cn } from '@/lib/utils';

interface EnhancedAgentResponseProps {
  agentId: string;
  agentName: string;
  agentEmoji?: string;
  level?: number;
  specialty?: string;
  content: string;
  timestamp: Date;
  conversationId?: string;
  messageId?: string;
  onSaveResponse?: (data: {
    agentId: string;
    agentName: string;
    content: string;
    conversationId?: string;
    messageId?: string;
  }) => void;
  isSaved?: boolean;
  isFavorite?: boolean;
}

export function EnhancedAgentResponse({
  agentId,
  agentName,
  agentEmoji = '🤖',
  level = 1,
  specialty,
  content,
  timestamp,
  conversationId,
  messageId,
  onSaveResponse,
  isSaved = false,
  isFavorite = false,
}: EnhancedAgentResponseProps) {
  const [copied, setCopied] = useState(false);
  const [showMenu, setShowMenu] = useState(false);

  const handleCopy = async () => {
    try {
      await navigator.clipboard.writeText(content);
      setCopied(true);
      setTimeout(() => setCopied(false), 2000);
    } catch (error) {
      console.error('Error copying:', error);
    }
  };

  const handleQuickCopy = async () => {
    await handleCopy();
  };

  const handleExport = () => {
    const blob = new Blob([content], { type: 'text/markdown' });
    const url = URL.createObjectURL(blob);
    const a = document.createElement('a');
    a.href = url;
    a.download = `${agentName}_${new Date().toISOString().slice(0, 10)}.md`;
    a.click();
    URL.revokeObjectURL(url);
  };

  const handleSave = () => {
    if (onSaveResponse) {
      onSaveResponse({
        agentId,
        agentName,
        content,
        conversationId,
        messageId,
      });
    }
  };

  const getLevelColor = (level: number) => {
    const colors = {
      1: 'border-blue-500 bg-blue-500/10 text-blue-500',
      2: 'border-emerald-500 bg-emerald-500/10 text-emerald-500',
      3: 'border-amber-500 bg-amber-500/10 text-amber-500',
    };
    return colors[level as keyof typeof colors] || colors[1];
  };

  const levelColor = getLevelColor(level);

  return (
    <div className="group relative bg-accent rounded-lg border-l-4 overflow-hidden transition-all duration-200 hover:shadow-lg">
      {/* Header */}
      <div className="flex items-start justify-between p-4 border-b border-border/50">
        <div className="flex items-start gap-3">
          <div className={cn(
            "p-2 rounded-lg border",
            levelColor
          )}>
            <span className="text-2xl">{agentEmoji}</span>
          </div>
          
          <div className="flex-1 min-w-0">
            <div className="flex items-center gap-2 mb-1">
              <h3 className="font-semibold text-sm sm:text-base">{agentName}</h3>
              {isFavorite && (
                <Star className="w-4 h-4 text-yellow-500 fill-yellow-500" />
              )}
            </div>
            <div className="flex items-center gap-2 text-xs text-muted-foreground">
              <span className="px-2 py-1 rounded-full bg-primary/10 text-primary">
                Nivel {level}
              </span>
              {specialty && (
                <span>{specialty}</span>
              )}
            </div>
          </div>
        </div>

        {/* Quick Actions - Always Visible */}
        <div className="flex items-center gap-2">
          {/* One-Click Copy Button */}
          <button
            onClick={handleQuickCopy}
            className={cn(
              "p-2 rounded-lg transition-all active:scale-95",
              copied
                ? "bg-green-500 text-white"
                : "bg-accent hover:bg-accent/80"
            )}
            title="Copiar respuesta completa"
          >
            {copied ? (
              <Check className="w-5 h-5" />
            ) : (
              <Copy className="w-5 h-5" />
            )}
          </button>

          {/* More Actions Menu */}
          <div className="relative">
            <button
              onClick={() => setShowMenu(!showMenu)}
              className="p-2 hover:bg-accent rounded-lg transition-colors"
            >
              <MoreVertical className="w-4 h-4" />
            </button>

            {showMenu && (
            <div className="absolute right-0 top-8 bg-background border border-border rounded-lg shadow-lg z-50 py-1 min-w-[150px]">
              <button
                onClick={handleCopy}
                className="w-full px-3 py-2 text-left text-sm hover:bg-accent flex items-center gap-2"
              >
                {copied ? (
                  <Check className="w-4 h-4 text-green-500" />
                ) : (
                  <Copy className="w-4 h-4" />
                )}
                {copied ? '¡Copiado!' : 'Copiar'}
              </button>
              
              <button
                onClick={handleExport}
                className="w-full px-3 py-2 text-left text-sm hover:bg-accent flex items-center gap-2"
              >
                <Download className="w-4 h-4" />
                Exportar
              </button>
              
              <button
                onClick={handleSave}
                disabled={isSaved}
                className="w-full px-3 py-2 text-left text-sm hover:bg-accent flex items-center gap-2 disabled:opacity-50 disabled:cursor-not-allowed"
              >
                <Bookmark className={`w-4 h-4 ${isSaved ? 'text-green-500' : ''}`} />
                {isSaved ? 'Guardado' : 'Guardar'}
              </button>
            </div>
            )}
          </div>
        </div>
      </div>

      {/* Content */}
      <div className="p-4">
        <div className="prose prose-sm max-w-none text-sm sm:text-base">
          <ReactMarkdown
            components={{
              h1: ({ children }) => <h1 className="text-lg sm:text-xl font-bold mb-2">{children}</h1>,
              h2: ({ children }) => <h2 className="text-base sm:text-lg font-semibold mb-2">{children}</h2>,
              h3: ({ children }) => <h3 className="text-sm sm:text-base font-medium mb-1">{children}</h3>,
              p: ({ children }) => <p className="leading-relaxed mb-3">{children}</p>,
              ul: ({ children }) => <ul className="list-disc list-inside space-y-1 mb-3">{children}</ul>,
              ol: ({ children }) => <ol className="list-decimal list-inside space-y-1 mb-3">{children}</ol>,
              li: ({ children }) => <li className="text-sm sm:text-base">{children}</li>,
              code: ({ children, className }) => {
                const isInline = !className;
                return isInline ? (
                  <code className="px-1.5 py-0.5 rounded text-xs sm:text-sm bg-background border border-border font-mono">
                    {children}
                  </code>
                ) : (
                  <code className="block p-2 sm:p-3 rounded-lg bg-background border border-border text-xs sm:text-sm font-mono overflow-x-auto whitespace-pre-wrap break-words">
                    {children}
                  </code>
                );
              },
              blockquote: ({ children }) => (
                <blockquote className="border-l-2 border-border pl-4 italic my-3">
                  {children}
                </blockquote>
              ),
              strong: ({ children }) => <strong className="font-semibold">{children}</strong>,
            }}
          >
            {content}
          </ReactMarkdown>
        </div>
      </div>

      {/* Footer */}
      <div className="flex items-center justify-between px-4 py-2 bg-background/50 border-t border-border/50">
        <div className="flex items-center gap-1 text-xs text-muted-foreground">
          <span>{timestamp.toLocaleTimeString('es-ES', { hour: '2-digit', minute: '2-digit' })}</span>
        </div>
        
        <div className="flex items-center gap-2">
          {/* Botón de guardar principal */}
          <button
            onClick={handleSave}
            disabled={isSaved}
            className={cn(
              "px-3 py-1 rounded-md text-xs font-medium transition-all",
              "hover:scale-105 active:scale-95",
              isSaved 
                ? "bg-green-500 text-white cursor-default" 
                : levelColor + " border border-current/30"
            )}
          >
            {isSaved ? (
              <>
                <Check className="w-3 h-3 mr-1" />
                Guardado
              </>
            ) : (
              <>
                <Bookmark className="w-3 h-3 mr-1" />
                Guardar
              </>
            )}
          </button>
          
          <span className="text-xs font-mono text-muted-foreground">
            @{agentId}
          </span>
        </div>
      </div>
    </div>
  );
}
