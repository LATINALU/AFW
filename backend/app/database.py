"""
ATP v0.8.0+ - Database System with User Management
==================================================
Sistema de base de datos con gestión de usuarios, roles y suscripciones
"""

import sqlite3
import hashlib
import secrets
import json
from datetime import datetime, timedelta
from typing import Optional, Dict, List, Any
from pathlib import Path

# Configuración de base de datos
DB_PATH = Path(__file__).parent.parent / "data" / "atp_users.db"
DB_PATH.parent.mkdir(parents=True, exist_ok=True)

class UserRole:
    """Roles de usuario"""
    ADMIN = "admin"
    PREMIUM = "premium"
    FREE = "free"

class SubscriptionPlan:
    """Planes de suscripción"""
    ADMIN = {
        "name": "Admin",
        "monthly_queries": -1,  # Ilimitado
        "max_agents": -1,
        "price": 0,
        "features": ["unlimited_queries", "all_agents", "admin_panel", "user_management"]
    }
    PREMIUM = {
        "name": "Premium",
        "monthly_queries": 1000,
        "max_agents": 30,
        "price": 29.99,
        "features": ["1000_queries", "all_agents", "priority_support", "conversation_history"]
    }
    FREE = {
        "name": "Free",
        "monthly_queries": 10,
        "max_agents": 5,
        "price": 0,
        "features": ["10_queries", "5_agents", "basic_support"]
    }

class Database:
    """Gestor de base de datos"""
    
    def __init__(self, db_path: str = str(DB_PATH)):
        self.db_path = db_path
        self.init_database()
    
    def get_connection(self):
        """Obtener conexión a la base de datos"""
        conn = sqlite3.connect(self.db_path)
        conn.row_factory = sqlite3.Row
        return conn
    
    def init_database(self):
        """Inicializar base de datos con tablas"""
        conn = self.get_connection()
        cursor = conn.cursor()
        
        # Tabla de usuarios
        cursor.execute("""
            CREATE TABLE IF NOT EXISTS users (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                username TEXT UNIQUE NOT NULL,
                email TEXT UNIQUE NOT NULL,
                password_hash TEXT NOT NULL,
                user_code TEXT UNIQUE NOT NULL,
                role TEXT NOT NULL DEFAULT 'free',
                created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
                updated_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
                last_login TIMESTAMP,
                is_active BOOLEAN DEFAULT 1,
                created_by INTEGER,
                FOREIGN KEY (created_by) REFERENCES users(id)
            )
        """)
        
        # Tabla de uso/límites
        cursor.execute("""
            CREATE TABLE IF NOT EXISTS user_usage (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                user_id INTEGER NOT NULL,
                month TEXT NOT NULL,
                queries_used INTEGER DEFAULT 0,
                last_reset TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
                FOREIGN KEY (user_id) REFERENCES users(id),
                UNIQUE(user_id, month)
            )
        """)
        
        # Tabla de suscripciones
        cursor.execute("""
            CREATE TABLE IF NOT EXISTS subscriptions (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                user_id INTEGER NOT NULL,
                plan TEXT NOT NULL,
                status TEXT NOT NULL DEFAULT 'active',
                start_date TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
                end_date TIMESTAMP,
                payment_method TEXT,
                amount REAL,
                FOREIGN KEY (user_id) REFERENCES users(id)
            )
        """)
        
        # Tabla de conversaciones
        cursor.execute("""
            CREATE TABLE IF NOT EXISTS conversations (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                user_id INTEGER NOT NULL,
                conversation_id TEXT UNIQUE NOT NULL,
                title TEXT NOT NULL,
                messages TEXT,
                created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
                updated_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
                model TEXT,
                agents TEXT,
                FOREIGN KEY (user_id) REFERENCES users(id)
            )
        """)
        
        # Tabla de sesiones
        cursor.execute("""
            CREATE TABLE IF NOT EXISTS sessions (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                user_id INTEGER NOT NULL,
                session_token TEXT UNIQUE NOT NULL,
                client_id TEXT,
                ip_address TEXT,
                user_agent TEXT,
                created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
                expires_at TIMESTAMP NOT NULL,
                is_active BOOLEAN DEFAULT 1,
                FOREIGN KEY (user_id) REFERENCES users(id)
            )
        """)
        
        conn.commit()
        conn.close()
        
        # Crear usuario admin por defecto si no existe
        self.create_default_admin()
    
    def generate_user_code(self) -> str:
        """Generar código único de usuario #XXXX"""
        while True:
            code = f"#{secrets.token_hex(2).upper()}"
            if not self.get_user_by_code(code):
                return code
    
    def hash_password(self, password: str) -> str:
        """Hash de contraseña con salt"""
        salt = secrets.token_hex(16)
        pwd_hash = hashlib.pbkdf2_hmac('sha256', password.encode(), salt.encode(), 100000)
        return f"{salt}${pwd_hash.hex()}"
    
    def verify_password(self, password: str, password_hash: str) -> bool:
        """Verificar contraseña"""
        try:
            salt, pwd_hash = password_hash.split('$')
            new_hash = hashlib.pbkdf2_hmac('sha256', password.encode(), salt.encode(), 100000)
            return new_hash.hex() == pwd_hash
        except:
            return False
    
    def create_user(self, username: str, email: str, password: str, 
                   role: str = UserRole.FREE, created_by: Optional[int] = None) -> Dict[str, Any]:
        """Crear nuevo usuario"""
        conn = self.get_connection()
        cursor = conn.cursor()
        
        try:
            user_code = self.generate_user_code()
            password_hash = self.hash_password(password)
            
            cursor.execute("""
                INSERT INTO users (username, email, password_hash, user_code, role, created_by)
                VALUES (?, ?, ?, ?, ?, ?)
            """, (username, email, password_hash, user_code, role, created_by))
            
            user_id = cursor.lastrowid
            
            # Crear registro de uso inicial
            current_month = datetime.now().strftime("%Y-%m")
            cursor.execute("""
                INSERT INTO user_usage (user_id, month, queries_used)
                VALUES (?, ?, 0)
            """, (user_id, current_month))
            
            # Crear suscripción inicial
            plan = SubscriptionPlan.ADMIN if role == UserRole.ADMIN else \
                   SubscriptionPlan.PREMIUM if role == UserRole.PREMIUM else \
                   SubscriptionPlan.FREE
            
            cursor.execute("""
                INSERT INTO subscriptions (user_id, plan, status, amount)
                VALUES (?, ?, 'active', ?)
            """, (user_id, role, plan["price"]))
            
            conn.commit()
            
            return {
                "id": user_id,
                "username": username,
                "email": email,
                "user_code": user_code,
                "role": role,
                "created_at": datetime.now().isoformat()
            }
        except sqlite3.IntegrityError as e:
            conn.rollback()
            raise ValueError(f"Usuario o email ya existe: {e}")
        finally:
            conn.close()
    
    def create_default_admin(self):
        """Crear usuario admin por defecto"""
        try:
            # Verificar si ya existe un admin
            conn = self.get_connection()
            cursor = conn.cursor()
            cursor.execute("SELECT id FROM users WHERE role = 'admin' LIMIT 1")
            if cursor.fetchone():
                conn.close()
                return
            conn.close()
            
            # Crear admin con credenciales por defecto
            admin = self.create_user(
                username="admin",
                email="admin@atp.local",
                password="Admin123!",  # CAMBIAR EN PRODUCCIÓN
                role=UserRole.ADMIN
            )
            print(f"✅ Usuario admin creado: {admin['username']} | Código: {admin['user_code']}")
            print("⚠️ IMPORTANTE: Cambiar contraseña por defecto 'Admin123!'")
        except ValueError:
            pass  # Admin ya existe
    
    def authenticate_user(self, username: str, password: str) -> Optional[Dict[str, Any]]:
        """Autenticar usuario"""
        conn = self.get_connection()
        cursor = conn.cursor()
        
        cursor.execute("""
            SELECT id, username, email, password_hash, user_code, role, is_active
            FROM users WHERE username = ? OR email = ?
        """, (username, username))
        
        user = cursor.fetchone()
        conn.close()
        
        if not user:
            return None
        
        if not user['is_active']:
            raise ValueError("Usuario inactivo")
        
        if not self.verify_password(password, user['password_hash']):
            return None
        
        # Actualizar último login
        self.update_last_login(user['id'])
        
        return {
            "id": user['id'],
            "username": user['username'],
            "email": user['email'],
            "user_code": user['user_code'],
            "role": user['role']
        }
    
    def get_user_by_id(self, user_id: int) -> Optional[Dict[str, Any]]:
        """Obtener usuario por ID"""
        conn = self.get_connection()
        cursor = conn.cursor()
        
        cursor.execute("""
            SELECT id, username, email, user_code, role, created_at, last_login, is_active
            FROM users WHERE id = ?
        """, (user_id,))
        
        user = cursor.fetchone()
        conn.close()
        
        if user:
            return dict(user)
        return None
    
    def get_user_by_code(self, user_code: str) -> Optional[Dict[str, Any]]:
        """Obtener usuario por código"""
        conn = self.get_connection()
        cursor = conn.cursor()
        
        cursor.execute("""
            SELECT id, username, email, user_code, role, is_active
            FROM users WHERE user_code = ?
        """, (user_code,))
        
        user = cursor.fetchone()
        conn.close()
        
        if user:
            return dict(user)
        return None
    
    def update_last_login(self, user_id: int):
        """Actualizar último login"""
        conn = self.get_connection()
        cursor = conn.cursor()
        
        cursor.execute("""
            UPDATE users SET last_login = CURRENT_TIMESTAMP
            WHERE id = ?
        """, (user_id,))
        
        conn.commit()
        conn.close()
    
    def check_query_limit(self, user_id: int) -> Dict[str, Any]:
        """Verificar límite de consultas"""
        user = self.get_user_by_id(user_id)
        if not user:
            raise ValueError("Usuario no encontrado")
        
        # Obtener plan del usuario
        plan = SubscriptionPlan.ADMIN if user['role'] == UserRole.ADMIN else \
               SubscriptionPlan.PREMIUM if user['role'] == UserRole.PREMIUM else \
               SubscriptionPlan.FREE
        
        # Si es ilimitado (admin)
        if plan["monthly_queries"] == -1:
            return {
                "allowed": True,
                "queries_used": 0,
                "queries_limit": -1,
                "queries_remaining": -1
            }
        
        # Obtener uso del mes actual
        conn = self.get_connection()
        cursor = conn.cursor()
        current_month = datetime.now().strftime("%Y-%m")
        
        cursor.execute("""
            SELECT queries_used FROM user_usage
            WHERE user_id = ? AND month = ?
        """, (user_id, current_month))
        
        usage = cursor.fetchone()
        conn.close()
        
        if not usage:
            # Crear registro si no existe
            conn = self.get_connection()
            cursor = conn.cursor()
            cursor.execute("""
                INSERT INTO user_usage (user_id, month, queries_used)
                VALUES (?, ?, 0)
            """, (user_id, current_month))
            conn.commit()
            conn.close()
            queries_used = 0
        else:
            queries_used = usage['queries_used']
        
        queries_limit = plan["monthly_queries"]
        queries_remaining = queries_limit - queries_used
        
        return {
            "allowed": queries_remaining > 0,
            "queries_used": queries_used,
            "queries_limit": queries_limit,
            "queries_remaining": queries_remaining
        }
    
    def increment_query_count(self, user_id: int) -> bool:
        """Incrementar contador de consultas"""
        limit_check = self.check_query_limit(user_id)
        
        if not limit_check["allowed"]:
            raise ValueError("Límite de consultas alcanzado")
        
        conn = self.get_connection()
        cursor = conn.cursor()
        current_month = datetime.now().strftime("%Y-%m")
        
        cursor.execute("""
            UPDATE user_usage
            SET queries_used = queries_used + 1
            WHERE user_id = ? AND month = ?
        """, (user_id, current_month))
        
        conn.commit()
        conn.close()
        return True
    
    def get_all_users(self, admin_id: int) -> List[Dict[str, Any]]:
        """Obtener todos los usuarios (solo admin)"""
        admin = self.get_user_by_id(admin_id)
        if not admin or admin['role'] != UserRole.ADMIN:
            raise ValueError("Solo administradores pueden ver todos los usuarios")
        
        conn = self.get_connection()
        cursor = conn.cursor()
        
        cursor.execute("""
            SELECT id, username, email, user_code, role, created_at, last_login, is_active
            FROM users
            ORDER BY created_at DESC
        """)
        
        users = [dict(row) for row in cursor.fetchall()]
        conn.close()
        
        return users
    
    def save_conversation(self, user_id: int, conversation_id: str, 
                         title: str, messages: List[Dict], model: str, agents: List[str]):
        """Guardar conversación"""
        conn = self.get_connection()
        cursor = conn.cursor()
        
        messages_json = json.dumps(messages)
        agents_json = json.dumps(agents)
        
        cursor.execute("""
            INSERT OR REPLACE INTO conversations 
            (user_id, conversation_id, title, messages, model, agents, updated_at)
            VALUES (?, ?, ?, ?, ?, ?, CURRENT_TIMESTAMP)
        """, (user_id, conversation_id, title, messages_json, model, agents_json))
        
        conn.commit()
        conn.close()
    
    def get_user_conversations(self, user_id: int) -> List[Dict[str, Any]]:
        """Obtener conversaciones del usuario"""
        conn = self.get_connection()
        cursor = conn.cursor()
        
        cursor.execute("""
            SELECT conversation_id, title, created_at, updated_at, model, agents
            FROM conversations
            WHERE user_id = ?
            ORDER BY updated_at DESC
        """, (user_id,))
        
        conversations = []
        for row in cursor.fetchall():
            conv = dict(row)
            conv['agents'] = json.loads(conv['agents']) if conv['agents'] else []
            conversations.append(conv)
        
        conn.close()
        return conversations

# Instancia global
db = Database()

__all__ = ['Database', 'db', 'UserRole', 'SubscriptionPlan']
