"use client";

/**
 * Connection Status Indicator v0.8.0
 * ================================
 * Indicador de conexión en tiempo real con animaciones
 * y estados visuales detallados
 */

import { useState, useEffect } from "react";
import { cn } from "@/lib/utils";
import {
  Wifi,
  WifiOff,
  AlertTriangle,
  Loader2,
  CheckCircle2,
  XCircle,
  Activity,
  Server,
  Cloud,
  CloudOff,
} from "lucide-react";

export type ConnectionStatus = "connected" | "connecting" | "disconnected" | "error" | "reconnecting";

interface ConnectionStatusProps {
  status?: ConnectionStatus;
  latency?: number;
  showDetails?: boolean;
  size?: "sm" | "md" | "lg";
  position?: "header" | "floating";
  className?: string;
}

const statusConfig = {
  connected: {
    icon: Wifi,
    color: "text-green-500",
    bgColor: "bg-green-500/10",
    borderColor: "border-green-500/30",
    label: "Conectado",
    description: "Conexión estable",
  },
  connecting: {
    icon: Loader2,
    color: "text-yellow-500",
    bgColor: "bg-yellow-500/10",
    borderColor: "border-yellow-500/30",
    label: "Conectando...",
    description: "Estableciendo conexión",
  },
  disconnected: {
    icon: WifiOff,
    color: "text-red-500",
    bgColor: "bg-red-500/10",
    borderColor: "border-red-500/30",
    label: "Desconectado",
    description: "Sin conexión al servidor",
  },
  error: {
    icon: XCircle,
    color: "text-red-600",
    bgColor: "bg-red-600/10",
    borderColor: "border-red-600/30",
    label: "Error",
    description: "Error de conexión",
  },
  reconnecting: {
    icon: Activity,
    color: "text-orange-500",
    bgColor: "bg-orange-500/10",
    borderColor: "border-orange-500/30",
    label: "Reconectando...",
    description: "Intentando reconectar",
  },
};

const sizeConfig = {
  sm: {
    container: "w-6 h-6",
    icon: "h-3 w-3",
    text: "text-xs",
  },
  md: {
    container: "w-8 h-8",
    icon: "h-4 w-4",
    text: "text-sm",
  },
  lg: {
    container: "w-10 h-10",
    icon: "h-5 w-5",
    text: "text-base",
  },
};

export function ConnectionStatus({
  status = "disconnected",
  latency,
  showDetails = false,
  size = "md",
  position = "header",
  className,
}: ConnectionStatusProps) {
  const [currentStatus, setCurrentStatus] = useState<ConnectionStatus>(status);
  const [currentLatency, setCurrentLatency] = useState<number | undefined>(latency);
  const [isPulsing, setIsPulsing] = useState(false);

  // Simular cambios de estado para demostración
  useEffect(() => {
    if (status !== currentStatus) {
      setCurrentStatus(status);
      
      // Efectos visuales según el estado
      if (status === "connecting" || status === "reconnecting") {
        setIsPulsing(true);
      } else {
        setIsPulsing(false);
      }
    }
  }, [status, currentStatus]);

  // Actualizar latencia
  useEffect(() => {
    if (latency !== undefined) {
      setCurrentLatency(latency);
    }
  }, [latency]);

  const config = statusConfig[currentStatus];
  const sizeCfg = sizeConfig[size];
  const Icon = config.icon;

  // Determinar color de latencia
  const getLatencyColor = (lat: number) => {
    if (lat < 50) return "text-green-500";
    if (lat < 150) return "text-yellow-500";
    return "text-red-500";
  };

  // Componente principal
  const StatusIndicator = () => (
    <div
      className={cn(
        "relative flex items-center justify-center rounded-full border transition-all duration-300",
        sizeCfg.container,
        config.bgColor,
        config.borderColor,
        isPulsing && "animate-pulse",
        className
      )}
    >
      <Icon
        className={cn(
          sizeCfg.icon,
          config.color,
          currentStatus === "connecting" && "animate-spin",
          currentStatus === "reconnecting" && "animate-pulse"
        )}
      />
      
      {/* Indicador de actividad */}
      {currentStatus === "connected" && (
        <div className="absolute -bottom-1 -right-1 w-2 h-2 bg-green-500 rounded-full animate-ping" />
      )}
      
      {/* Tooltip */}
      {showDetails && (
        <div className="absolute bottom-full left-1/2 transform -translate-x-1/2 mb-2 px-2 py-1 bg-background border border-border rounded shadow-lg whitespace-nowrap z-50">
          <div className="flex items-center gap-2">
            <span className={cn("text-xs font-medium", config.color)}>
              {config.label}
            </span>
            {currentLatency !== undefined && (
              <span className={cn("text-xs", getLatencyColor(currentLatency))}>
                {currentLatency}ms
              </span>
            )}
          </div>
          <div className="text-xs text-muted-foreground mt-1">
            {config.description}
          </div>
        </div>
      )}
    </div>
  );

  // Versión flotante
  if (position === "floating") {
    return (
      <div className="fixed top-4 right-4 z-50">
        <StatusIndicator />
      </div>
    );
  }

  // Versión header (inline)
  return <StatusIndicator />;
}

// Hook para monitoreo de conexión
export function useConnectionStatus() {
  const [status, setStatus] = useState<ConnectionStatus>("disconnected");
  const [latency, setLatency] = useState<number | undefined>();
  const [lastCheck, setLastCheck] = useState<Date>(new Date());

  const checkConnection = async () => {
    try {
      const startTime = Date.now();
      const response = await fetch("/api/health", {
        method: "GET",
        cache: "no-cache",
      });
      
      const endTime = Date.now();
      const responseLatency = endTime - startTime;
      
      if (response.ok) {
        setStatus("connected");
        setLatency(responseLatency);
      } else {
        setStatus("error");
        setLatency(undefined);
      }
    } catch (error) {
      setStatus("disconnected");
      setLatency(undefined);
    }
    
    setLastCheck(new Date());
  };

  useEffect(() => {
    // Verificar conexión inicial
    checkConnection();

    // Verificar conexión periódicamente
    const interval = setInterval(checkConnection, 5000); // 5 segundos

    return () => clearInterval(interval);
  }, []);

  return {
    status,
    latency,
    lastCheck,
    checkConnection,
    isConnected: status === "connected",
  };
}

// Componente de conexión detallada para panel
export function DetailedConnectionStatus() {
  const { status, latency, lastCheck, isConnected } = useConnectionStatus();

  return (
    <div className="flex items-center gap-3 p-3 rounded-lg border bg-card">
      <ConnectionStatus status={status} latency={latency} showDetails={false} size="md" />
      
      <div className="flex-1 min-w-0">
        <div className="flex items-center justify-between">
          <span className="text-sm font-medium">
            {statusConfig[status].label}
          </span>
          {latency !== undefined && (
            <span className={cn("text-xs", getLatencyColor(latency))}>
              {latency}ms
            </span>
          )}
        </div>
        <div className="text-xs text-muted-foreground">
          Última verificación: {lastCheck.toLocaleTimeString()}
        </div>
      </div>
      
      <div className="flex items-center gap-2">
        {isConnected ? (
          <>
            <CheckCircle2 className="h-4 w-4 text-green-500" />
            <Server className="h-4 w-4 text-muted-foreground" />
          </>
        ) : (
          <>
            <CloudOff className="h-4 w-4 text-red-500" />
            <AlertTriangle className="h-4 w-4 text-yellow-500" />
          </>
        )}
      </div>
    </div>
  );
}

// Componente minimal para header
export function MinimalConnectionStatus() {
  const { status, latency } = useConnectionStatus();
  
  return (
    <div className="flex items-center gap-2">
      <ConnectionStatus 
        status={status} 
        latency={latency} 
        showDetails={true} 
        size="sm" 
      />
      <span className="text-xs text-muted-foreground hidden sm:inline">
        {statusConfig[status].label}
      </span>
    </div>
  );
}

function getLatencyColor(lat: number): string {
  if (lat < 50) return "text-green-500";
  if (lat < 150) return "text-yellow-500";
  return "text-red-500";
}

export default ConnectionStatus;
