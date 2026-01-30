"use client";

export default function TestChat() {
  return (
    <div className="flex-1 flex items-center justify-center p-8">
      <div className="text-center">
        <h1 className="text-2xl font-bold mb-4">Chat de Prueba</h1>
        <p className="text-muted-foreground">El sistema está funcionando correctamente.</p>
        <div className="mt-4 p-4 bg-muted rounded-lg">
          <p>✅ Frontend cargado</p>
          <p>✅ Componente renderizado</p>
          <p>✅ Sin errores de JavaScript</p>
        </div>
      </div>
    </div>
  );
}
