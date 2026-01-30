/**
 * Mobile Bottom Navigation v1.0.0
 * ================================
 * Navegación inferior optimizada para móvil con gestos táctiles.
 */

'use client';

import React from 'react';
import { Home, MessageSquare, History, Settings, Users } from 'lucide-react';
import { motion } from 'framer-motion';

interface MobileBottomNavProps {
  activeTab: 'home' | 'chat' | 'history' | 'agents' | 'settings';
  onTabChange: (tab: 'home' | 'chat' | 'history' | 'agents' | 'settings') => void;
}

export function MobileBottomNav({ activeTab, onTabChange }: MobileBottomNavProps) {
  const tabs = [
    { id: 'home' as const, icon: Home, label: 'Inicio' },
    { id: 'chat' as const, icon: MessageSquare, label: 'Chat' },
    { id: 'agents' as const, icon: Users, label: 'Agentes' },
    { id: 'history' as const, icon: History, label: 'Historial' },
    { id: 'settings' as const, icon: Settings, label: 'Config' },
  ];

  return (
    <nav className="fixed bottom-0 left-0 right-0 bg-background/95 backdrop-blur-sm border-t border-border z-50">
      <div className="flex items-center justify-around px-2 py-2 safe-area-inset-bottom">
        {tabs.map((tab) => {
          const Icon = tab.icon;
          const isActive = activeTab === tab.id;

          return (
            <button
              key={tab.id}
              onClick={() => onTabChange(tab.id)}
              className="relative flex flex-col items-center justify-center min-w-[60px] py-2 px-3 transition-colors"
              aria-label={tab.label}
            >
              <div className="relative">
                <Icon
                  className={`w-6 h-6 transition-colors ${
                    isActive ? 'text-primary' : 'text-muted-foreground'
                  }`}
                />
                
                {isActive && (
                  <motion.div
                    layoutId="activeTab"
                    className="absolute -bottom-1 left-1/2 -translate-x-1/2 w-1 h-1 bg-primary rounded-full"
                    transition={{ type: 'spring', stiffness: 500, damping: 30 }}
                  />
                )}
              </div>
              
              <span
                className={`text-xs mt-1 transition-colors ${
                  isActive ? 'text-primary font-medium' : 'text-muted-foreground'
                }`}
              >
                {tab.label}
              </span>
            </button>
          );
        })}
      </div>
    </nav>
  );
}
