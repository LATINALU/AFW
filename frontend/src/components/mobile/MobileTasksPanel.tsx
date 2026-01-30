/**
 * Mobile Tasks Panel v1.0.0
 * =========================
 * Panel de gestión de tareas para interfaz móvil
 */

'use client';

import React, { useState, useEffect } from 'react';
import { X, Plus, Trash2, CheckSquare, Square } from 'lucide-react';
import { cn } from '@/lib/utils';
import { PRESETS } from '@/data/presets';

interface Task {
  id: string;
  title: string;
  completed: boolean;
  createdAt: Date;
  icon?: any;
  agents?: string[];
}

interface MobileTasksPanelProps {
  isOpen: boolean;
  onClose: () => void;
  onSelectTask?: (agents: string[]) => void;
}

export function MobileTasksPanel({ isOpen, onClose, onSelectTask }: MobileTasksPanelProps) {
  const [selectedPreset, setSelectedPreset] = useState<string | null>(null);

  const handlePresetSelect = (preset: typeof PRESETS[0]) => {
    setSelectedPreset(preset.title === selectedPreset ? null : preset.title);
    if (onSelectTask && preset.title !== selectedPreset) {
      onSelectTask(preset.agents);
    }
  };

  if (!isOpen) return null;

  return (
    <div className="fixed inset-0 z-50 bg-background">
      {/* Header */}
      <div className="flex items-center justify-between p-4 border-b border-border">
        <div className="flex items-center gap-2">
          <CheckSquare className="w-6 h-6 text-green-500" />
          <h2 className="text-xl font-bold">Tareas</h2>
        </div>
        <button
          onClick={onClose}
          className="p-2 hover:bg-accent rounded-lg transition-colors"
        >
          <X className="w-6 h-6" />
        </button>
      </div>

      {/* Content */}
      <div className="flex-1 overflow-y-auto p-4 pb-24">
        <div className="mb-4">
          <h3 className="text-sm font-semibold text-muted-foreground mb-2">
            16 Tareas Preprogramadas
          </h3>
          <p className="text-xs text-muted-foreground">
            Selecciona una tarea para ver los agentes especializados
          </p>
        </div>

        {/* Preset Tasks Grid */}
        <div className="space-y-2">
          {PRESETS.map((preset, idx) => {
            const Icon = preset.icon;
            const isSelected = selectedPreset === preset.title;
            
            return (
              <button
                key={idx}
                onClick={() => handlePresetSelect(preset)}
                className={cn(
                  "w-full flex items-center gap-3 p-3 rounded-xl transition-all text-left",
                  "border-2",
                  isSelected
                    ? "bg-green-500/10 border-green-500"
                    : "bg-accent border-transparent hover:border-primary/20"
                )}
              >
                <div className={cn(
                  "p-2 rounded-lg shrink-0",
                  isSelected
                    ? "bg-green-500 text-white"
                    : "bg-primary/10 text-primary"
                )}>
                  <Icon className="w-5 h-5" />
                </div>
                
                <div className="flex-1 min-w-0">
                  <p className="font-medium text-sm truncate">
                    {preset.title}
                  </p>
                  <p className="text-xs text-muted-foreground truncate">
                    {preset.description}
                  </p>
                  {isSelected && (
                    <div className="mt-2 flex flex-wrap gap-1">
                      {preset.agents.map((agent, i) => (
                        <span
                          key={i}
                          className="text-[10px] px-2 py-0.5 bg-green-500/20 text-green-700 dark:text-green-300 rounded-full"
                        >
                          {agent}
                        </span>
                      ))}
                    </div>
                  )}
                </div>

                {isSelected && (
                  <CheckSquare className="w-5 h-5 text-green-500 shrink-0" />
                )}
              </button>
            );
          })}
        </div>
      </div>
    </div>
  );
}
