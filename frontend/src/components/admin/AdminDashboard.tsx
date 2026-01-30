/**
 * Admin Dashboard v1.0.0
 * ======================
 * Dashboard administrativo para monitoreo en tiempo real del sistema.
 */

'use client';

import React, { useState, useEffect } from 'react';
import { Users, Activity, Cpu, HardDrive, Wifi, TrendingUp, RefreshCw } from 'lucide-react';

interface DashboardStats {
  online_users: number;
  peak_users: number;
  active_sessions: number;
  websocket_connections: number;
  system_cpu_percent: number;
  system_memory_percent: number;
  device_breakdown: Record<string, number>;
}

interface OnlineUser {
  user_id: string;
  session_id: string;
  device_type: string;
  connected_at: string;
  last_activity: string;
  duration_seconds: number;
}

export function AdminDashboard() {
  const [stats, setStats] = useState<DashboardStats | null>(null);
  const [onlineUsers, setOnlineUsers] = useState<OnlineUser[]>([]);
  const [loading, setLoading] = useState(true);
  const [autoRefresh, setAutoRefresh] = useState(true);

  const fetchDashboardStats = async () => {
    try {
      const response = await fetch('/api/admin/stats/dashboard', {
        headers: {
          'Authorization': `Bearer ${localStorage.getItem('token')}`,
        },
      });

      if (response.ok) {
        const data = await response.json();
        setStats(data.dashboard);
      }
    } catch (error) {
      console.error('Error fetching dashboard stats:', error);
    }
  };

  const fetchOnlineUsers = async () => {
    try {
      const response = await fetch('/api/admin/stats/online-users', {
        headers: {
          'Authorization': `Bearer ${localStorage.getItem('token')}`,
        },
      });

      if (response.ok) {
        const data = await response.json();
        setOnlineUsers(data.users || []);
      }
    } catch (error) {
      console.error('Error fetching online users:', error);
    }
  };

  const refreshData = async () => {
    setLoading(true);
    await Promise.all([fetchDashboardStats(), fetchOnlineUsers()]);
    setLoading(false);
  };

  useEffect(() => {
    refreshData();

    if (autoRefresh) {
      const interval = setInterval(refreshData, 5000); // Refresh every 5 seconds
      return () => clearInterval(interval);
    }
  }, [autoRefresh]);

  if (loading && !stats) {
    return (
      <div className="flex items-center justify-center h-screen">
        <div className="text-center">
          <RefreshCw className="w-8 h-8 animate-spin mx-auto mb-4" />
          <p className="text-muted-foreground">Cargando dashboard...</p>
        </div>
      </div>
    );
  }

  return (
    <div className="min-h-screen bg-background p-6">
      {/* Header */}
      <div className="mb-8">
        <div className="flex items-center justify-between">
          <div>
            <h1 className="text-3xl font-bold mb-2">Panel de Administración</h1>
            <p className="text-muted-foreground">
              Monitoreo en tiempo real del sistema ATP
            </p>
          </div>
          
          <div className="flex items-center gap-4">
            <label className="flex items-center gap-2 cursor-pointer">
              <input
                type="checkbox"
                checked={autoRefresh}
                onChange={(e) => setAutoRefresh(e.target.checked)}
                className="w-4 h-4"
              />
              <span className="text-sm">Auto-refresh (5s)</span>
            </label>
            
            <button
              onClick={refreshData}
              className="p-2 bg-primary text-primary-foreground rounded-lg hover:bg-primary/90 transition-colors"
              aria-label="Refrescar"
            >
              <RefreshCw className={`w-5 h-5 ${loading ? 'animate-spin' : ''}`} />
            </button>
          </div>
        </div>
      </div>

      {/* Stats Grid */}
      {stats && (
        <div className="grid grid-cols-1 md:grid-cols-2 lg:grid-cols-4 gap-6 mb-8">
          <StatCard
            icon={<Users className="w-6 h-6" />}
            title="Usuarios en Línea"
            value={stats.online_users}
            subtitle={`Pico: ${stats.peak_users}`}
            color="blue"
          />
          
          <StatCard
            icon={<Activity className="w-6 h-6" />}
            title="Sesiones Activas"
            value={stats.active_sessions}
            subtitle={`WebSocket: ${stats.websocket_connections}`}
            color="green"
          />
          
          <StatCard
            icon={<Cpu className="w-6 h-6" />}
            title="CPU"
            value={`${stats.system_cpu_percent.toFixed(1)}%`}
            subtitle="Uso del sistema"
            color="orange"
            progress={stats.system_cpu_percent}
          />
          
          <StatCard
            icon={<HardDrive className="w-6 h-6" />}
            title="Memoria"
            value={`${stats.system_memory_percent.toFixed(1)}%`}
            subtitle="Uso del sistema"
            color="purple"
            progress={stats.system_memory_percent}
          />
        </div>
      )}

      {/* Device Breakdown */}
      {stats && stats.device_breakdown && (
        <div className="bg-card rounded-lg border border-border p-6 mb-8">
          <h2 className="text-xl font-semibold mb-4">Distribución por Dispositivo</h2>
          <div className="grid grid-cols-1 md:grid-cols-3 gap-4">
            {Object.entries(stats.device_breakdown).map(([device, count]) => (
              <div key={device} className="bg-accent rounded-lg p-4">
                <div className="flex items-center justify-between">
                  <span className="text-sm font-medium capitalize">{device}</span>
                  <span className="text-2xl font-bold">{count}</span>
                </div>
              </div>
            ))}
          </div>
        </div>
      )}

      {/* Online Users Table */}
      <div className="bg-card rounded-lg border border-border p-6">
        <h2 className="text-xl font-semibold mb-4">
          Usuarios Conectados ({onlineUsers.length})
        </h2>
        
        {onlineUsers.length === 0 ? (
          <div className="text-center py-8 text-muted-foreground">
            No hay usuarios conectados actualmente
          </div>
        ) : (
          <div className="overflow-x-auto">
            <table className="w-full">
              <thead>
                <tr className="border-b border-border">
                  <th className="text-left py-3 px-4 font-medium">Usuario</th>
                  <th className="text-left py-3 px-4 font-medium">Dispositivo</th>
                  <th className="text-left py-3 px-4 font-medium">Conectado</th>
                  <th className="text-left py-3 px-4 font-medium">Duración</th>
                  <th className="text-left py-3 px-4 font-medium">Sesión</th>
                </tr>
              </thead>
              <tbody>
                {onlineUsers.map((user) => (
                  <tr key={user.session_id} className="border-b border-border hover:bg-accent/50">
                    <td className="py-3 px-4">
                      <div className="flex items-center gap-2">
                        <div className="w-2 h-2 bg-green-500 rounded-full" />
                        <span className="font-mono text-sm">{user.user_id}</span>
                      </div>
                    </td>
                    <td className="py-3 px-4">
                      <span className="capitalize text-sm">{user.device_type}</span>
                    </td>
                    <td className="py-3 px-4 text-sm text-muted-foreground">
                      {new Date(user.connected_at).toLocaleTimeString('es-ES')}
                    </td>
                    <td className="py-3 px-4 text-sm">
                      {formatDuration(user.duration_seconds)}
                    </td>
                    <td className="py-3 px-4">
                      <span className="font-mono text-xs text-muted-foreground">
                        {user.session_id.substring(0, 12)}...
                      </span>
                    </td>
                  </tr>
                ))}
              </tbody>
            </table>
          </div>
        )}
      </div>
    </div>
  );
}

interface StatCardProps {
  icon: React.ReactNode;
  title: string;
  value: string | number;
  subtitle: string;
  color: 'blue' | 'green' | 'orange' | 'purple';
  progress?: number;
}

function StatCard({ icon, title, value, subtitle, color, progress }: StatCardProps) {
  const colorClasses = {
    blue: 'bg-blue-500/10 text-blue-500',
    green: 'bg-green-500/10 text-green-500',
    orange: 'bg-orange-500/10 text-orange-500',
    purple: 'bg-purple-500/10 text-purple-500',
  };

  return (
    <div className="bg-card rounded-lg border border-border p-6">
      <div className="flex items-start justify-between mb-4">
        <div className={`p-3 rounded-lg ${colorClasses[color]}`}>
          {icon}
        </div>
      </div>
      
      <div className="mb-2">
        <div className="text-3xl font-bold mb-1">{value}</div>
        <div className="text-sm text-muted-foreground">{title}</div>
      </div>
      
      {progress !== undefined && (
        <div className="mb-2">
          <div className="w-full bg-accent rounded-full h-2">
            <div
              className={`h-2 rounded-full transition-all ${
                progress > 80 ? 'bg-red-500' : progress > 60 ? 'bg-orange-500' : 'bg-green-500'
              }`}
              style={{ width: `${Math.min(progress, 100)}%` }}
            />
          </div>
        </div>
      )}
      
      <div className="text-xs text-muted-foreground">{subtitle}</div>
    </div>
  );
}

function formatDuration(seconds: number): string {
  if (seconds < 60) {
    return `${Math.floor(seconds)}s`;
  } else if (seconds < 3600) {
    return `${Math.floor(seconds / 60)}m`;
  } else {
    const hours = Math.floor(seconds / 3600);
    const minutes = Math.floor((seconds % 3600) / 60);
    return `${hours}h ${minutes}m`;
  }
}
