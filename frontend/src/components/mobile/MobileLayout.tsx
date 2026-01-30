/**
 * Mobile Layout v1.0.0
 * ====================
 * Layout principal para la versión móvil de la aplicación.
 */

'use client';

import React, { useState } from 'react';
import { MobileBottomNav } from './MobileBottomNav';
import { MobileChatInterface } from './MobileChatInterface';
import { MobileAgentSelector } from './MobileAgentSelector';
import { AnimatePresence } from 'framer-motion';

interface MobileLayoutProps {
  children?: React.ReactNode;
}

export function MobileLayout({ children }: MobileLayoutProps) {
  const [activeTab, setActiveTab] = useState<'home' | 'chat' | 'history' | 'agents' | 'settings'>('chat');
  const [showAgentSelector, setShowAgentSelector] = useState(false);

  return (
    <div className="h-screen flex flex-col bg-background">
      {/* Contenido principal */}
      <div className="flex-1 overflow-hidden pb-16">
        {children}
      </div>

      {/* Navegación inferior */}
      <MobileBottomNav
        activeTab={activeTab}
        onTabChange={setActiveTab}
      />

      {/* Modales y overlays */}
      <AnimatePresence>
        {showAgentSelector && (
          <MobileAgentSelector
            agents={[]}
            selectedAgents={[]}
            onToggleAgent={() => {}}
            onClose={() => setShowAgentSelector(false)}
          />
        )}
      </AnimatePresence>
    </div>
  );
}
