"use client";

import React, { useState, useMemo } from "react";
import { motion, AnimatePresence } from "framer-motion";
import { AgentCard } from "./agent-card";
import { CategoryFilter } from "./category-filter";

interface Agent {
  id: string;
  name: string;
  emoji: string;
  description: string;
  category: string;
}

interface Category {
  id: string;
  name: string;
  emoji: string;
  count: number;
}

interface AgentSelectorProps {
  agents: Agent[];
  categories: Category[];
  selectedAgents: string[];
  maxAgents?: number;
  onSelectionChange: (selected: string[]) => void;
}

export const AgentSelector: React.FC<AgentSelectorProps> = ({
  agents,
  categories,
  selectedAgents,
  maxAgents = 10,
  onSelectionChange,
}) => {
  const [selectedCategory, setSelectedCategory] = useState<string | null>(null);
  const [searchQuery, setSearchQuery] = useState("");

  const filteredAgents = useMemo(() => {
    return agents.filter((agent) => {
      const matchesCategory = !selectedCategory || agent.category === selectedCategory;
      const matchesSearch = !searchQuery || 
        agent.name.toLowerCase().includes(searchQuery.toLowerCase()) ||
        agent.description.toLowerCase().includes(searchQuery.toLowerCase());
      return matchesCategory && matchesSearch;
    });
  }, [agents, selectedCategory, searchQuery]);

  const handleAgentClick = (agentId: string) => {
    if (selectedAgents.includes(agentId)) {
      onSelectionChange(selectedAgents.filter((id) => id !== agentId));
    } else if (selectedAgents.length < maxAgents) {
      onSelectionChange([...selectedAgents, agentId]);
    }
  };

  return (
    <div className="space-y-6">
      {/* Header with counter and search */}
      <div className="flex flex-col sm:flex-row gap-4 items-start sm:items-center justify-between">
        <div className="flex items-center gap-4">
          <h2 className="text-2xl font-bold text-white">Seleccionar Agentes</h2>
          <span className={`
            px-3 py-1 rounded-full text-sm font-medium
            ${selectedAgents.length >= maxAgents 
              ? "bg-red-500/20 text-red-400 border border-red-500/50" 
              : "bg-primary/20 text-primary border border-primary/50"
            }
          `}>
            {selectedAgents.length} / {maxAgents}
          </span>
        </div>

        {/* Search */}
        <div className="relative w-full sm:w-64">
          <input
            type="text"
            placeholder="Buscar agentes..."
            value={searchQuery}
            onChange={(e) => setSearchQuery(e.target.value)}
            className="w-full px-4 py-2 pl-10 rounded-lg bg-card border border-border text-white placeholder-gray-500 focus:outline-none focus:ring-2 focus:ring-primary/50"
          />
          <svg
            className="absolute left-3 top-1/2 -translate-y-1/2 w-4 h-4 text-gray-500"
            fill="none"
            viewBox="0 0 24 24"
            stroke="currentColor"
          >
            <path
              strokeLinecap="round"
              strokeLinejoin="round"
              strokeWidth={2}
              d="M21 21l-6-6m2-5a7 7 0 11-14 0 7 7 0 0114 0z"
            />
          </svg>
        </div>
      </div>

      {/* Category Filter */}
      <CategoryFilter
        categories={categories}
        selectedCategory={selectedCategory}
        onSelectCategory={setSelectedCategory}
      />

      {/* Selected Agents Summary */}
      {selectedAgents.length > 0 && (
        <motion.div
          initial={{ opacity: 0, height: 0 }}
          animate={{ opacity: 1, height: "auto" }}
          className="p-4 rounded-xl bg-primary/10 border border-primary/30"
        >
          <div className="flex flex-wrap gap-2">
            <span className="text-sm text-primary font-medium">Seleccionados:</span>
            {selectedAgents.map((agentId) => {
              const agent = agents.find((a) => a.id === agentId);
              return (
                <motion.span
                  key={agentId}
                  initial={{ scale: 0 }}
                  animate={{ scale: 1 }}
                  exit={{ scale: 0 }}
                  className="inline-flex items-center gap-1 px-2 py-1 rounded-full bg-primary/20 text-sm"
                >
                  <span>{agent?.emoji}</span>
                  <span className="text-white">{agent?.name}</span>
                  <button
                    onClick={() => handleAgentClick(agentId)}
                    className="ml-1 w-4 h-4 rounded-full bg-white/20 flex items-center justify-center hover:bg-red-500/50 transition-colors"
                  >
                    ×
                  </button>
                </motion.span>
              );
            })}
          </div>
        </motion.div>
      )}

      {/* Agents Grid */}
      <div className="grid grid-cols-1 sm:grid-cols-2 lg:grid-cols-3 xl:grid-cols-4 gap-4">
        <AnimatePresence mode="popLayout">
          {filteredAgents.map((agent) => (
            <motion.div
              key={agent.id}
              layout
              initial={{ opacity: 0, scale: 0.9 }}
              animate={{ opacity: 1, scale: 1 }}
              exit={{ opacity: 0, scale: 0.9 }}
              transition={{ duration: 0.2 }}
            >
              <AgentCard
                {...agent}
                isSelected={selectedAgents.includes(agent.id)}
                onClick={() => handleAgentClick(agent.id)}
              />
            </motion.div>
          ))}
        </AnimatePresence>
      </div>

      {/* Empty state */}
      {filteredAgents.length === 0 && (
        <div className="text-center py-12">
          <div className="text-4xl mb-4">🔍</div>
          <p className="text-gray-400">No se encontraron agentes con esos criterios</p>
        </div>
      )}
    </div>
  );
};

export default AgentSelector;
