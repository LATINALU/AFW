# 🎨 AFW v0.5.0 - Plan de Integración EldoraUI

> **Actualización de UI/UX** con componentes modernos inspirados en shadcn/ui, Aceternity UI y Magic UI

## 📋 Resumen

**Librería:** [EldoraUI](https://www.eldoraui.site/)  
**Versión:** Latest  
**Objetivo:** Modernizar la interfaz de AFW con componentes elegantes y animaciones fluidas

---

## 🎯 ¿Por qué EldoraUI?

| Característica | Beneficio |
|----------------|-----------|
| **Copy-paste components** | Rápida implementación |
| **Inspirado en shadcn/ui** | Arquitectura familiar |
| **Animaciones Aceternity** | UX premium |
| **Magic UI interactions** | Experiencias memorables |
| **MIT License** | Uso comercial permitido |

---

## 📦 Instalación

### Paso 1: Dependencias Base

```bash
cd frontend

# Dependencias requeridas por EldoraUI
npm install framer-motion clsx tailwind-merge
npm install @radix-ui/react-slot
npm install lucide-react

# Opcional: Para animaciones avanzadas
npm install @react-spring/web
```

### Paso 2: Configurar Tailwind

```javascript
// tailwind.config.js
module.exports = {
  darkMode: ["class"],
  content: [
    "./src/**/*.{js,ts,jsx,tsx,mdx}",
    "./components/**/*.{js,ts,jsx,tsx,mdx}",
  ],
  theme: {
    extend: {
      colors: {
        // Paleta AFW
        primary: {
          DEFAULT: "#6366f1",  // Indigo
          foreground: "#ffffff",
        },
        secondary: {
          DEFAULT: "#8b5cf6",  // Violet
          foreground: "#ffffff",
        },
        accent: {
          DEFAULT: "#06b6d4",  // Cyan
          foreground: "#ffffff",
        },
        background: "#0a0a0f",
        foreground: "#fafafa",
        muted: {
          DEFAULT: "#27272a",
          foreground: "#a1a1aa",
        },
        card: {
          DEFAULT: "#18181b",
          foreground: "#fafafa",
        },
        border: "#27272a",
      },
      animation: {
        "fade-in": "fadeIn 0.5s ease-out",
        "slide-up": "slideUp 0.5s ease-out",
        "pulse-glow": "pulseGlow 2s infinite",
        "shimmer": "shimmer 2s linear infinite",
      },
      keyframes: {
        fadeIn: {
          "0%": { opacity: "0" },
          "100%": { opacity: "1" },
        },
        slideUp: {
          "0%": { transform: "translateY(20px)", opacity: "0" },
          "100%": { transform: "translateY(0)", opacity: "1" },
        },
        pulseGlow: {
          "0%, 100%": { boxShadow: "0 0 20px rgba(99, 102, 241, 0.5)" },
          "50%": { boxShadow: "0 0 40px rgba(99, 102, 241, 0.8)" },
        },
        shimmer: {
          "0%": { backgroundPosition: "-200% 0" },
          "100%": { backgroundPosition: "200% 0" },
        },
      },
    },
  },
  plugins: [require("tailwindcss-animate")],
};
```

### Paso 3: Utilidad cn()

```typescript
// frontend/src/lib/utils.ts
import { clsx, type ClassValue } from "clsx";
import { twMerge } from "tailwind-merge";

export function cn(...inputs: ClassValue[]) {
  return twMerge(clsx(inputs));
}
```

---

## 🧩 Componentes a Integrar

### 1. **Hero Section** (Landing Page)

```tsx
// components/ui/hero-section.tsx
import { motion } from "framer-motion";

export const HeroSection = () => {
  return (
    <div className="relative min-h-screen flex items-center justify-center overflow-hidden">
      {/* Gradient Background */}
      <div className="absolute inset-0 bg-gradient-to-br from-primary/20 via-background to-secondary/20" />
      
      {/* Animated Grid */}
      <div className="absolute inset-0 bg-[linear-gradient(rgba(99,102,241,0.1)_1px,transparent_1px),linear-gradient(90deg,rgba(99,102,241,0.1)_1px,transparent_1px)] bg-[size:50px_50px]" />
      
      <motion.div
        initial={{ opacity: 0, y: 20 }}
        animate={{ opacity: 1, y: 0 }}
        transition={{ duration: 0.8 }}
        className="relative z-10 text-center px-4"
      >
        <h1 className="text-5xl md:text-7xl font-bold bg-clip-text text-transparent bg-gradient-to-r from-primary via-secondary to-accent">
          AFW Platform
        </h1>
        <p className="mt-6 text-xl text-muted-foreground max-w-2xl mx-auto">
          102 Agentes Especializados para el Desarrollo de la Humanidad
        </p>
      </motion.div>
    </div>
  );
};
```

### 2. **Agent Cards** (Catálogo de Agentes)

```tsx
// components/ui/agent-card.tsx
import { motion } from "framer-motion";
import { cn } from "@/lib/utils";

interface AgentCardProps {
  name: string;
  emoji: string;
  description: string;
  category: string;
  onClick?: () => void;
}

export const AgentCard = ({ name, emoji, description, category, onClick }: AgentCardProps) => {
  return (
    <motion.div
      whileHover={{ scale: 1.02, y: -5 }}
      whileTap={{ scale: 0.98 }}
      onClick={onClick}
      className={cn(
        "relative group cursor-pointer",
        "rounded-xl border border-border/50",
        "bg-card/50 backdrop-blur-sm",
        "p-6 transition-all duration-300",
        "hover:border-primary/50 hover:shadow-lg hover:shadow-primary/10"
      )}
    >
      {/* Glow Effect */}
      <div className="absolute inset-0 rounded-xl bg-gradient-to-r from-primary/0 via-primary/5 to-secondary/0 opacity-0 group-hover:opacity-100 transition-opacity" />
      
      <div className="relative z-10">
        <span className="text-4xl">{emoji}</span>
        <h3 className="mt-4 font-semibold text-lg">{name}</h3>
        <p className="mt-2 text-sm text-muted-foreground line-clamp-2">
          {description}
        </p>
        <span className="mt-4 inline-block text-xs px-2 py-1 rounded-full bg-primary/10 text-primary">
          {category}
        </span>
      </div>
    </motion.div>
  );
};
```

### 3. **Chat Interface** (Mejorado)

```tsx
// components/ui/chat-bubble.tsx
import { motion } from "framer-motion";
import { cn } from "@/lib/utils";

interface ChatBubbleProps {
  role: "user" | "assistant";
  content: string;
  agentName?: string;
  agentEmoji?: string;
}

export const ChatBubble = ({ role, content, agentName, agentEmoji }: ChatBubbleProps) => {
  const isUser = role === "user";
  
  return (
    <motion.div
      initial={{ opacity: 0, y: 10 }}
      animate={{ opacity: 1, y: 0 }}
      className={cn(
        "flex gap-3",
        isUser ? "flex-row-reverse" : "flex-row"
      )}
    >
      {/* Avatar */}
      <div className={cn(
        "w-10 h-10 rounded-full flex items-center justify-center text-lg",
        isUser 
          ? "bg-primary text-primary-foreground" 
          : "bg-secondary/20 border border-secondary/50"
      )}>
        {isUser ? "👤" : agentEmoji || "🤖"}
      </div>
      
      {/* Message */}
      <div className={cn(
        "max-w-[80%] rounded-2xl px-4 py-3",
        isUser 
          ? "bg-primary text-primary-foreground rounded-tr-sm" 
          : "bg-card border border-border rounded-tl-sm"
      )}>
        {!isUser && agentName && (
          <p className="text-xs text-primary font-medium mb-1">{agentName}</p>
        )}
        <p className="text-sm leading-relaxed">{content}</p>
      </div>
    </motion.div>
  );
};
```

### 4. **Animated Button**

```tsx
// components/ui/animated-button.tsx
import { motion } from "framer-motion";
import { cn } from "@/lib/utils";

interface AnimatedButtonProps {
  children: React.ReactNode;
  variant?: "primary" | "secondary" | "outline" | "ghost";
  size?: "sm" | "md" | "lg";
  onClick?: () => void;
  className?: string;
}

export const AnimatedButton = ({ 
  children, 
  variant = "primary", 
  size = "md",
  onClick,
  className 
}: AnimatedButtonProps) => {
  return (
    <motion.button
      whileHover={{ scale: 1.02 }}
      whileTap={{ scale: 0.98 }}
      onClick={onClick}
      className={cn(
        "relative overflow-hidden rounded-lg font-medium transition-all",
        // Sizes
        size === "sm" && "px-3 py-1.5 text-sm",
        size === "md" && "px-4 py-2 text-base",
        size === "lg" && "px-6 py-3 text-lg",
        // Variants
        variant === "primary" && "bg-primary text-primary-foreground hover:bg-primary/90",
        variant === "secondary" && "bg-secondary text-secondary-foreground hover:bg-secondary/90",
        variant === "outline" && "border border-border hover:bg-accent/10",
        variant === "ghost" && "hover:bg-muted",
        className
      )}
    >
      {/* Shimmer Effect */}
      <span className="absolute inset-0 bg-gradient-to-r from-transparent via-white/10 to-transparent -translate-x-full hover:translate-x-full transition-transform duration-1000" />
      <span className="relative z-10">{children}</span>
    </motion.button>
  );
};
```

### 5. **Workflow Card**

```tsx
// components/ui/workflow-card.tsx
import { motion } from "framer-motion";
import { Clock, Users, Zap } from "lucide-react";

interface WorkflowCardProps {
  name: string;
  description: string;
  category: string;
  complexity: "basic" | "medium" | "complex";
  estimatedTime: number;
  agentCount: number;
}

export const WorkflowCard = ({
  name,
  description,
  category,
  complexity,
  estimatedTime,
  agentCount
}: WorkflowCardProps) => {
  const complexityColors = {
    basic: "text-green-400 bg-green-400/10",
    medium: "text-yellow-400 bg-yellow-400/10",
    complex: "text-red-400 bg-red-400/10"
  };

  return (
    <motion.div
      whileHover={{ y: -5 }}
      className="p-6 rounded-xl bg-card border border-border hover:border-primary/50 transition-all"
    >
      <div className="flex items-start justify-between">
        <div>
          <h3 className="font-semibold text-lg">{name}</h3>
          <p className="text-sm text-muted-foreground mt-1">{description}</p>
        </div>
        <span className={`px-2 py-1 rounded text-xs ${complexityColors[complexity]}`}>
          {complexity}
        </span>
      </div>
      
      <div className="flex items-center gap-4 mt-4 text-sm text-muted-foreground">
        <span className="flex items-center gap-1">
          <Clock className="w-4 h-4" />
          {estimatedTime}min
        </span>
        <span className="flex items-center gap-1">
          <Users className="w-4 h-4" />
          {agentCount} agentes
        </span>
        <span className="flex items-center gap-1">
          <Zap className="w-4 h-4" />
          {category}
        </span>
      </div>
    </motion.div>
  );
};
```

---

## 🎨 Paleta de Colores AFW

```css
:root {
  /* Primary - Indigo */
  --primary: 99 102 241;
  
  /* Secondary - Violet */  
  --secondary: 139 92 246;
  
  /* Accent - Cyan */
  --accent: 6 182 212;
  
  /* Background - Dark */
  --background: 10 10 15;
  
  /* Foreground - Light */
  --foreground: 250 250 250;
  
  /* Muted */
  --muted: 39 39 42;
  --muted-foreground: 161 161 170;
  
  /* Card */
  --card: 24 24 27;
  --card-foreground: 250 250 250;
  
  /* Border */
  --border: 39 39 42;
  
  /* Success/Error/Warning */
  --success: 34 197 94;
  --error: 239 68 68;
  --warning: 234 179 8;
}
```

---

## 📱 Responsive Design

### Breakpoints

```javascript
// tailwind.config.js
screens: {
  'sm': '640px',   // Mobile landscape
  'md': '768px',   // Tablet
  'lg': '1024px',  // Desktop
  'xl': '1280px',  // Large desktop
  '2xl': '1536px', // Extra large
}
```

### Mobile-First Approach

```tsx
// Ejemplo: Grid de agentes
<div className="grid grid-cols-1 sm:grid-cols-2 lg:grid-cols-3 xl:grid-cols-4 gap-4">
  {agents.map(agent => (
    <AgentCard key={agent.id} {...agent} />
  ))}
</div>
```

---

## 🚀 Plan de Implementación

### Fase 1: Fundamentos (1-2 días)
- [ ] Instalar dependencias
- [ ] Configurar Tailwind con paleta AFW
- [ ] Crear utilidades (cn, etc.)
- [ ] Componentes base (Button, Card, Input)

### Fase 2: Componentes Core (2-3 días)
- [ ] HeroSection
- [ ] AgentCard
- [ ] WorkflowCard
- [ ] ChatBubble
- [ ] NavigationMenu

### Fase 3: Páginas Principales (3-4 días)
- [ ] Landing Page
- [ ] Catálogo de Agentes
- [ ] Chat Interface mejorado
- [ ] Dashboard

### Fase 4: Animaciones y Polish (1-2 días)
- [ ] Transiciones de página
- [ ] Micro-interacciones
- [ ] Loading states
- [ ] Error states

---

## 📚 Recursos

- [EldoraUI Documentation](https://www.eldoraui.site/docs)
- [Framer Motion](https://www.framer.com/motion/)
- [Tailwind CSS](https://tailwindcss.com/)
- [Lucide Icons](https://lucide.dev/)

---

*AFW v0.5.0 - Diseñado para impresionar* ✨
