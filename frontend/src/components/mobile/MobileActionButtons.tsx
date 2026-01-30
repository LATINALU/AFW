/**
 * Mobile Action Buttons v1.0.0
 * ============================
 * Botones de acción para interfaz móvil: Agentes, Memoria, Tareas
 */

'use client';

import React from 'react';
import { Users, CheckSquare } from 'lucide-react';
import { cn } from '@/lib/utils';

interface MobileActionButtonsProps {
  onOpenAgents: () => void;
  onOpenTasks: () => void;
  activeView?: 'agents' | 'tasks' | null;
}

export function MobileActionButtons({
  onOpenAgents,
  onOpenTasks,
  activeView = null,
}: MobileActionButtonsProps) {
  return (
    <div className="fixed bottom-0 left-0 right-0 z-40 px-3 pb-safe">
      <div className="bg-background/95 backdrop-blur-sm border-t border-border shadow-lg">
        <div className="grid grid-cols-2 gap-1 p-1.5">
          {/* Botón Agentes */}
          <button
            onClick={onOpenAgents}
            className={cn(
              "flex flex-col items-center justify-center gap-0.5 py-2 px-1 rounded-lg transition-all",
              "active:scale-95",
              activeView === 'agents'
                ? "bg-blue-500 text-white shadow-md"
                : "bg-accent hover:bg-accent/80"
            )}
          >
            <Users className="w-5 h-5" />
            <span className="text-[10px] font-medium">Agentes</span>
          </button>

          {/* Botón Tareas */}
          <button
            onClick={onOpenTasks}
            className={cn(
              "flex flex-col items-center justify-center gap-0.5 py-2 px-1 rounded-lg transition-all",
              "active:scale-95",
              activeView === 'tasks'
                ? "bg-green-500 text-white shadow-md"
                : "bg-accent hover:bg-accent/80"
            )}
          >
            <CheckSquare className="w-5 h-5" />
            <span className="text-[10px] font-medium">Tareas</span>
          </button>
        </div>
      </div>
    </div>
  );
}
