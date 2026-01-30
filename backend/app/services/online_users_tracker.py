"""
Online Users Tracker v1.0.0
===========================
Sistema de seguimiento de usuarios en línea usando Redis para alta disponibilidad.
Permite monitorear usuarios activos en tiempo real y generar estadísticas.
"""

import redis
import json
from datetime import datetime, timedelta
from typing import Dict, List, Optional, Set
import asyncio
from dataclasses import dataclass, asdict


@dataclass
class OnlineUser:
    """Representa un usuario en línea"""
    user_id: str
    session_id: str
    client_id: str
    connected_at: str
    last_activity: str
    ip_address: Optional[str] = None
    user_agent: Optional[str] = None
    device_type: Optional[str] = None


class OnlineUsersTracker:
    """
    Gestor de usuarios en línea con Redis.
    
    Características:
    - Tracking en tiempo real de usuarios conectados
    - Detección automática de desconexiones
    - Estadísticas de uso y concurrencia
    - Soporte para múltiples sesiones por usuario
    """
    
    def __init__(self, redis_url: str = "redis://localhost:6379"):
        """
        Inicializa el tracker con conexión a Redis.
        
        Args:
            redis_url: URL de conexión a Redis
        """
        try:
            self.redis_client = redis.from_url(
                redis_url,
                decode_responses=True,
                socket_connect_timeout=5
            )
            # Test connection
            self.redis_client.ping()
            print("✅ Redis conectado para tracking de usuarios")
        except Exception as e:
            print(f"⚠️ Redis no disponible, usando fallback en memoria: {e}")
            self.redis_client = None
            self._memory_store: Dict[str, OnlineUser] = {}
        
        # Configuración
        self.user_ttl = 300  # 5 minutos de TTL
        self.cleanup_interval = 60  # Limpiar cada minuto
        
        # Prefijos de keys
        self.ONLINE_USERS_KEY = "atp:online_users"
        self.USER_SESSIONS_PREFIX = "atp:user_sessions:"
        self.STATS_KEY = "atp:stats"
        self.PEAK_USERS_KEY = "atp:peak_users"
    
    async def add_user(
        self,
        user_id: str,
        session_id: str,
        client_id: str,
        ip_address: Optional[str] = None,
        user_agent: Optional[str] = None,
        device_type: Optional[str] = None
    ) -> bool:
        """
        Registra un usuario como en línea.
        
        Args:
            user_id: ID del usuario
            session_id: ID de sesión
            client_id: ID del cliente WebSocket
            ip_address: Dirección IP
            user_agent: User agent del navegador
            device_type: Tipo de dispositivo (mobile/desktop/tablet)
            
        Returns:
            True si se registró exitosamente
        """
        now = datetime.utcnow().isoformat()
        
        user = OnlineUser(
            user_id=user_id,
            session_id=session_id,
            client_id=client_id,
            connected_at=now,
            last_activity=now,
            ip_address=ip_address,
            user_agent=user_agent,
            device_type=device_type
        )
        
        if self.redis_client:
            try:
                # Agregar a set de usuarios en línea
                self.redis_client.sadd(self.ONLINE_USERS_KEY, user_id)
                
                # Guardar datos del usuario con TTL
                user_key = f"{self.USER_SESSIONS_PREFIX}{session_id}"
                self.redis_client.setex(
                    user_key,
                    self.user_ttl,
                    json.dumps(asdict(user))
                )
                
                # Actualizar estadísticas
                await self._update_stats()
                
                print(f"👤 Usuario conectado: {user_id} (session: {session_id})")
                return True
            except Exception as e:
                print(f"❌ Error agregando usuario a Redis: {e}")
                return False
        else:
            # Fallback en memoria
            self._memory_store[session_id] = user
            return True
    
    async def update_activity(self, session_id: str) -> bool:
        """
        Actualiza la última actividad de un usuario.
        
        Args:
            session_id: ID de sesión del usuario
            
        Returns:
            True si se actualizó exitosamente
        """
        now = datetime.utcnow().isoformat()
        
        if self.redis_client:
            try:
                user_key = f"{self.USER_SESSIONS_PREFIX}{session_id}"
                user_data = self.redis_client.get(user_key)
                
                if user_data:
                    user = json.loads(user_data)
                    user['last_activity'] = now
                    
                    # Renovar TTL
                    self.redis_client.setex(
                        user_key,
                        self.user_ttl,
                        json.dumps(user)
                    )
                    return True
                return False
            except Exception as e:
                print(f"❌ Error actualizando actividad: {e}")
                return False
        else:
            # Fallback en memoria
            if session_id in self._memory_store:
                self._memory_store[session_id].last_activity = now
                return True
            return False
    
    async def remove_user(self, session_id: str) -> bool:
        """
        Elimina un usuario de la lista de en línea.
        
        Args:
            session_id: ID de sesión del usuario
            
        Returns:
            True si se eliminó exitosamente
        """
        if self.redis_client:
            try:
                user_key = f"{self.USER_SESSIONS_PREFIX}{session_id}"
                user_data = self.redis_client.get(user_key)
                
                if user_data:
                    user = json.loads(user_data)
                    user_id = user['user_id']
                    
                    # Eliminar datos de sesión
                    self.redis_client.delete(user_key)
                    
                    # Verificar si el usuario tiene otras sesiones activas
                    has_other_sessions = await self._user_has_active_sessions(user_id, session_id)
                    
                    if not has_other_sessions:
                        # Eliminar del set de usuarios en línea
                        self.redis_client.srem(self.ONLINE_USERS_KEY, user_id)
                    
                    print(f"👋 Usuario desconectado: {user_id} (session: {session_id})")
                    return True
                return False
            except Exception as e:
                print(f"❌ Error eliminando usuario: {e}")
                return False
        else:
            # Fallback en memoria
            if session_id in self._memory_store:
                del self._memory_store[session_id]
                return True
            return False
    
    async def get_online_count(self) -> int:
        """
        Obtiene el número de usuarios únicos en línea.
        
        Returns:
            Número de usuarios en línea
        """
        if self.redis_client:
            try:
                return self.redis_client.scard(self.ONLINE_USERS_KEY)
            except Exception as e:
                print(f"❌ Error obteniendo conteo: {e}")
                return 0
        else:
            # Fallback en memoria - contar usuarios únicos
            unique_users = set(user.user_id for user in self._memory_store.values())
            return len(unique_users)
    
    async def get_online_users(self) -> List[Dict]:
        """
        Obtiene la lista de todos los usuarios en línea con sus detalles.
        
        Returns:
            Lista de usuarios en línea
        """
        if self.redis_client:
            try:
                # Obtener todas las sesiones activas
                pattern = f"{self.USER_SESSIONS_PREFIX}*"
                sessions = []
                
                for key in self.redis_client.scan_iter(match=pattern):
                    user_data = self.redis_client.get(key)
                    if user_data:
                        sessions.append(json.loads(user_data))
                
                return sessions
            except Exception as e:
                print(f"❌ Error obteniendo usuarios: {e}")
                return []
        else:
            # Fallback en memoria
            return [asdict(user) for user in self._memory_store.values()]
    
    async def get_user_sessions(self, user_id: str) -> List[Dict]:
        """
        Obtiene todas las sesiones activas de un usuario específico.
        
        Args:
            user_id: ID del usuario
            
        Returns:
            Lista de sesiones del usuario
        """
        all_users = await self.get_online_users()
        return [user for user in all_users if user['user_id'] == user_id]
    
    async def get_stats(self) -> Dict:
        """
        Obtiene estadísticas detalladas de usuarios en línea.
        
        Returns:
            Diccionario con estadísticas
        """
        online_users = await self.get_online_users()
        unique_users = set(user['user_id'] for user in online_users)
        
        # Contar por tipo de dispositivo
        device_counts = {}
        for user in online_users:
            device = user.get('device_type', 'unknown')
            device_counts[device] = device_counts.get(device, 0) + 1
        
        # Obtener pico de usuarios
        peak_users = 0
        if self.redis_client:
            try:
                peak_data = self.redis_client.get(self.PEAK_USERS_KEY)
                if peak_data:
                    peak_users = int(peak_data)
            except:
                pass
        
        current_count = len(unique_users)
        
        # Actualizar pico si es necesario
        if current_count > peak_users:
            peak_users = current_count
            if self.redis_client:
                try:
                    self.redis_client.set(self.PEAK_USERS_KEY, peak_users)
                except:
                    pass
        
        return {
            "online_users": current_count,
            "total_sessions": len(online_users),
            "peak_users": peak_users,
            "device_breakdown": device_counts,
            "timestamp": datetime.utcnow().isoformat()
        }
    
    async def cleanup_stale_users(self):
        """
        Limpia usuarios inactivos (ejecutar periódicamente).
        Redis maneja esto automáticamente con TTL, pero útil para fallback.
        """
        if not self.redis_client:
            # Limpiar memoria manualmente
            now = datetime.utcnow()
            stale_sessions = []
            
            for session_id, user in self._memory_store.items():
                last_activity = datetime.fromisoformat(user.last_activity)
                if (now - last_activity).total_seconds() > self.user_ttl:
                    stale_sessions.append(session_id)
            
            for session_id in stale_sessions:
                del self._memory_store[session_id]
            
            if stale_sessions:
                print(f"🧹 Limpiados {len(stale_sessions)} usuarios inactivos")
    
    async def _user_has_active_sessions(self, user_id: str, exclude_session: str) -> bool:
        """
        Verifica si un usuario tiene otras sesiones activas.
        
        Args:
            user_id: ID del usuario
            exclude_session: Sesión a excluir de la búsqueda
            
        Returns:
            True si tiene otras sesiones activas
        """
        sessions = await self.get_user_sessions(user_id)
        return any(s['session_id'] != exclude_session for s in sessions)
    
    async def _update_stats(self):
        """Actualiza estadísticas globales."""
        if self.redis_client:
            try:
                stats = await self.get_stats()
                self.redis_client.setex(
                    self.STATS_KEY,
                    60,  # Cache por 1 minuto
                    json.dumps(stats)
                )
            except:
                pass


# Instancia global del tracker
_tracker_instance: Optional[OnlineUsersTracker] = None


def get_tracker(redis_url: str = "redis://localhost:6379") -> OnlineUsersTracker:
    """
    Obtiene la instancia global del tracker (singleton).
    
    Args:
        redis_url: URL de conexión a Redis
        
    Returns:
        Instancia del tracker
    """
    global _tracker_instance
    if _tracker_instance is None:
        _tracker_instance = OnlineUsersTracker(redis_url)
    return _tracker_instance
