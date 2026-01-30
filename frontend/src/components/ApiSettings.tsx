"use client";

import { useState, useEffect } from "react";
import { cn } from "@/lib/utils";
import { SecureStorage } from "@/lib/encryption";
import {
  Key,
  Plus,
  Trash2,
  Check,
  X,
  Eye,
  EyeOff,
  Settings,
  Zap,
  AlertCircle,
  ChevronDown,
  Save,
  Loader2,
  RefreshCw,
  Shield,
  Lock,
} from "lucide-react";

export interface ApiProvider {
  id: string;
  name: string;
  type: "groq" | "openai" | "anthropic" | "local" | "custom";
  apiKey: string;
  baseUrl?: string;
  models: string[];
  enabledModels?: string[]; // Modelos que el usuario ha habilitado para usar
  isActive: boolean;
}

const DEFAULT_PROVIDERS: Omit<ApiProvider, "apiKey" | "isActive">[] = [
  {
    id: "groq",
    name: "Groq",
    type: "groq",
    baseUrl: "https://api.groq.com/openai/v1",
    models: ["openai/gpt-oss-120b", "llama-3.3-70b-versatile"], // Solo los 2 modelos disponibles
  },
  {
    id: "openai",
    name: "OpenAI",
    type: "openai",
    baseUrl: "https://api.openai.com/v1",
    models: ["gpt-4", "gpt-3.5-turbo"],
  },
  {
    id: "anthropic",
    name: "Anthropic",
    type: "anthropic",
    baseUrl: "https://api.anthropic.com",
    models: ["claude-3-sonnet-20240229"],
  },
  {
    id: "local",
    name: "Local AI",
    type: "local",
    baseUrl: "http://localhost:11434/v1",
    models: ["llama2", "mistral", "codellama"],
  },
];

interface ApiSettingsProps {
  isOpen: boolean;
  onClose: () => void;
  onProvidersChange: (providers: ApiProvider[]) => void;
}

export function ApiSettings({ isOpen, onClose, onProvidersChange }: ApiSettingsProps) {
  const [providers, setProviders] = useState<ApiProvider[]>([]);
  const [originalProviders, setOriginalProviders] = useState<ApiProvider[]>([]);
  const [showKeys, setShowKeys] = useState<Record<string, boolean>>({});
  const [expandedProvider, setExpandedProvider] = useState<string | null>(null);
  const [customProvider, setCustomProvider] = useState({
    name: "",
    baseUrl: "",
    apiKey: "",
    models: "",
  });
  const [showAddCustom, setShowAddCustom] = useState(false);
  const [loadingModels, setLoadingModels] = useState<string | null>(null);
  const [modelError, setModelError] = useState<string | null>(null);
  const [saveToStorage, setSaveToStorage] = useState(true);
  const [hasChanges, setHasChanges] = useState(false);

  // Load providers from localStorage on mount
  useEffect(() => {
    // Cargar configuración guardada con SecureStorage
    const loadSavedProviders = async () => {
      try {
        const saved = await SecureStorage.getItem("api-providers");
        if (saved) {
          setProviders(saved);
          setOriginalProviders(saved);
          onProvidersChange(saved);
        }
      } catch (e) {
        console.error("Error loading providers:", e);
        // Fallback a localStorage si SecureStorage falla
        try {
          const saved = localStorage.getItem("atp-api-providers");
          if (saved) {
            const parsed = JSON.parse(saved);
            setProviders(parsed);
            setOriginalProviders(parsed);
            onProvidersChange(parsed);
          }
        } catch (fallbackError) {
          console.error("Error loading providers from fallback:", fallbackError);
        }
      }
    };

    // Cargar preferencia de guardado
    const savePreference = localStorage.getItem("atp-save-apis");
    setSaveToStorage(savePreference === "true");

    loadSavedProviders();
  }, []);

  const saveProviders = (newProviders: ApiProvider[]) => {
    setProviders(newProviders);
    // Detectar cambios
    const changes = JSON.stringify(newProviders) !== JSON.stringify(originalProviders);
    setHasChanges(changes);
  };

  const applyChanges = async () => {
    if (saveToStorage) {
      try {
        // Guardar con SecureStorage (encriptado)
        await SecureStorage.setItem("api-providers", providers);
        console.log("✅ API providers guardados con SecureStorage");
      } catch (e) {
        console.error("Error guardando con SecureStorage, usando fallback:", e);
        // Fallback a localStorage si SecureStorage falla
        localStorage.setItem("atp-api-providers", JSON.stringify(providers));
      }
    }
    setOriginalProviders(providers);
    onProvidersChange(providers);
    setHasChanges(false);
    onClose();
  };

  const toggleSaveToStorage = () => {
    const newValue = !saveToStorage;
    setSaveToStorage(newValue);
    localStorage.setItem("atp-save-apis", String(newValue));

    if (!newValue) {
      // Si desactiva, borrar las APIs guardadas
      try {
        SecureStorage.removeItem("api-providers");
      } catch (e) {
        console.error("Error borrando de SecureStorage:", e);
        // Fallback
        localStorage.removeItem("atp-api-providers");
      }
    } else {
      // Si activa, guardar las actuales
      applyChanges();
    }
  };

  const clearAllApis = () => {
    setProviders([]);
    setHasChanges(true);
  };

  const handleAddProvider = (defaultProvider: typeof DEFAULT_PROVIDERS[0]) => {
    const existing = providers.find(p => p.id === defaultProvider.id);
    if (existing) {
      setExpandedProvider(defaultProvider.id);
      return;
    }

    const newProvider: ApiProvider = {
      ...defaultProvider,
      apiKey: "",
      isActive: false,
    };

    saveProviders([...providers, newProvider]);
    setExpandedProvider(defaultProvider.id);
  };

  const handleUpdateProvider = (id: string, updates: Partial<ApiProvider>) => {
    const newProviders = providers.map(p =>
      p.id === id ? { ...p, ...updates } : p
    );
    saveProviders(newProviders);
  };

  const handleRemoveProvider = (id: string) => {
    saveProviders(providers.filter(p => p.id !== id));
  };

  const handleAddCustomProvider = () => {
    if (!customProvider.name || !customProvider.apiKey) return;

    const newProvider: ApiProvider = {
      id: `custom-${Date.now()}`,
      name: customProvider.name,
      type: "custom",
      apiKey: customProvider.apiKey,
      baseUrl: customProvider.baseUrl || undefined,
      models: customProvider.models.split(",").map(m => m.trim()).filter(Boolean),
      isActive: true,
    };

    saveProviders([...providers, newProvider]);
    setCustomProvider({ name: "", baseUrl: "", apiKey: "", models: "" });
    setShowAddCustom(false);
  };

  const toggleKeyVisibility = (id: string) => {
    setShowKeys(prev => ({ ...prev, [id]: !prev[id] }));
  };

  // Detectar modelos disponibles en la API
  const fetchModelsForProvider = async (providerId: string) => {
    const provider = providers.find(p => p.id === providerId);
    if (!provider || !provider.apiKey) {
      setModelError("Ingresa una API key primero");
      return;
    }

    setLoadingModels(providerId);
    setModelError(null);

    try {
      const response = await fetch("/api/fetch-models", {
        method: "POST",
        headers: { "Content-Type": "application/json" },
        body: JSON.stringify({
          api_type: provider.type,
          api_key: provider.apiKey,
          base_url: provider.baseUrl || null,
        }),
      });

      const data = await response.json();

      if (data.success && data.models.length > 0) {
        const modelIds = data.models.map((m: { id: string }) => m.id);
        handleUpdateProvider(providerId, {
          models: modelIds,
          isActive: true
        });
        setModelError(null);
      } else {
        setModelError(data.error || "No se encontraron modelos");
      }
    } catch (err) {
      setModelError("Error de conexión. Verifica el backend.");
    } finally {
      setLoadingModels(null);
    }
  };

  if (!isOpen) return null;

  return (
    <div className="fixed inset-0 z-50 flex items-center justify-center">
      {/* Backdrop */}
      <div
        className="absolute inset-0 bg-black/60 backdrop-blur-sm"
        onClick={onClose}
      />

      {/* Modal */}
      <div className="relative w-full max-w-2xl max-h-[85vh] overflow-hidden rounded-xl border border-border bg-card shadow-2xl">
        {/* Header */}
        <div className="flex items-center justify-between p-4 border-b border-border">
          <div className="flex items-center gap-3">
            <div className="p-2 rounded-lg bg-primary/10">
              <Key className="h-5 w-5 text-primary" />
            </div>
            <div>
              <h2 className="text-lg font-bold text-foreground">Configuración de APIs</h2>
              <p className="text-sm text-muted-foreground">
                Añade tus propias claves API para usar diferentes proveedores de IA
              </p>
            </div>
          </div>
          <button
            onClick={onClose}
            className="p-2 rounded-lg hover:bg-muted transition-colors"
          >
            <X className="h-5 w-5 text-muted-foreground" />
          </button>
        </div>

        {/* Content */}
        <div className="p-4 overflow-y-auto max-h-[60vh]">
          {/* Security Options */}
          <div className="flex items-start gap-3 p-3 mb-4 rounded-lg bg-muted/50 border border-border">
            <AlertCircle className="h-5 w-5 text-primary shrink-0 mt-0.5" />
            <div className="flex-1">
              <div className="flex items-center justify-between mb-2">
                <p className="font-medium text-foreground">🔒 Seguridad de APIs</p>
                <button
                  onClick={clearAllApis}
                  className="text-xs text-destructive hover:underline"
                >
                  Borrar todas
                </button>
              </div>

              <div className="flex items-center justify-between">
                <p className="text-sm text-muted-foreground">
                  {saveToStorage
                    ? "Las APIs se guardan en tu navegador"
                    : "⚠️ Las APIs NO se guardan (se borran al cerrar)"}
                </p>
                <button
                  onClick={toggleSaveToStorage}
                  className={cn(
                    "px-3 py-1 text-xs rounded-full border transition-colors",
                    saveToStorage
                      ? "bg-green-500/10 border-green-500/30 text-green-500"
                      : "bg-yellow-500/10 border-yellow-500/30 text-yellow-500"
                  )}
                >
                  {saveToStorage ? "✓ Guardando" : "✗ No guardar"}
                </button>
              </div>
            </div>
          </div>

          {/* Configured Providers */}
          {providers.length > 0 && (
            <div className="mb-6">
              <h3 className="text-sm font-medium text-foreground mb-3">Proveedores Configurados</h3>
              <div className="space-y-2">
                {providers.map((provider) => (
                  <div
                    key={provider.id}
                    className={cn(
                      "rounded-lg border transition-all",
                      provider.isActive
                        ? "border-primary/50 bg-primary/5"
                        : "border-border bg-card"
                    )}
                  >
                    <div
                      className="flex items-center justify-between p-3 cursor-pointer"
                      onClick={() => setExpandedProvider(
                        expandedProvider === provider.id ? null : provider.id
                      )}
                    >
                      <div className="flex items-center gap-3">
                        <div className={cn(
                          "w-2 h-2 rounded-full",
                          provider.isActive && provider.apiKey ? "bg-green-500" : "bg-muted-foreground"
                        )} />
                        <span className="font-medium text-foreground">{provider.name}</span>
                        {provider.isActive && provider.apiKey && (
                          <span className="text-xs px-2 py-0.5 rounded-full bg-green-500/10 text-green-500">
                            Activo
                          </span>
                        )}
                      </div>
                      <ChevronDown className={cn(
                        "h-4 w-4 text-muted-foreground transition-transform",
                        expandedProvider === provider.id && "rotate-180"
                      )} />
                    </div>

                    {expandedProvider === provider.id && (
                      <div className="px-3 pb-3 space-y-3 border-t border-border pt-3">
                        {/* API Key Input */}
                        <div>
                          <label className="text-xs text-muted-foreground mb-1 block">
                            API Key
                          </label>
                          <div className="flex gap-2">
                            <div className="relative flex-1">
                              <input
                                type={showKeys[provider.id] ? "text" : "password"}
                                value={provider.apiKey}
                                onChange={(e) => handleUpdateProvider(provider.id, {
                                  apiKey: e.target.value,
                                  isActive: e.target.value.length > 0
                                })}
                                placeholder="sk-..."
                                className="w-full px-3 py-2 pr-10 rounded-lg border border-border bg-background text-foreground text-sm focus:outline-none focus:ring-2 focus:ring-primary/50"
                              />
                              <button
                                onClick={() => toggleKeyVisibility(provider.id)}
                                className="absolute right-2 top-1/2 -translate-y-1/2 p-1 hover:bg-muted rounded"
                              >
                                {showKeys[provider.id] ? (
                                  <EyeOff className="h-4 w-4 text-muted-foreground" />
                                ) : (
                                  <Eye className="h-4 w-4 text-muted-foreground" />
                                )}
                              </button>
                            </div>
                          </div>
                        </div>

                        {/* Base URL (optional) */}
                        {provider.baseUrl && (
                          <div>
                            <label className="text-xs text-muted-foreground mb-1 block">
                              Base URL
                            </label>
                            <input
                              type="text"
                              value={provider.baseUrl}
                              onChange={(e) => handleUpdateProvider(provider.id, { baseUrl: e.target.value })}
                              className="w-full px-3 py-2 rounded-lg border border-border bg-background text-foreground text-sm focus:outline-none focus:ring-2 focus:ring-primary/50"
                            />
                          </div>
                        )}

                        {/* Detect Models Button */}
                        <div>
                          <button
                            onClick={() => fetchModelsForProvider(provider.id)}
                            disabled={!provider.apiKey || loadingModels === provider.id}
                            className="flex items-center gap-2 px-3 py-2 text-sm bg-primary/10 text-primary border border-primary/30 rounded-lg hover:bg-primary/20 transition-colors disabled:opacity-50 disabled:cursor-not-allowed w-full justify-center"
                          >
                            {loadingModels === provider.id ? (
                              <>
                                <Loader2 className="h-4 w-4 animate-spin" />
                                Detectando modelos...
                              </>
                            ) : (
                              <>
                                <RefreshCw className="h-4 w-4" />
                                🔍 Detectar Modelos Disponibles
                              </>
                            )}
                          </button>
                          {modelError && expandedProvider === provider.id && (
                            <p className="text-xs text-destructive mt-1">{modelError}</p>
                          )}
                        </div>

                        {/* Models Selection */}
                        <div>
                          <div className="flex items-center justify-between mb-2">
                            <label className="text-xs text-muted-foreground">
                              Modelos Disponibles ({provider.models.length})
                            </label>
                            <div className="flex gap-2">
                              <button
                                onClick={() => {
                                  handleUpdateProvider(provider.id, {
                                    enabledModels: provider.models
                                  });
                                }}
                                className="text-xs text-primary hover:underline"
                              >
                                Todos
                              </button>
                              <button
                                onClick={() => {
                                  handleUpdateProvider(provider.id, {
                                    enabledModels: []
                                  });
                                }}
                                className="text-xs text-muted-foreground hover:underline"
                              >
                                Ninguno
                              </button>
                            </div>
                          </div>
                          <div className="space-y-1 max-h-48 overflow-y-auto p-2 bg-background rounded border border-border">
                            {provider.models.map((model) => {
                              const isEnabled = provider.enabledModels?.includes(model) ?? true;
                              return (
                                <label
                                  key={model}
                                  className="flex items-center gap-2 p-2 rounded hover:bg-muted cursor-pointer transition-colors"
                                >
                                  <input
                                    type="checkbox"
                                    checked={isEnabled}
                                    onChange={(e) => {
                                      const currentEnabled = provider.enabledModels || provider.models;
                                      const newEnabled = e.target.checked
                                        ? [...currentEnabled, model]
                                        : currentEnabled.filter(m => m !== model);
                                      handleUpdateProvider(provider.id, {
                                        enabledModels: newEnabled
                                      });
                                    }}
                                    className="w-4 h-4 rounded border-border text-primary focus:ring-2 focus:ring-primary/50"
                                  />
                                  <span className="text-xs text-foreground flex-1">{model}</span>
                                  {isEnabled && (
                                    <Check className="h-3 w-3 text-green-500" />
                                  )}
                                </label>
                              );
                            })}
                          </div>
                          <p className="text-xs text-muted-foreground mt-1">
                            ✓ {provider.enabledModels?.length || provider.models.length} de {provider.models.length} modelos habilitados
                          </p>
                        </div>

                        {/* Old Models Display (hidden) */}
                        <div className="hidden">
                          <div className="flex flex-wrap gap-1 max-h-32 overflow-y-auto">
                            {provider.models.map((model) => (
                              <span
                                key={model}
                                className="text-xs px-2 py-1 rounded bg-muted text-muted-foreground"
                              >
                                {model.split("/").pop()}
                              </span>
                            ))}
                          </div>
                        </div>

                        {/* Actions */}
                        <div className="flex justify-end gap-2 pt-2">
                          <button
                            onClick={() => handleRemoveProvider(provider.id)}
                            className="flex items-center gap-1 px-3 py-1.5 text-sm text-destructive hover:bg-destructive/10 rounded-lg transition-colors"
                          >
                            <Trash2 className="h-4 w-4" />
                            Eliminar
                          </button>
                        </div>
                      </div>
                    )}
                  </div>
                ))}
              </div>
            </div>
          )}

          {/* Available Providers */}
          <div>
            <h3 className="text-sm font-medium text-foreground mb-3">Añadir Proveedor</h3>
            <div className="grid grid-cols-2 sm:grid-cols-3 gap-2">
              {DEFAULT_PROVIDERS.map((provider) => {
                const isAdded = providers.some(p => p.id === provider.id);
                return (
                  <button
                    key={provider.id}
                    onClick={() => handleAddProvider(provider)}
                    className={cn(
                      "flex items-center gap-2 p-3 rounded-lg border transition-all text-left",
                      isAdded
                        ? "border-primary/30 bg-primary/5"
                        : "border-border hover:border-primary/50 hover:bg-muted/50"
                    )}
                  >
                    <Zap className={cn(
                      "h-4 w-4",
                      isAdded ? "text-primary" : "text-muted-foreground"
                    )} />
                    <span className={cn(
                      "text-sm font-medium",
                      isAdded ? "text-primary" : "text-foreground"
                    )}>
                      {provider.name}
                    </span>
                    {isAdded && (
                      <Check className="h-4 w-4 text-primary ml-auto" />
                    )}
                  </button>
                );
              })}

              {/* Add Custom */}
              <button
                onClick={() => setShowAddCustom(true)}
                className="flex items-center gap-2 p-3 rounded-lg border border-dashed border-border hover:border-primary/50 hover:bg-muted/50 transition-all"
              >
                <Plus className="h-4 w-4 text-muted-foreground" />
                <span className="text-sm text-muted-foreground">Personalizado</span>
              </button>
            </div>
          </div>

          {/* Custom Provider Form */}
          {showAddCustom && (
            <div className="mt-4 p-4 rounded-lg border border-border bg-muted/30">
              <h4 className="text-sm font-medium text-foreground mb-3">Añadir Proveedor Personalizado</h4>
              <div className="space-y-3">
                <input
                  type="text"
                  value={customProvider.name}
                  onChange={(e) => setCustomProvider(prev => ({ ...prev, name: e.target.value }))}
                  placeholder="Nombre del proveedor"
                  className="w-full px-3 py-2 rounded-lg border border-border bg-background text-foreground text-sm focus:outline-none focus:ring-2 focus:ring-primary/50"
                />
                <input
                  type="text"
                  value={customProvider.baseUrl}
                  onChange={(e) => setCustomProvider(prev => ({ ...prev, baseUrl: e.target.value }))}
                  placeholder="Base URL (ej: https://api.example.com/v1)"
                  className="w-full px-3 py-2 rounded-lg border border-border bg-background text-foreground text-sm focus:outline-none focus:ring-2 focus:ring-primary/50"
                />
                <input
                  type="password"
                  value={customProvider.apiKey}
                  onChange={(e) => setCustomProvider(prev => ({ ...prev, apiKey: e.target.value }))}
                  placeholder="API Key"
                  className="w-full px-3 py-2 rounded-lg border border-border bg-background text-foreground text-sm focus:outline-none focus:ring-2 focus:ring-primary/50"
                />
                <input
                  type="text"
                  value={customProvider.models}
                  onChange={(e) => setCustomProvider(prev => ({ ...prev, models: e.target.value }))}
                  placeholder="Modelos (separados por coma)"
                  className="w-full px-3 py-2 rounded-lg border border-border bg-background text-foreground text-sm focus:outline-none focus:ring-2 focus:ring-primary/50"
                />
                <div className="flex justify-end gap-2">
                  <button
                    onClick={() => setShowAddCustom(false)}
                    className="px-3 py-1.5 text-sm text-muted-foreground hover:bg-muted rounded-lg transition-colors"
                  >
                    Cancelar
                  </button>
                  <button
                    onClick={handleAddCustomProvider}
                    disabled={!customProvider.name || !customProvider.apiKey}
                    className="flex items-center gap-1 px-3 py-1.5 text-sm bg-primary text-primary-foreground rounded-lg hover:bg-primary/90 transition-colors disabled:opacity-50 disabled:cursor-not-allowed"
                  >
                    <Save className="h-4 w-4" />
                    Guardar
                  </button>
                </div>
              </div>
            </div>
          )}
        </div>

        {/* Footer */}
        <div className="flex items-center justify-between p-4 border-t border-border bg-muted/30">
          <div className="flex items-center gap-4">
            <p className="text-xs text-muted-foreground">
              {providers.filter(p => p.isActive && p.apiKey).length} proveedor(es) activo(s)
            </p>
            {hasChanges && (
              <div className="flex items-center gap-1 text-xs text-amber-600 dark:text-amber-400">
                <AlertCircle className="h-3 w-3" />
                <span>Tienes cambios sin guardar</span>
              </div>
            )}
          </div>
          <div className="flex gap-2">
            <button
              onClick={() => {
                setProviders(originalProviders);
                setHasChanges(false);
              }}
              disabled={!hasChanges}
              className="px-3 py-2 text-sm font-medium text-muted-foreground hover:bg-muted rounded-lg transition-colors disabled:opacity-50 disabled:cursor-not-allowed"
            >
              Cancelar
            </button>
            <button
              onClick={applyChanges}
              disabled={!hasChanges}
              className="flex items-center gap-2 px-4 py-2 text-sm font-medium bg-primary text-primary-foreground rounded-lg hover:bg-primary/90 transition-colors disabled:opacity-50 disabled:cursor-not-allowed"
            >
              <Save className="h-4 w-4" />
              {hasChanges ? "Guardar Cambios" : "Listo"}
            </button>
          </div>
        </div>
      </div>
    </div>
  );
}

// Hook para usar los proveedores en otros componentes
export function useApiProviders() {
  const [providers, setProviders] = useState<ApiProvider[]>([]);

  useEffect(() => {
    const saved = localStorage.getItem("atp-api-providers");
    if (saved) {
      try {
        setProviders(JSON.parse(saved));
      } catch (e) {
        console.error("Error loading providers:", e);
      }
    }
  }, []);

  const getActiveProviders = () => providers.filter(p => p.isActive && p.apiKey);

  const getProviderByType = (type: ApiProvider["type"]) =>
    providers.find(p => p.type === type && p.isActive && p.apiKey);

  return { providers, getActiveProviders, getProviderByType };
}
