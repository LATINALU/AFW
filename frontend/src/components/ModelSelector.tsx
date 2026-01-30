"use client";

import { useState, useEffect } from "react";
import { Button } from "@/components/ui/button";
import { Card, CardContent, CardHeader, CardTitle } from "@/components/ui/card";
import { Input } from "@/components/ui/input";
import { Select, SelectContent, SelectItem, SelectTrigger, SelectValue } from "@/components/ui/select";
import { Badge } from "@/components/ui/badge";
import { ScrollArea } from "@/components/ui/scroll-area";
import { 
  Loader2, 
  Check, 
  AlertCircle, 
  Cpu, 
  Zap,
  RefreshCw,
  Settings2,
  Brain
} from "lucide-react";

interface AvailableModel {
  id: string;
  name: string;
  description: string;
  provider: string;
}

interface AgentModelConfig {
  agentName: string;
  modelId: string;
}

interface ModelSelectorProps {
  selectedAgents: string[];
  onAgentModelsChange: (configs: AgentModelConfig[]) => void;
}

const PROVIDERS = [
  { id: "groq", name: "Groq", description: "Ultra rápido, Llama 3.3" },
  { id: "openai", name: "OpenAI", description: "GPT-4o, o1" },
  { id: "deepseek", name: "DeepSeek", description: "Económico, potente" },
  { id: "together", name: "Together AI", description: "Open source" },
  { id: "openrouter", name: "OpenRouter", description: "Múltiples proveedores" },
  { id: "mistral", name: "Mistral", description: "Europeo, multilingüe" },
  { id: "ollama", name: "Ollama", description: "Local, privado" },
];

export function ModelSelector({ selectedAgents, onAgentModelsChange }: ModelSelectorProps) {
  const [apiKey, setApiKey] = useState("");
  const [provider, setProvider] = useState("groq");
  const [baseUrl, setBaseUrl] = useState("");
  const [isLoading, setIsLoading] = useState(false);
  const [error, setError] = useState<string | null>(null);
  const [availableModels, setAvailableModels] = useState<AvailableModel[]>([]);
  const [agentModels, setAgentModels] = useState<Record<string, string>>({});
  const [isConnected, setIsConnected] = useState(false);

  // Cargar configuración guardada
  useEffect(() => {
    const saved = localStorage.getItem("atp_api_config");
    if (saved) {
      const config = JSON.parse(saved);
      setApiKey(config.apiKey || "");
      setProvider(config.provider || "groq");
      setBaseUrl(config.baseUrl || "");
    }
    
    const savedModels = localStorage.getItem("atp_agent_models");
    if (savedModels) {
      setAgentModels(JSON.parse(savedModels));
    }
  }, []);

  // Guardar configuración de agentes
  useEffect(() => {
    if (Object.keys(agentModels).length > 0) {
      localStorage.setItem("atp_agent_models", JSON.stringify(agentModels));
      
      // Notificar cambios
      const configs = Object.entries(agentModels).map(([agentName, modelId]) => ({
        agentName,
        modelId,
      }));
      onAgentModelsChange(configs);
    }
  }, [agentModels, onAgentModelsChange]);

  const fetchModels = async () => {
    if (!apiKey.trim()) {
      setError("Ingresa tu API key");
      return;
    }

    setIsLoading(true);
    setError(null);

    try {
      const response = await fetch("/api/fetch-models", {
        method: "POST",
        headers: { "Content-Type": "application/json" },
        body: JSON.stringify({
          api_type: provider,
          api_key: apiKey,
          base_url: baseUrl || null,
        }),
      });

      const data = await response.json();

      if (data.success && data.models.length > 0) {
        setAvailableModels(data.models);
        setIsConnected(true);
        
        // Guardar configuración
        localStorage.setItem("atp_api_config", JSON.stringify({
          apiKey,
          provider,
          baseUrl,
        }));

        // Asignar modelo por defecto a agentes sin configurar
        const defaultModel = data.models[0].id;
        const newAgentModels = { ...agentModels };
        selectedAgents.forEach(agent => {
          if (!newAgentModels[agent]) {
            newAgentModels[agent] = defaultModel;
          }
        });
        setAgentModels(newAgentModels);
      } else {
        setError(data.error || "No se encontraron modelos");
        setIsConnected(false);
      }
    } catch (err) {
      setError("Error de conexión. Verifica el backend.");
      setIsConnected(false);
    } finally {
      setIsLoading(false);
    }
  };

  const setModelForAgent = (agentName: string, modelId: string) => {
    setAgentModels(prev => ({
      ...prev,
      [agentName]: modelId,
    }));
  };

  const setModelForAll = (modelId: string) => {
    const newModels: Record<string, string> = {};
    selectedAgents.forEach(agent => {
      newModels[agent] = modelId;
    });
    setAgentModels(newModels);
  };

  return (
    <Card className="border-primary/30">
      <CardHeader className="pb-3">
        <CardTitle className="flex items-center gap-2 text-lg">
          <Settings2 className="h-5 w-5 text-primary" />
          Configurar IA por Agente
        </CardTitle>
      </CardHeader>
      <CardContent className="space-y-4">
        {/* Paso 1: Conectar API */}
        <div className="space-y-3 p-3 bg-muted/30 rounded-lg">
          <span className="text-sm font-semibold">1️⃣ Conectar API</span>
          
          <Select value={provider} onValueChange={setProvider}>
            <SelectTrigger>
              <SelectValue placeholder="Selecciona proveedor" />
            </SelectTrigger>
            <SelectContent>
              {PROVIDERS.map((p) => (
                <SelectItem key={p.id} value={p.id}>
                  <div className="flex items-center gap-2">
                    <Cpu className="h-4 w-4" />
                    <span>{p.name}</span>
                    <span className="text-xs text-muted-foreground">- {p.description}</span>
                  </div>
                </SelectItem>
              ))}
            </SelectContent>
          </Select>

          <Input
            type="password"
            placeholder="API Key"
            value={apiKey}
            onChange={(e) => setApiKey(e.target.value)}
          />

          {provider === "ollama" && (
            <Input
              placeholder="URL (default: http://localhost:11434)"
              value={baseUrl}
              onChange={(e) => setBaseUrl(e.target.value)}
            />
          )}

          <Button 
            onClick={fetchModels} 
            disabled={isLoading || !apiKey.trim()}
            className="w-full"
          >
            {isLoading ? (
              <>
                <Loader2 className="h-4 w-4 mr-2 animate-spin" />
                Conectando...
              </>
            ) : isConnected ? (
              <>
                <RefreshCw className="h-4 w-4 mr-2" />
                Actualizar Modelos
              </>
            ) : (
              <>
                <Zap className="h-4 w-4 mr-2" />
                Conectar y Detectar Modelos
              </>
            )}
          </Button>

          {error && (
            <div className="flex items-center gap-2 text-destructive text-sm">
              <AlertCircle className="h-4 w-4" />
              {error}
            </div>
          )}

          {isConnected && (
            <div className="flex items-center gap-2 text-green-500 text-sm">
              <Check className="h-4 w-4" />
              Conectado - {availableModels.length} modelos disponibles
            </div>
          )}
        </div>

        {/* Paso 2: Asignar modelos a agentes */}
        {isConnected && availableModels.length > 0 && (
          <div className="space-y-3">
            <div className="flex items-center justify-between">
              <span className="text-sm font-semibold">2️⃣ Asignar IA a cada Agente</span>
              <Select onValueChange={setModelForAll}>
                <SelectTrigger className="w-48">
                  <SelectValue placeholder="Aplicar a todos" />
                </SelectTrigger>
                <SelectContent>
                  {availableModels.map((model) => (
                    <SelectItem key={model.id} value={model.id}>
                      {model.name.split("/").pop()}
                    </SelectItem>
                  ))}
                </SelectContent>
              </Select>
            </div>

            <ScrollArea className="h-64 pr-3">
              <div className="space-y-2">
                {selectedAgents.map((agent) => (
                  <div 
                    key={agent}
                    className="flex items-center justify-between p-2 bg-card border border-border rounded-lg"
                  >
                    <div className="flex items-center gap-2">
                      <Brain className="h-4 w-4 text-primary" />
                      <span className="text-sm font-medium">
                        {agent.replace(/_/g, " ").replace(/agent/i, "").trim()}
                      </span>
                    </div>
                    
                    <Select 
                      value={agentModels[agent] || ""} 
                      onValueChange={(value: string) => setModelForAgent(agent, value)}
                    >
                      <SelectTrigger className="w-56">
                        <SelectValue placeholder="Seleccionar modelo" />
                      </SelectTrigger>
                      <SelectContent>
                        {availableModels.map((model) => (
                          <SelectItem key={model.id} value={model.id}>
                            <div className="flex flex-col">
                              <span className="font-medium">{model.name.split("/").pop()}</span>
                              <span className="text-xs text-muted-foreground">{model.description}</span>
                            </div>
                          </SelectItem>
                        ))}
                      </SelectContent>
                    </Select>
                  </div>
                ))}
              </div>
            </ScrollArea>

            {selectedAgents.length === 0 && (
              <p className="text-sm text-muted-foreground text-center py-4">
                Selecciona agentes en el sidebar para configurar sus modelos
              </p>
            )}
          </div>
        )}
      </CardContent>
    </Card>
  );
}
