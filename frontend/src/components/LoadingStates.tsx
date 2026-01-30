"use client";

/**
 * Loading States v0.8.0
 * ===================
 * Componentes de carga con animaciones y estados visuales mejorados
 */

import { cn } from "@/lib/utils";
import { Loader2, Brain, Wifi, Cloud, AlertTriangle } from "lucide-react";

export type LoadingState = "idle" | "loading" | "success" | "error" | "connecting" | "processing";

interface LoadingStateProps {
  state: LoadingState;
  message?: string;
  size?: "sm" | "md" | "lg";
  showIcon?: boolean;
  className?: string;
}

const sizeConfig = {
  sm: {
    container: "w-8 h-8",
    icon: "h-4 w-4",
    text: "text-xs",
  },
  md: {
    container: "w-12 h-12",
    icon: "h-6 w-6",
    text: "text-sm",
  },
  lg: {
    container: "w-16 h-16",
    icon: "h-8 w-8",
    "text": "text-base",
  },
};

const stateConfig = {
  idle: {
    color: "text-muted-foreground",
    bgColor: "bg-muted/30",
    borderColor: "border-muted/50",
    icon: Brain,
    defaultMessage: "Listo para comenzar",
    animate: false,
  },
  loading: {
    color: "text-primary",
    bgColor: "bg-primary/10",
    borderColor: "border-primary/30",
    icon: Loader2,
    defaultMessage: "Procesando...",
    animate: true,
  },
  connecting: {
    color: "text-yellow-500",
    bgColor: "bg-yellow-500/10",
    borderColor: "border-yellow-500/30",
    icon: Wifi,
    defaultMessage: "Conectando...",
    animate: true,
  },
  processing: {
    color: "text-blue-500",
    bgColor: "bg-blue-500/10",
    borderColor: "border-blue-500/30",
    icon: Cloud,
    defaultMessage: "Procesando tarea...",
    animate: true,
  },
  success: {
    color: "text-green-500",
    bgColor: "bg-green-500/10",
    borderColor: "border-green-500/30",
    icon: Wifi,
    defaultMessage: "Completado",
    animate: false,
  },
  error: {
    color: "text-red-500",
    bgColor: "bg-red-500/10",
    borderColor: "border-red-500/30",
    icon: AlertTriangle,
    defaultMessage: "Error",
    animate: false,
  },
};

export function LoadingState({
  state,
  message,
  size = "md",
  showIcon = true,
  className,
}: LoadingStateProps) {
  const config = stateConfig[state];
  const sizeCfg = sizeConfig[size];
  const Icon = config.icon;

  return (
    <div
      className={cn(
        "flex items-center justify-center rounded-full border transition-all duration-300",
        sizeCfg.container,
        config.bgColor,
        config.borderColor,
        config.animate && "animate-pulse",
        className
      )}
    >
      {showIcon && (
        <Icon
          className={cn(
            sizeCfg.icon,
            config.color,
            state === "loading" && "animate-spin",
            state === "connecting" && "animate-bounce",
            state === "processing" && "animate-pulse"
          )}
        />
      )}
      
      {message && (
        <span
          className={cn(
            "font-medium",
            sizeCfg.text,
            config.color,
            "truncate max-w-[100px]"
          )}
        >
          {message}
        </span>
      )}
    </div>
  );
}

/* Componente de carga con texto */
export function LoadingText({
  state = "loading",
  message,
  size = "md",
  className,
}: {
  state?: LoadingState;
  message?: string;
  size?: "sm" | "md" | "lg";
  className?: string;
}) {
  const config = stateConfig[state];
  const sizeCfg = sizeConfig[size];

  return (
    <div
      className={cn(
        "flex items-center gap-2",
        "transition-all duration-300",
        className
      )}
    >
      <div
        className={cn(
          "rounded-full border",
          sizeCfg.container,
          config.bgColor,
          config.borderColor,
          config.animate && "animate-pulse"
        )}
      >
        <Loader2
          className={cn(
            sizeCfg.icon,
            config.color,
            state === "loading" && "animate-spin",
            state === "connecting" && "animate-bounce",
            state === "processing" && "animate-pulse"
          )}
        />
      </div>
      <span
        className={cn(
          "font-medium",
          sizeCfg.text,
          config.color
        )}
      >
        {message || config.defaultMessage}
      </span>
    </div>
  );
}

/* Skeleton loader para contenido */
export function SkeletonLoader({
  lines = 3,
  className,
}: {
  lines?: number;
  className?: string;
}) {
  return (
    <div className={cn("space-y-2", className)}>
      {Array.from({ length: lines }).map((_, index) => (
        <div
          key={index}
          className={cn(
            "h-4 bg-muted rounded animate-pulse",
            index === lines - 1 && "w-3/4"
          )}
        />
      ))}
    </div>
  );
}

/* Card skeleton loader */
export function CardSkeleton({ className }: { className?: string }) {
  return (
    <div
      className={cn(
        "rounded-lg border bg-card p-4 space-y-3 animate-fade-in",
        className
      )}
    >
      <div className="flex items-center space-x-3">
        <div className="w-10 h-10 bg-muted rounded-full animate-pulse" />
        <div className="flex-1 space-y-2">
          <div className="h-4 bg-muted rounded w-3/4 animate-pulse" />
          <div className="h-3 bg-muted rounded w-1/2 animate-pulse" />
        </div>
      </div>
      <div className="space-y-2">
        <div className="h-3 bg-muted rounded animate-pulse" />
        <div className="h-3 bg-muted rounded w-5/6 animate-pulse" />
        <div className="h-3 bg-muted rounded w-4/5 animate-pulse" />
      </div>
    </div>
  );
}

/* Inline loader */
export function InlineLoader({
  size = "sm",
  className,
}: {
  size?: "sm" | "md" | "lg";
  className?: string;
}) {
  const sizeCfg = sizeConfig[size];

  return (
    <div
      className={cn(
        "inline-flex items-center gap-2",
        "transition-all duration-200",
        className
      )}
    >
      <Loader2
        className={cn(
          sizeCfg.icon,
          "text-primary",
          "animate-spin"
        )}
      />
      <span className={cn("text-sm text-muted-foreground")}>
        Cargando...
      </span>
    </div>
  );
}

/* Progress loader */
export function ProgressLoader({
  progress = 0,
  size = "md",
  showPercentage = true,
  className,
}: {
  progress?: number;
  size?: "sm" | "md" | "lg";
  showPercentage?: boolean;
  className?: string;
}) {
  const sizeConfig = {
    sm: { height: "h-1", text: "text-xs" },
    md: { height: "h-2", text: "text-sm" },
    lg: { height: "h-3", text: "text-base" },
  };

  const currentSize = sizeConfig[size];

  return (
    <div className={cn("w-full space-y-2", className)}>
      <div className="flex items-center justify-between text-sm text-muted-foreground">
        <span>Progreso</span>
        {showPercentage && (
          <span className="font-mono">{Math.round(progress)}%</span>
        )}
      </div>
      <div className="w-full bg-muted rounded-full overflow-hidden">
        <div
          className={cn(
            "h-full bg-primary transition-all duration-300 ease-out",
            currentSize.height
          )}
          style={{ width: `${progress}%` }}
        />
      </div>
    </div>
  );
}

/* Staggered loading dots */
export function DotsLoader({
  dots = 3,
  size = "sm",
  className,
}: {
  dots?: number;
  size?: "sm" | "md" | "lg";
  className?: string;
}) {
  const sizeConfig = {
    sm: "w-2 h-2",
    md: "w-3 h-3",
    lg: "w-4 h-4",
  };

  const currentSize = sizeConfig[size];

  return (
    <div className={cn("flex items-center gap-2", className)}>
      {Array.from({ length: dots }).map((_, index) => (
        <div
          key={index}
          className={cn(
            currentSize,
            "rounded-full bg-primary",
            "animate-pulse",
            index === 0 && "animate-delay-0",
            index === 1 && "animate-delay-150",
            index === 2 && "animate-delay-300"
          )}
        />
      ))}
    </div>
  );
}

/* Pulse loader */
export function PulseLoader({
  size = "md",
  className,
}: {
  size?: "sm" | "md" | "lg";
  className?: string;
}) {
  const sizeConfig = {
    sm: "w-6 h-6",
    md: "w-8 h-8",
    lg: "w-10 h-10",
  };

  const currentSize = sizeConfig[size];

  return (
    <div
      className={cn(
        "rounded-full bg-primary animate-ping",
        currentSize,
        className
      )}
    />
  );
}

/* Wave loader */
export function WaveLoader({
  size = "md",
  className,
}: {
  size?: "sm" | "md" | "lg";
  className?: string;
}) {
  const sizeConfig = {
    sm: "w-6 h-4",
    md: "w-8 h-6",
    lg: "w-12 h-8",
  };

  const currentSize = sizeConfig[size];

  return (
    <div className={cn("relative", currentSize)}>
      <div className="absolute inset-0 bg-primary rounded-full animate-pulse" />
      <div className="absolute inset-0 bg-primary rounded-full animate-ping animation-delay-200" />
      <div className="absolute inset-0 bg-primary rounded-full animate-ping animation-delay-400" />
    </div>
  );
}

/* Componente de carga con fondo */
export function BackdropLoader({
  message = "Cargando...",
  overlay = true,
  className,
}: {
  message?: string;
  overlay?: boolean;
  className?: string;
}) {
  return (
    <div
      className={cn(
        "fixed inset-0 bg-background/80 backdrop-blur-sm flex items-center justify-center z-50",
        overlay && "bg-black/20"
      )}
    >
      <div className="text-center space-y-4">
        <div className="animate-bounce-in">
          <Brain className="h-12 w-12 text-primary mx-auto animate-spin" />
        </div>
        <p className="text-lg font-medium text-foreground">
          {message}
        </p>
        <div className="flex justify-center gap-2">
          <div className="w-2 h-2 bg-primary rounded-full animate-pulse" />
          <div className="w-2 h-2 bg-primary rounded-full animate-pulse animation-delay-200" />
          <div className="w-2 h-2 bg-primary rounded-full animate-pulse animation-delay-400" />
        </div>
      </div>
    </div>
  );
}

/* Componente de carga minimal */
export function MinimalLoader({
  size = "sm",
  className,
}: {
  size?: "sm" | "md" | "lg";
  className?: string;
}) {
  const sizeConfig = {
    sm: "w-4 h-4",
    md: "w-6 h-6",
    lg: "w-8 h-8",
  };

  const currentSize = sizeConfig[size];

  return <div className={cn("rounded-full bg-primary animate-pulse", currentSize, className)} />;
}
