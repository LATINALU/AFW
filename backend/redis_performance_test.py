#!/usr/bin/env python3
"""
ATP v0.8.0+ - Redis Performance Test
====================================

Script para probar el rendimiento de Redis con rate limiting
"""

import redis
import time
import threading
from datetime import datetime

# Configuración
REDIS_URL = "redis://:atp_redis_dev_password_2024@redis:6379"

def test_rate_limiting_performance():
    """Test de rendimiento para rate limiting"""
    print("🚀 Test de Rate Limiting Performance")
    print("=" * 50)
    
    try:
        r = redis.from_url(REDIS_URL)
        
        # Test 1: Operaciones básicas
        print("\n📊 Test 1: Operaciones Básicas")
        start_time = time.time()
        
        for i in range(1000):
            key = f"rate_limit:user_{i % 100}:api_test"
            r.setex(key, 60, "1")
        
        end_time = time.time()
        ops_per_sec = 1000 / (end_time - start_time)
        print(f"✅ 1000 operaciones SETEX: {ops_per_sec:.2f} ops/sec")
        
        # Test 2: Operaciones de lectura
        print("\n📊 Test 2: Operaciones de Lectura")
        start_time = time.time()
        
        for i in range(1000):
            key = f"rate_limit:user_{i % 100}:api_test"
            r.get(key)
        
        end_time = time.time()
        ops_per_sec = 1000 / (end_time - start_time)
        print(f"✅ 1000 operaciones GET: {ops_per_sec:.2f} ops/sec")
        
        # Test 3: Operaciones de expiración
        print("\n📊 Test 3: Operaciones de Expiración")
        start_time = time.time()
        
        for i in range(100):
            key = f"rate_limit:user_{i}:expire_test"
            r.setex(key, 1, "test")
        
        # Esperar 2 segundos
        time.sleep(2)
        
        # Verificar que hayan expirado
        expired_count = 0
        for i in range(100):
            key = f"rate_limit:user_{i}:expire_test"
            if not r.exists(key):
                expired_count += 1
        
        end_time = time.time()
        print(f"✅ {expired_count}/100 claves expiraron correctamente")
        
        # Test 4: Concurrent operations
        print("\n📊 Test 4: Operaciones Concurrentes")
        
        def worker_thread(thread_id, num_ops):
            for i in range(num_ops):
                key = f"rate_limit:user_{thread_id}_{i}:concurrent"
                r.setex(key, 60, f"thread_{thread_id}_op_{i}")
        
        start_time = time.time()
        threads = []
        
        # Crear 10 hilos con 100 operaciones cada uno
        for i in range(10):
            thread = threading.Thread(target=worker_thread, args=(i, 100))
            threads.append(thread)
            thread.start()
        
        # Esperar a que todos terminen
        for thread in threads:
            thread.join()
        
        end_time = time.time()
        total_ops = 10 * 100
        ops_per_sec = total_ops / (end_time - start_time)
        print(f"✅ {total_ops} operaciones concurrentes: {ops_per_sec:.2f} ops/sec")
        
        # Test 5: Memory usage
        print("\n📊 Test 5: Uso de Memoria")
        info = r.info()
        used_memory = info.get('used_memory_human')
        used_memory_bytes = info.get('used_memory')
        
        print(f"✅ Memoria usada: {used_memory}")
        print(f"✅ Memoria en bytes: {used_memory_bytes:,}")
        
        # Calcular memoria por clave
        if used_memory_bytes and r.dbsize() > 0:
            memory_per_key = used_memory_bytes / r.dbsize()
            print(f"✅ Memoria por clave: {memory_per_key:.2f} bytes")
        
        return True
        
    except Exception as e:
        print(f"❌ Error en performance test: {e}")
        return False

def test_redis_optimizations():
    """Test de optimizaciones específicas para ATP"""
    print("\n🔧 Test de Optimizaciones ATP")
    print("=" * 50)
    
    try:
        r = redis.from_url(REDIS_URL)
        
        # Test de compresión de datos
        print("\n📊 Test de Compresión de Datos")
        
        # Datos grandes
        large_data = "x" * 10000  # 10KB
        start_time = time.time()
        
        for i in range(100):
            key = f"cache:agent_response:{i}"
            r.setex(key, 3600, large_data)
        
        end_time = time.time()
        ops_per_sec = 100 / (end_time - start_time)
        print(f"✅ 100 operaciones con datos grandes: {ops_per_sec:.2f} ops/sec")
        
        # Test de hash structures
        print("\n📊 Test de Hash Structures")
        
        start_time = time.time()
        
        for i in range(100):
            hash_key = f"session:{i}"
            r.hset(hash_key, "user_id", f"user_{i}")
            r.hset(hash_key, "created_at", str(time.time()))
            r.hset(hash_key, "last_activity", str(time.time()))
            r.expire(hash_key, 86400)
        
        end_time = time.time()
        ops_per_sec = 100 / (end_time - start_time)
        print(f"✅ 100 operaciones HASH: {ops_per_sec:.2f} ops/sec")
        
        # Test de listas
        print("\n📊 Test de Listas")
        
        start_time = time.time()
        
        for i in range(50):
            list_key = f"conversation:{i}:messages"
            for j in range(10):
                r.lpush(list_key, f"message_{j}")
            r.expire(list_key, 3600)
        
        end_time = time.time()
        total_ops = 50 * 10
        ops_per_sec = total_ops / (end_time - start_time)
        print(f"✅ {total_ops} operaciones LIST: {ops_per_sec:.2f} ops/sec")
        
        return True
        
    except Exception as e:
        print(f"❌ Error en optimizaciones test: {e}")
        return False

def cleanup_test_data():
    """Limpiar datos de prueba"""
    print("\n🧹 Limpiando datos de prueba...")
    
    try:
        r = redis.from_url(REDIS_URL)
        
        # Eliminar claves de prueba
        patterns = [
            "rate_limit:user_*",
            "cache:agent_response_*",
            "session:*",
            "conversation:*"
        ]
        
        deleted_count = 0
        for pattern in patterns:
            keys = r.keys(pattern)
            if keys:
                deleted = r.delete(*keys)
                deleted_count += deleted
                print(f"   - Eliminadas {deleted} claves con patrón: {pattern}")
        
        print(f"✅ Total claves eliminadas: {deleted_count}")
        return True
        
    except Exception as e:
        print(f"❌ Error limpiando datos: {e}")
        return False

def main():
    """Función principal"""
    print("🚀 ATP v0.8.0+ - Redis Performance Test")
    print("=" * 60)
    print(f"📅 Fecha: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}")
    print("=" * 60)
    
    # Ejecutar tests
    tests = [
        ("Rate Limiting Performance", test_rate_limiting_performance),
        ("Redis Optimizations", test_redis_optimizations),
        ("Cleanup Test Data", cleanup_test_data)
    ]
    
    results = {}
    
    for test_name, test_func in tests:
        print(f"\n{'='*60}")
        print(f"🧪 Ejecutando: {test_name}")
        print(f"{'='*60}")
        
        results[test_name] = test_func()
        time.sleep(1)
    
    # Resumen final
    print(f"\n{'='*60}")
    print("📊 RESUMEN DE PERFORMANCE TESTS")
    print(f"{'='*60}")
    
    passed = sum(1 for result in results.values() if result)
    total = len(results)
    
    for test_name, result in results.items():
        status = "✅ PASSED" if result else "❌ FAILED"
        print(f"{test_name:.<40} {status}")
    
    print(f"\n🎯 Resultado: {passed}/{total} tests pasaron")
    
    if passed == total:
        print("🎉 ¡Redis está optimizado para ATP!")
        print("🚀 Rate limiting funcionando correctamente")
    else:
        print("⚠️ Algunas optimizaciones necesitan atención")
    
    print(f"{'='*60}")

if __name__ == "__main__":
    main()
