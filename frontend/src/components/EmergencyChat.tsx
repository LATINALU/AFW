"use client";

export default function EmergencyChat() {
  return (
    <div className="flex-1 flex items-center justify-center p-8 bg-background">
      <div className="text-center max-w-md">
        <div className="mb-8">
          <h1 className="text-3xl font-bold text-primary mb-4">
            ATP Platform
          </h1>
          <p className="text-muted-foreground">
            Sistema de Agentes de IA - Modo Emergencia
          </p>
        </div>
        
        <div className="space-y-4">
          <div className="p-4 bg-green-500/10 border border-green-500/20 rounded-lg">
            <p className="text-green-400">✅ Frontend funcionando</p>
          </div>
          <div className="p-4 bg-blue-500/10 border border-blue-500/20 rounded-lg">
            <p className="text-blue-400">🔧 Modo emergencia activado</p>
          </div>
          <div className="p-4 bg-yellow-500/10 border border-yellow-500/20 rounded-lg">
            <p className="text-yellow-400">⚠️ Depurando sistema principal</p>
          </div>
        </div>
        
        <div className="mt-8 text-sm text-muted-foreground">
          <p>Sistema operativo en modo simplificado</p>
          <p>Por favor, espera mientras solucionamos los problemas técnicos...</p>
        </div>
      </div>
    </div>
  );
}
