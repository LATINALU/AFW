/**
 * Mobile Agent Selector v1.0.0
 * ============================
 * Selector de agentes optimizado para móvil con gestos táctiles.
 */

'use client';

import React, { useState } from 'react';
import { X, Search, Check } from 'lucide-react';
import { motion, AnimatePresence } from 'framer-motion';

interface Agent {
  id: string;
  name: string;
  description: string;
  level: number;
  icon?: string;
}

interface MobileAgentSelectorProps {
  agents: Agent[];
  selectedAgents: string[];
  onToggleAgent: (agentId: string) => void;
  onClose: () => void;
  maxAgents?: number;
}

export function MobileAgentSelector({
  agents,
  selectedAgents,
  onToggleAgent,
  onClose,
  maxAgents = 30,
}: MobileAgentSelectorProps) {
  const [searchQuery, setSearchQuery] = useState('');

  const filteredAgents = agents.filter(
    (agent) =>
      agent.name.toLowerCase().includes(searchQuery.toLowerCase()) ||
      agent.description.toLowerCase().includes(searchQuery.toLowerCase())
  );

  const groupedAgents = filteredAgents.reduce((acc, agent) => {
    const level = agent.level;
    if (!acc[level]) {
      acc[level] = [];
    }
    acc[level].push(agent);
    return acc;
  }, {} as Record<number, Agent[]>);

  const levelNames: Record<number, string> = {
    1: 'Nivel 1: Fundamentos',
    2: 'Nivel 2: Especializados',
    3: 'Nivel 3: Avanzados',
  };

  return (
    <motion.div
      initial={{ x: '100%' }}
      animate={{ x: 0 }}
      exit={{ x: '100%' }}
      transition={{ type: 'spring', damping: 30, stiffness: 300 }}
      className="fixed inset-0 z-50 bg-background"
    >
      {/* Header */}
      <div className="sticky top-0 bg-background/95 backdrop-blur-sm border-b border-border">
        <div className="flex items-center justify-between px-4 py-3">
          <h2 className="text-lg font-semibold">
            Seleccionar Agentes ({selectedAgents.length}/{maxAgents})
          </h2>
          <button
            onClick={onClose}
            className="p-2 rounded-lg hover:bg-accent transition-colors"
            aria-label="Cerrar"
          >
            <X className="w-5 h-5" />
          </button>
        </div>

        {/* Barra de búsqueda */}
        <div className="px-4 pb-3">
          <div className="relative">
            <Search className="absolute left-3 top-1/2 -translate-y-1/2 w-4 h-4 text-muted-foreground" />
            <input
              type="text"
              value={searchQuery}
              onChange={(e) => setSearchQuery(e.target.value)}
              placeholder="Buscar agentes..."
              className="w-full pl-10 pr-4 py-2 bg-accent rounded-lg focus:outline-none focus:ring-2 focus:ring-primary"
            />
          </div>
        </div>
      </div>

      {/* Lista de agentes */}
      <div className="overflow-y-auto pb-20" style={{ height: 'calc(100vh - 140px)' }}>
        {Object.entries(groupedAgents)
          .sort(([a], [b]) => Number(a) - Number(b))
          .map(([level, levelAgents]) => (
            <div key={level} className="mb-6">
              <div className="sticky top-0 bg-background/95 backdrop-blur-sm px-4 py-2 border-b border-border">
                <h3 className="text-sm font-semibold text-muted-foreground">
                  {levelNames[Number(level)] || `Nivel ${level}`}
                </h3>
              </div>
              
              <div className="px-4 py-2 space-y-2">
                {levelAgents.map((agent) => (
                  <AgentCard
                    key={agent.id}
                    agent={agent}
                    isSelected={selectedAgents.includes(agent.id)}
                    onToggle={() => onToggleAgent(agent.id)}
                    disabled={
                      !selectedAgents.includes(agent.id) &&
                      selectedAgents.length >= maxAgents
                    }
                  />
                ))}
              </div>
            </div>
          ))}

        {filteredAgents.length === 0 && (
          <div className="flex flex-col items-center justify-center h-64 text-center px-6">
            <div className="text-4xl mb-4">🔍</div>
            <p className="text-muted-foreground">
              No se encontraron agentes
            </p>
          </div>
        )}
      </div>

      {/* Footer con acciones rápidas */}
      <div className="fixed bottom-0 left-0 right-0 bg-background/95 backdrop-blur-sm border-t border-border p-4">
        <div className="flex gap-2">
          <button
            onClick={() => {
              agents.forEach((agent) => {
                if (!selectedAgents.includes(agent.id)) {
                  onToggleAgent(agent.id);
                }
              });
            }}
            className="flex-1 px-4 py-2 bg-accent rounded-lg text-sm font-medium transition-colors active:scale-95"
          >
            Seleccionar Todos
          </button>
          <button
            onClick={() => {
              selectedAgents.forEach((agentId) => {
                onToggleAgent(agentId);
              });
            }}
            className="flex-1 px-4 py-2 bg-accent rounded-lg text-sm font-medium transition-colors active:scale-95"
          >
            Limpiar
          </button>
        </div>
      </div>
    </motion.div>
  );
}

function AgentCard({
  agent,
  isSelected,
  onToggle,
  disabled,
}: {
  agent: Agent;
  isSelected: boolean;
  onToggle: () => void;
  disabled: boolean;
}) {
  return (
    <motion.button
      whileTap={{ scale: disabled ? 1 : 0.98 }}
      onClick={onToggle}
      disabled={disabled}
      className={`w-full p-4 rounded-xl border-2 transition-all text-left ${
        isSelected
          ? 'border-primary bg-primary/10'
          : disabled
          ? 'border-border bg-accent/50 opacity-50'
          : 'border-border bg-accent hover:border-primary/50'
      }`}
    >
      <div className="flex items-start gap-3">
        <div className="flex-shrink-0 mt-1">
          {isSelected ? (
            <div className="w-6 h-6 bg-primary rounded-full flex items-center justify-center">
              <Check className="w-4 h-4 text-primary-foreground" />
            </div>
          ) : (
            <div className="w-6 h-6 border-2 border-border rounded-full" />
          )}
        </div>
        
        <div className="flex-1 min-w-0">
          <div className="flex items-center gap-2 mb-1">
            {agent.icon && <span className="text-lg">{agent.icon}</span>}
            <h4 className="font-semibold text-sm">{agent.name}</h4>
          </div>
          <p className="text-xs text-muted-foreground line-clamp-2">
            {agent.description}
          </p>
        </div>
      </div>
    </motion.button>
  );
}
