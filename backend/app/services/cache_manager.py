"""
Cache Manager v1.0.0
===================
Sistema de caché con Redis para mejorar el rendimiento y reducir carga.
"""

import redis
import json
import hashlib
from typing import Optional, Any, Callable
from datetime import timedelta
from functools import wraps
import asyncio


class CacheManager:
    """
    Gestor de caché con Redis para optimización de rendimiento.
    
    Características:
    - Caché de respuestas de agentes
    - Caché de consultas frecuentes
    - TTL configurable por tipo de dato
    - Invalidación selectiva
    - Fallback a memoria si Redis no está disponible
    """
    
    def __init__(self, redis_url: str = "redis://localhost:6379"):
        """
        Inicializa el gestor de caché.
        
        Args:
            redis_url: URL de conexión a Redis
        """
        try:
            self.redis_client = redis.from_url(
                redis_url,
                decode_responses=True,
                socket_connect_timeout=5
            )
            self.redis_client.ping()
            self.available = True
            print("✅ Redis Cache Manager conectado")
        except Exception as e:
            print(f"⚠️ Redis no disponible para caché, usando fallback: {e}")
            self.redis_client = None
            self.available = False
            self._memory_cache = {}
        
        # Prefijos de keys
        self.AGENT_RESPONSE_PREFIX = "atp:cache:agent:"
        self.QUERY_CACHE_PREFIX = "atp:cache:query:"
        self.MODEL_CACHE_PREFIX = "atp:cache:model:"
        
        # TTLs por defecto (en segundos)
        self.DEFAULT_TTL = 3600  # 1 hora
        self.AGENT_RESPONSE_TTL = 7200  # 2 horas
        self.QUERY_CACHE_TTL = 1800  # 30 minutos
        self.MODEL_CACHE_TTL = 86400  # 24 horas
    
    def _generate_key(self, prefix: str, *args) -> str:
        """
        Genera una key única para el caché.
        
        Args:
            prefix: Prefijo de la key
            *args: Argumentos para generar el hash
            
        Returns:
            Key única
        """
        # Crear hash de los argumentos
        content = json.dumps(args, sort_keys=True)
        hash_value = hashlib.md5(content.encode()).hexdigest()
        return f"{prefix}{hash_value}"
    
    async def get(self, key: str) -> Optional[Any]:
        """
        Obtiene un valor del caché.
        
        Args:
            key: Key del valor
            
        Returns:
            Valor cacheado o None si no existe
        """
        if self.redis_client:
            try:
                value = self.redis_client.get(key)
                if value:
                    return json.loads(value)
                return None
            except Exception as e:
                print(f"⚠️ Error obteniendo del caché: {e}")
                return None
        else:
            # Fallback a memoria
            return self._memory_cache.get(key)
    
    async def set(
        self,
        key: str,
        value: Any,
        ttl: Optional[int] = None
    ) -> bool:
        """
        Guarda un valor en el caché.
        
        Args:
            key: Key del valor
            value: Valor a guardar
            ttl: Tiempo de vida en segundos (None = DEFAULT_TTL)
            
        Returns:
            True si se guardó exitosamente
        """
        ttl = ttl or self.DEFAULT_TTL
        
        if self.redis_client:
            try:
                serialized = json.dumps(value)
                self.redis_client.setex(key, ttl, serialized)
                return True
            except Exception as e:
                print(f"⚠️ Error guardando en caché: {e}")
                return False
        else:
            # Fallback a memoria (sin TTL automático)
            self._memory_cache[key] = value
            return True
    
    async def delete(self, key: str) -> bool:
        """
        Elimina un valor del caché.
        
        Args:
            key: Key a eliminar
            
        Returns:
            True si se eliminó
        """
        if self.redis_client:
            try:
                self.redis_client.delete(key)
                return True
            except:
                return False
        else:
            if key in self._memory_cache:
                del self._memory_cache[key]
                return True
            return False
    
    async def clear_pattern(self, pattern: str) -> int:
        """
        Elimina todas las keys que coincidan con un patrón.
        
        Args:
            pattern: Patrón de búsqueda (ej: "atp:cache:agent:*")
            
        Returns:
            Número de keys eliminadas
        """
        if self.redis_client:
            try:
                keys = list(self.redis_client.scan_iter(match=pattern))
                if keys:
                    self.redis_client.delete(*keys)
                return len(keys)
            except:
                return 0
        else:
            # Fallback a memoria
            count = 0
            keys_to_delete = [
                k for k in self._memory_cache.keys()
                if pattern.replace('*', '') in k
            ]
            for key in keys_to_delete:
                del self._memory_cache[key]
                count += 1
            return count
    
    async def cache_agent_response(
        self,
        agent_id: str,
        task: str,
        model: str,
        response: str
    ) -> bool:
        """
        Cachea la respuesta de un agente.
        
        Args:
            agent_id: ID del agente
            task: Tarea procesada
            model: Modelo usado
            response: Respuesta del agente
            
        Returns:
            True si se cacheó exitosamente
        """
        key = self._generate_key(
            self.AGENT_RESPONSE_PREFIX,
            agent_id,
            task,
            model
        )
        
        return await self.set(key, {
            "agent_id": agent_id,
            "task": task,
            "model": model,
            "response": response
        }, ttl=self.AGENT_RESPONSE_TTL)
    
    async def get_cached_agent_response(
        self,
        agent_id: str,
        task: str,
        model: str
    ) -> Optional[str]:
        """
        Obtiene una respuesta cacheada de un agente.
        
        Args:
            agent_id: ID del agente
            task: Tarea a buscar
            model: Modelo usado
            
        Returns:
            Respuesta cacheada o None
        """
        key = self._generate_key(
            self.AGENT_RESPONSE_PREFIX,
            agent_id,
            task,
            model
        )
        
        cached = await self.get(key)
        if cached:
            return cached.get("response")
        return None
    
    async def cache_query_result(
        self,
        query: str,
        agents: list,
        model: str,
        result: str
    ) -> bool:
        """
        Cachea el resultado de una consulta completa.
        
        Args:
            query: Consulta del usuario
            agents: Lista de agentes usados
            model: Modelo usado
            result: Resultado final
            
        Returns:
            True si se cacheó exitosamente
        """
        key = self._generate_key(
            self.QUERY_CACHE_PREFIX,
            query,
            sorted(agents),
            model
        )
        
        return await self.set(key, {
            "query": query,
            "agents": agents,
            "model": model,
            "result": result
        }, ttl=self.QUERY_CACHE_TTL)
    
    async def get_cached_query_result(
        self,
        query: str,
        agents: list,
        model: str
    ) -> Optional[str]:
        """
        Obtiene el resultado cacheado de una consulta.
        
        Args:
            query: Consulta del usuario
            agents: Lista de agentes usados
            model: Modelo usado
            
        Returns:
            Resultado cacheado o None
        """
        key = self._generate_key(
            self.QUERY_CACHE_PREFIX,
            query,
            sorted(agents),
            model
        )
        
        cached = await self.get(key)
        if cached:
            return cached.get("result")
        return None
    
    async def get_stats(self) -> dict:
        """
        Obtiene estadísticas del caché.
        
        Returns:
            Diccionario con estadísticas
        """
        if self.redis_client:
            try:
                info = self.redis_client.info('stats')
                return {
                    "available": True,
                    "total_keys": self.redis_client.dbsize(),
                    "hits": info.get('keyspace_hits', 0),
                    "misses": info.get('keyspace_misses', 0),
                    "memory_used": self.redis_client.info('memory').get('used_memory_human', 'N/A')
                }
            except:
                return {"available": False, "error": "Could not get stats"}
        else:
            return {
                "available": False,
                "total_keys": len(self._memory_cache),
                "backend": "memory"
            }


def cached(ttl: int = 3600, key_prefix: str = "atp:cache:func:"):
    """
    Decorador para cachear resultados de funciones.
    
    Args:
        ttl: Tiempo de vida del caché en segundos
        key_prefix: Prefijo para las keys del caché
        
    Returns:
        Decorador
    """
    def decorator(func: Callable):
        @wraps(func)
        async def wrapper(*args, **kwargs):
            # Generar key única
            cache_key = f"{key_prefix}{func.__name__}:{hash((args, tuple(sorted(kwargs.items()))))}"
            
            # Intentar obtener del caché
            cache_manager = get_cache_manager()
            cached_result = await cache_manager.get(cache_key)
            
            if cached_result is not None:
                return cached_result
            
            # Ejecutar función
            if asyncio.iscoroutinefunction(func):
                result = await func(*args, **kwargs)
            else:
                result = func(*args, **kwargs)
            
            # Guardar en caché
            await cache_manager.set(cache_key, result, ttl=ttl)
            
            return result
        
        return wrapper
    return decorator


# Instancia global del cache manager
_cache_manager_instance: Optional[CacheManager] = None


def get_cache_manager(redis_url: str = "redis://localhost:6379") -> CacheManager:
    """
    Obtiene la instancia global del cache manager (singleton).
    
    Args:
        redis_url: URL de conexión a Redis
        
    Returns:
        Instancia del cache manager
    """
    global _cache_manager_instance
    if _cache_manager_instance is None:
        _cache_manager_instance = CacheManager(redis_url)
    return _cache_manager_instance
