/**
 * Quick Start Guide v1.0.0
 * ========================
 * Guía rápida para configurar API keys en PC y móvil
 */

'use client';

import React, { useState } from 'react';
import { X, Key, Check, AlertCircle, Copy, Eye, EyeOff } from 'lucide-react';
import { cn } from '@/lib/utils';

interface QuickStartGuideProps {
  isOpen: boolean;
  onClose: () => void;
}

export function QuickStartGuide({ isOpen, onClose }: QuickStartGuideProps) {
  const [apiKeys, setApiKeys] = useState({
    groq: '',
    openai: '',
    anthropic: '',
  });
  const [showKeys, setShowKeys] = useState({
    groq: false,
    openai: false,
    anthropic: false,
  });
  const [saved, setSaved] = useState(false);

  const handleSave = () => {
    // Guardar en localStorage
    localStorage.setItem('atp_api_keys', JSON.stringify(apiKeys));
    setSaved(true);
    setTimeout(() => setSaved(false), 2000);
  };

  const handleCopyExample = (provider: string) => {
    const examples = {
      groq: 'gsk_xxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxx',
      openai: 'sk-xxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxx',
      anthropic: 'sk-ant-xxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxx',
    };
    navigator.clipboard.writeText(examples[provider as keyof typeof examples]);
  };

  if (!isOpen) return null;

  return (
    <div className="fixed inset-0 z-50 bg-black/50 flex items-center justify-center p-4">
      <div className="bg-background rounded-2xl shadow-2xl max-w-2xl w-full max-h-[90vh] overflow-y-auto">
        {/* Header */}
        <div className="sticky top-0 bg-background border-b border-border p-6 flex items-center justify-between">
          <div className="flex items-center gap-3">
            <div className="p-2 bg-blue-500/10 rounded-lg">
              <Key className="w-6 h-6 text-blue-500" />
            </div>
            <div>
              <h2 className="text-2xl font-bold">Guía Rápida</h2>
              <p className="text-sm text-muted-foreground">
                Configura tus API keys para comenzar
              </p>
            </div>
          </div>
          <button
            onClick={onClose}
            className="p-2 hover:bg-accent rounded-lg transition-colors"
          >
            <X className="w-6 h-6" />
          </button>
        </div>

        {/* Content */}
        <div className="p-6 space-y-6">
          {/* Alert */}
          <div className="flex gap-3 p-4 bg-gradient-to-r from-blue-500/10 to-green-500/10 border border-blue-500/20 rounded-xl">
            <AlertCircle className="w-5 h-5 text-blue-500 flex-shrink-0 mt-0.5" />
            <div className="text-sm">
              <p className="font-medium text-blue-500 mb-1">
                ¡Bienvenido a ATP!
              </p>
              <p className="text-muted-foreground">
                ATP necesita acceso a modelos de IA para funcionar. Las API keys te permiten usar tus propias cuentas de OpenAI, Groq o Anthropic.
              </p>
            </div>
          </div>

          {/* Steps */}
          <div className="space-y-6">
            {/* Step 1: Groq */}
            <div className="space-y-3">
              <div className="flex items-center gap-2">
                <div className="w-8 h-8 bg-blue-500 text-white rounded-full flex items-center justify-center text-sm font-bold">
                  1
                </div>
                <h3 className="text-lg font-semibold">Groq API Key (Recomendado)</h3>
              </div>
              
              <div className="ml-10 space-y-3">
                <p className="text-sm text-muted-foreground">
                  Groq ofrece acceso rápido y gratuito a modelos como Llama.
                </p>
                
                <div className="space-y-2">
                  <label className="text-sm font-medium">Tu API Key de Groq</label>
                  <div className="flex gap-2">
                    <div className="relative flex-1">
                      <input
                        type={showKeys.groq ? 'text' : 'password'}
                        value={apiKeys.groq}
                        onChange={(e) => setApiKeys({ ...apiKeys, groq: e.target.value })}
                        placeholder="gsk_xxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxx"
                        className="w-full px-4 py-3 pr-10 bg-accent rounded-xl focus:outline-none focus:ring-2 focus:ring-blue-500"
                      />
                      <button
                        onClick={() => setShowKeys({ ...showKeys, groq: !showKeys.groq })}
                        className="absolute right-3 top-1/2 -translate-y-1/2 text-muted-foreground hover:text-foreground"
                      >
                        {showKeys.groq ? <EyeOff className="w-4 h-4" /> : <Eye className="w-4 h-4" />}
                      </button>
                    </div>
                  </div>
                </div>

                <a
                  href="https://console.groq.com/keys"
                  target="_blank"
                  rel="noopener noreferrer"
                  className="inline-flex items-center justify-center gap-2 px-6 py-3 bg-gradient-to-r from-blue-500 to-green-500 text-white font-semibold rounded-xl hover:shadow-lg hover:scale-105 transition-all"
                >
                  <Key className="w-5 h-5" />
                  Obtener API Key GRATIS en Groq
                </a>
                <p className="text-xs text-muted-foreground">
                  ✨ Recomendado: Groq es rápido, gratuito y fácil de configurar
                </p>
              </div>
            </div>

            {/* Step 2: OpenAI */}
            <div className="space-y-3">
              <div className="flex items-center gap-2">
                <div className="w-8 h-8 bg-green-500 text-white rounded-full flex items-center justify-center text-sm font-bold">
                  2
                </div>
                <h3 className="text-lg font-semibold">OpenAI API Key (Opcional)</h3>
              </div>
              
              <div className="ml-10 space-y-3">
                <p className="text-sm text-muted-foreground">
                  Para usar GPT-4 y otros modelos de OpenAI.
                </p>
                
                <div className="space-y-2">
                  <label className="text-sm font-medium">Tu API Key de OpenAI</label>
                  <div className="relative">
                    <input
                      type={showKeys.openai ? 'text' : 'password'}
                      value={apiKeys.openai}
                      onChange={(e) => setApiKeys({ ...apiKeys, openai: e.target.value })}
                      placeholder="sk-xxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxx"
                      className="w-full px-4 py-3 pr-10 bg-accent rounded-xl focus:outline-none focus:ring-2 focus:ring-green-500"
                    />
                    <button
                      onClick={() => setShowKeys({ ...showKeys, openai: !showKeys.openai })}
                      className="absolute right-3 top-1/2 -translate-y-1/2 text-muted-foreground hover:text-foreground"
                    >
                      {showKeys.openai ? <EyeOff className="w-4 h-4" /> : <Eye className="w-4 h-4" />}
                    </button>
                  </div>
                </div>

                <a
                  href="https://platform.openai.com/api-keys"
                  target="_blank"
                  rel="noopener noreferrer"
                  className="inline-flex items-center gap-2 text-sm text-green-500 hover:underline"
                >
                  → Obtener API Key de OpenAI
                </a>
              </div>
            </div>

            {/* Step 3: Anthropic */}
            <div className="space-y-3">
              <div className="flex items-center gap-2">
                <div className="w-8 h-8 bg-purple-500 text-white rounded-full flex items-center justify-center text-sm font-bold">
                  3
                </div>
                <h3 className="text-lg font-semibold">Anthropic API Key (Opcional)</h3>
              </div>
              
              <div className="ml-10 space-y-3">
                <p className="text-sm text-muted-foreground">
                  Para usar Claude y otros modelos de Anthropic.
                </p>
                
                <div className="space-y-2">
                  <label className="text-sm font-medium">Tu API Key de Anthropic</label>
                  <div className="relative">
                    <input
                      type={showKeys.anthropic ? 'text' : 'password'}
                      value={apiKeys.anthropic}
                      onChange={(e) => setApiKeys({ ...apiKeys, anthropic: e.target.value })}
                      placeholder="sk-ant-xxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxx"
                      className="w-full px-4 py-3 pr-10 bg-accent rounded-xl focus:outline-none focus:ring-2 focus:ring-purple-500"
                    />
                    <button
                      onClick={() => setShowKeys({ ...showKeys, anthropic: !showKeys.anthropic })}
                      className="absolute right-3 top-1/2 -translate-y-1/2 text-muted-foreground hover:text-foreground"
                    >
                      {showKeys.anthropic ? <EyeOff className="w-4 h-4" /> : <Eye className="w-4 h-4" />}
                    </button>
                  </div>
                </div>

                <a
                  href="https://console.anthropic.com/settings/keys"
                  target="_blank"
                  rel="noopener noreferrer"
                  className="inline-flex items-center gap-2 text-sm text-purple-500 hover:underline"
                >
                  → Obtener API Key de Anthropic
                </a>
              </div>
            </div>
          </div>

          {/* Security Note */}
          <div className="flex gap-3 p-4 bg-yellow-500/10 border border-yellow-500/20 rounded-xl">
            <AlertCircle className="w-5 h-5 text-yellow-500 flex-shrink-0 mt-0.5" />
            <div className="text-sm">
              <p className="font-medium text-yellow-500 mb-1">
                Seguridad
              </p>
              <p className="text-muted-foreground">
                Tus API keys se guardan localmente en tu dispositivo y nunca se comparten con terceros. Funciona tanto en PC como en móvil.
              </p>
            </div>
          </div>

          {/* Save Button */}
          <div className="flex gap-3">
            <button
              onClick={handleSave}
              disabled={!apiKeys.groq && !apiKeys.openai && !apiKeys.anthropic}
              className={cn(
                "flex-1 px-6 py-3 rounded-xl font-medium transition-all",
                "disabled:opacity-50 disabled:cursor-not-allowed",
                saved
                  ? "bg-green-500 text-white"
                  : "bg-blue-500 text-white hover:bg-blue-600 active:scale-95"
              )}
            >
              {saved ? (
                <span className="flex items-center justify-center gap-2">
                  <Check className="w-5 h-5" />
                  ¡Guardado!
                </span>
              ) : (
                'Guardar y Comenzar'
              )}
            </button>
            
            <button
              onClick={onClose}
              className="px-6 py-3 bg-accent hover:bg-accent/80 rounded-xl font-medium transition-colors"
            >
              Cerrar
            </button>
          </div>

          {/* Mobile Note */}
          <div className="text-center text-sm text-muted-foreground">
            <p>💡 Esta configuración funciona en PC y móvil</p>
          </div>
        </div>
      </div>
    </div>
  );
}
