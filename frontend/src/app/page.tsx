"use client";

/**
 * ATP v1.1.0 - Responsive Router with New Features
 * ================================================
 * Detecta el tamaño de pantalla y carga la versión apropiada
 */

import { useState, useEffect } from "react";
import dynamic from "next/dynamic";

const LoadingScreen = () => (
  <div className="h-screen flex items-center justify-center bg-background">
    <div className="text-center">
      <div className="h-12 w-12 rounded-xl bg-gradient-to-br from-primary/30 to-cyan-500/30 border border-primary/50 flex items-center justify-center mx-auto mb-4">
        <span className="text-2xl font-black text-primary">A</span>
      </div>
      <p className="text-sm text-muted-foreground">Loading ATP Platform...</p>
    </div>
  </div>
);

const DesktopPage = dynamic(() => import("./page.desktop"), {
  ssr: false,
  loading: LoadingScreen,
});
const MobilePage = dynamic(() => import("./page.mobile"), {
  ssr: false,
  loading: LoadingScreen,
});

export default function HomePage() {
  const [isDesktop, setIsDesktop] = useState(true);

  useEffect(() => {
    const checkScreenSize = () => {
      setIsDesktop(window.innerWidth >= 1024);
    };
    
    checkScreenSize();
    window.addEventListener('resize', checkScreenSize);
    return () => window.removeEventListener('resize', checkScreenSize);
  }, []);

  return isDesktop ? <DesktopPage /> : <MobilePage />;
}
