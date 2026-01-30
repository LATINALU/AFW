"use client";

import React from "react";
import { motion } from "framer-motion";

interface AgentCardProps {
  id: string;
  name: string;
  emoji: string;
  description: string;
  category: string;
  isSelected?: boolean;
  onClick?: () => void;
}

export const AgentCard: React.FC<AgentCardProps> = ({
  id,
  name,
  emoji,
  description,
  category,
  isSelected = false,
  onClick,
}) => {
  const categoryColors: Record<string, string> = {
    software_development: "from-blue-500/20 to-cyan-500/20 border-blue-500/50",
    marketing: "from-pink-500/20 to-rose-500/20 border-pink-500/50",
    finance: "from-green-500/20 to-emerald-500/20 border-green-500/50",
    legal: "from-purple-500/20 to-violet-500/20 border-purple-500/50",
    human_resources: "from-orange-500/20 to-amber-500/20 border-orange-500/50",
    sales: "from-red-500/20 to-orange-500/20 border-red-500/50",
    operations: "from-slate-500/20 to-gray-500/20 border-slate-500/50",
    education: "from-indigo-500/20 to-blue-500/20 border-indigo-500/50",
    creative: "from-fuchsia-500/20 to-pink-500/20 border-fuchsia-500/50",
    project_management: "from-teal-500/20 to-cyan-500/20 border-teal-500/50",
    mercadolibre: "from-yellow-500/20 to-amber-500/20 border-yellow-500/50",
    youtube: "from-red-600/20 to-red-500/20 border-red-600/50",
  };

  const getCategoryColor = () => categoryColors[category] || "from-gray-500/20 to-slate-500/20 border-gray-500/50";

  return (
    <motion.div
      whileHover={{ scale: 1.02, y: -4 }}
      whileTap={{ scale: 0.98 }}
      onClick={onClick}
      className={`
        relative group cursor-pointer rounded-xl p-4
        bg-gradient-to-br ${getCategoryColor()}
        border transition-all duration-300
        ${isSelected 
          ? "ring-2 ring-primary shadow-lg shadow-primary/20" 
          : "hover:shadow-lg hover:shadow-white/5"
        }
      `}
    >
      {/* Selection indicator */}
      {isSelected && (
        <div className="absolute top-2 right-2 w-6 h-6 rounded-full bg-primary flex items-center justify-center">
          <svg className="w-4 h-4 text-white" fill="none" viewBox="0 0 24 24" stroke="currentColor">
            <path strokeLinecap="round" strokeLinejoin="round" strokeWidth={2} d="M5 13l4 4L19 7" />
          </svg>
        </div>
      )}

      {/* Glow effect on hover */}
      <div className="absolute inset-0 rounded-xl bg-gradient-to-r from-primary/0 via-primary/5 to-secondary/0 opacity-0 group-hover:opacity-100 transition-opacity duration-300" />

      <div className="relative z-10">
        <span className="text-4xl block mb-3">{emoji}</span>
        <h3 className="font-semibold text-base text-white mb-1">{name}</h3>
        <p className="text-xs text-gray-400 line-clamp-2 mb-3">{description}</p>
        <span className="inline-block text-[10px] px-2 py-1 rounded-full bg-white/10 text-gray-300 capitalize">
          {category.replace(/_/g, " ")}
        </span>
      </div>
    </motion.div>
  );
};

export default AgentCard;
