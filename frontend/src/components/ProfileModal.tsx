"use client";

import { useEffect, useState } from "react";
import {
    Dialog, DialogContent, DialogHeader, DialogTitle
} from "@/components/ui/dialog";
import { Button } from "@/components/ui/button";
import { Loader2, Activity, Zap, Shield, Crown } from "lucide-react";
import { useAuth } from "@/components/AuthProvider";
import { fetchWithAuth } from "@/lib/api";

interface ProfileModalProps {
    isOpen: boolean;
    onClose: () => void;
}

interface UserUsage {
    allowed: boolean;
    queries_used: number;
    queries_limit: number;
    queries_remaining: number;
    plan_name: string;
    plan_features: string[];
}

export function ProfileModal({ isOpen, onClose }: ProfileModalProps) {
    const { user, logout } = useAuth();
    const [usage, setUsage] = useState<UserUsage | null>(null);
    const [isLoading, setIsLoading] = useState(false);

    useEffect(() => {
        if (isOpen && user) {
            loadUsage();
        }
    }, [isOpen, user]);

    const loadUsage = async () => {
        setIsLoading(true);
        try {
            const res = await fetchWithAuth("/api/auth/usage");
            if (res.ok) {
                const data = await res.json();
                setUsage(data);
            }
        } catch (error) {
            console.error(error);
        } finally {
            setIsLoading(false);
        }
    };

    if (!isOpen) return null;

    if (!user) {
        onClose();
        return null;
    }

    const percentageUsed = usage
        ? Math.min(100, Math.round((usage.queries_used / usage.queries_limit) * 100))
        : 0;

    return (
        <Dialog open={isOpen} onOpenChange={onClose}>
            <DialogContent className="sm:max-w-md bg-card border-primary/20">
                <DialogHeader>
                    <DialogTitle className="flex items-center gap-2">
                        <div className="h-8 w-8 rounded-full bg-primary/20 flex items-center justify-center border border-primary/30">
                            <span className="font-bold text-primary">{user.username ? user.username[0].toUpperCase() : "U"}</span>
                        </div>
                        <span className="text-xl font-bold">{user.username}</span>
                    </DialogTitle>
                </DialogHeader>

                <div className="space-y-6 py-4">
                    {/* User Info */}
                    <div className="grid grid-cols-2 gap-4">
                        <div className="bg-muted/40 p-3 rounded-xl border border-border">
                            <p className="text-[10px] text-muted-foreground uppercase tracking-widest font-bold mb-1">Role</p>
                            <div className="flex items-center gap-2">
                                <Shield className="h-4 w-4 text-primary" />
                                <span className="font-medium text-sm capitalize">{user.role}</span>
                            </div>
                        </div>
                        <div className="bg-muted/40 p-3 rounded-xl border border-border">
                            <p className="text-[10px] text-muted-foreground uppercase tracking-widest font-bold mb-1">Code</p>
                            <div className="flex items-center gap-2">
                                <span className="font-mono text-sm bg-black/20 px-2 py-0.5 rounded text-primary/80">{user.user_code}</span>
                            </div>
                        </div>
                    </div>

                    {/* Usage Stats from Backend */}
                    <div className="bg-gradient-to-br from-primary/5 via-card to-card p-4 rounded-xl border border-primary/10 relative overflow-hidden">
                        <div className="flex items-center justify-between mb-4">
                            <div className="flex items-center gap-2">
                                <Activity className="h-5 w-5 text-primary" />
                                <h3 className="font-bold text-sm">Uso Mensual</h3>
                            </div>
                            {usage?.plan_name === "Premium" && (
                                <span className="flex items-center gap-1 text-[10px] font-bold bg-amber-500/10 text-amber-500 px-2 py-0.5 rounded-full border border-amber-500/20">
                                    <Crown className="h-3 w-3" /> PREMIUM
                                </span>
                            )}
                        </div>

                        {isLoading ? (
                            <div className="h-20 flex items-center justify-center">
                                <Loader2 className="h-6 w-6 animate-spin text-primary" />
                            </div>
                        ) : usage ? (
                            <div className="space-y-4">
                                <div>
                                    <div className="flex justify-between text-xs mb-1">
                                        <span className="text-muted-foreground">Consultas realizadas</span>
                                        <span className="font-mono font-bold">{usage.queries_used} / {usage.queries_limit}</span>
                                    </div>
                                    <div className="h-2 bg-muted rounded-full overflow-hidden">
                                        <div
                                            className="h-full bg-gradient-to-r from-primary to-purple-500 transition-all duration-500"
                                            style={{ width: `${percentageUsed}%` }}
                                        />
                                    </div>
                                </div>

                                <div className="flex gap-2 flex-wrap">
                                    {usage.plan_features.map((feature: string, i: number) => (
                                        <span key={i} className="text-[10px] px-2 py-1 bg-background border border-border rounded-md text-muted-foreground">
                                            {feature}
                                        </span>
                                    ))}
                                </div>

                                {usage.queries_remaining < 5 && (
                                    <div className="text-xs text-amber-500 bg-amber-500/10 p-2 rounded border border-amber-500/20 flex items-center gap-2">
                                        <Zap className="h-3 w-3" />
                                        Te quedan pocas consultas este mes.
                                    </div>
                                )}
                            </div>
                        ) : (
                            <p className="text-xs text-muted-foreground">No se pudo cargar la información de uso.</p>
                        )}
                    </div>

                    <div className="flex justify-between items-center pt-2">
                        <Button variant="outline" size="sm" className="text-xs text-muted-foreground hover:text-foreground" onClick={onClose}>
                            Cerrar
                        </Button>

                        <Button
                            variant="destructive"
                            size="sm"
                            className="text-xs"
                            onClick={() => {
                                logout();
                                onClose();
                            }}
                        >
                            Cerrar Sesión
                        </Button>
                    </div>
                </div>
            </DialogContent>
        </Dialog>
    );
}
