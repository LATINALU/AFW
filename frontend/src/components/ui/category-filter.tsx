"use client";

import React from "react";
import { motion } from "framer-motion";

interface Category {
  id: string;
  name: string;
  emoji: string;
  count: number;
}

interface CategoryFilterProps {
  categories: Category[];
  selectedCategory: string | null;
  onSelectCategory: (categoryId: string | null) => void;
}

export const CategoryFilter: React.FC<CategoryFilterProps> = ({
  categories,
  selectedCategory,
  onSelectCategory,
}) => {
  return (
    <div className="flex flex-wrap gap-2 p-4 bg-card/50 rounded-xl border border-border/50">
      <motion.button
        whileHover={{ scale: 1.02 }}
        whileTap={{ scale: 0.98 }}
        onClick={() => onSelectCategory(null)}
        className={`
          px-4 py-2 rounded-lg text-sm font-medium transition-all
          ${selectedCategory === null
            ? "bg-primary text-white shadow-lg shadow-primary/30"
            : "bg-white/5 text-gray-400 hover:bg-white/10 hover:text-white"
          }
        `}
      >
        Todas ({categories.reduce((acc, cat) => acc + cat.count, 0)})
      </motion.button>

      {categories.map((category) => (
        <motion.button
          key={category.id}
          whileHover={{ scale: 1.02 }}
          whileTap={{ scale: 0.98 }}
          onClick={() => onSelectCategory(category.id)}
          className={`
            px-4 py-2 rounded-lg text-sm font-medium transition-all flex items-center gap-2
            ${selectedCategory === category.id
              ? "bg-primary text-white shadow-lg shadow-primary/30"
              : "bg-white/5 text-gray-400 hover:bg-white/10 hover:text-white"
            }
          `}
        >
          <span>{category.emoji}</span>
          <span className="hidden sm:inline">{category.name}</span>
          <span className="text-xs opacity-70">({category.count})</span>
        </motion.button>
      ))}
    </div>
  );
};

export default CategoryFilter;
