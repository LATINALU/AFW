"""
Conversation Service v1.0.0
===========================
Servicio para gestión de conversaciones y respuestas guardadas.
Optimizado para alta concurrencia.
"""

import sqlite3
import json
import uuid
from datetime import datetime
from typing import List, Dict, Optional, Any
from pathlib import Path
import asyncio
from concurrent.futures import ThreadPoolExecutor

# Pool de threads para operaciones de DB
executor = ThreadPoolExecutor(max_workers=10)

DB_PATH = Path(__file__).parent.parent.parent / "data" / "atp_conversations.db"
DB_PATH.parent.mkdir(parents=True, exist_ok=True)


class ConversationService:
    """
    Servicio de gestión de conversaciones y respuestas guardadas.
    
    Características:
    - Guardado automático de conversaciones
    - Historial como ChatGPT/Gemini
    - Guardar respuestas individuales
    - Búsqueda y filtrado
    - Optimizado para concurrencia
    """
    
    def __init__(self, db_path: str = str(DB_PATH)):
        self.db_path = db_path
        self.init_database()
    
    def get_connection(self):
        """Obtener conexión thread-safe a la base de datos"""
        conn = sqlite3.connect(self.db_path, check_same_thread=False)
        conn.row_factory = sqlite3.Row
        # Optimizaciones para concurrencia
        conn.execute("PRAGMA journal_mode=WAL")
        conn.execute("PRAGMA synchronous=NORMAL")
        conn.execute("PRAGMA cache_size=10000")
        conn.execute("PRAGMA temp_store=MEMORY")
        return conn
    
    def init_database(self):
        """Inicializar base de datos con tablas optimizadas"""
        conn = self.get_connection()
        cursor = conn.cursor()
        
        # Tabla de conversaciones
        cursor.execute("""
            CREATE TABLE IF NOT EXISTS conversations (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                conversation_id TEXT UNIQUE NOT NULL,
                user_id TEXT NOT NULL,
                title TEXT NOT NULL,
                created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
                updated_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
                message_count INTEGER DEFAULT 0,
                model TEXT,
                agents TEXT,
                is_pinned BOOLEAN DEFAULT 0,
                is_archived BOOLEAN DEFAULT 0
            )
        """)
        
        # Tabla de mensajes (separada para mejor performance)
        cursor.execute("""
            CREATE TABLE IF NOT EXISTS messages (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                message_id TEXT UNIQUE NOT NULL,
                conversation_id TEXT NOT NULL,
                role TEXT NOT NULL,
                content TEXT NOT NULL,
                agent_id TEXT,
                timestamp TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
                metadata TEXT,
                FOREIGN KEY (conversation_id) REFERENCES conversations(conversation_id)
            )
        """)
        
        # Tabla de respuestas guardadas
        cursor.execute("""
            CREATE TABLE IF NOT EXISTS saved_responses (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                response_id TEXT UNIQUE NOT NULL,
                user_id TEXT NOT NULL,
                conversation_id TEXT,
                message_id TEXT,
                agent_id TEXT NOT NULL,
                agent_name TEXT NOT NULL,
                content TEXT NOT NULL,
                title TEXT,
                tags TEXT,
                created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
                is_favorite BOOLEAN DEFAULT 0,
                category TEXT,
                FOREIGN KEY (conversation_id) REFERENCES conversations(conversation_id),
                FOREIGN KEY (message_id) REFERENCES messages(message_id)
            )
        """)
        
        # Índices para mejor performance
        cursor.execute("""
            CREATE INDEX IF NOT EXISTS idx_conversations_user 
            ON conversations(user_id, updated_at DESC)
        """)
        
        cursor.execute("""
            CREATE INDEX IF NOT EXISTS idx_conversations_archived 
            ON conversations(user_id, is_archived, updated_at DESC)
        """)
        
        cursor.execute("""
            CREATE INDEX IF NOT EXISTS idx_messages_conversation 
            ON messages(conversation_id, timestamp ASC)
        """)
        
        cursor.execute("""
            CREATE INDEX IF NOT EXISTS idx_saved_responses_user 
            ON saved_responses(user_id, created_at DESC)
        """)
        
        cursor.execute("""
            CREATE INDEX IF NOT EXISTS idx_saved_responses_category 
            ON saved_responses(user_id, category, created_at DESC)
        """)
        
        conn.commit()
        conn.close()
        print("✅ Conversation database initialized")
    
    async def create_conversation(
        self,
        user_id: str,
        title: str,
        model: Optional[str] = None,
        agents: Optional[List[str]] = None
    ) -> str:
        """
        Crea una nueva conversación.
        
        Args:
            user_id: ID del usuario
            title: Título de la conversación
            model: Modelo usado
            agents: Lista de agentes
            
        Returns:
            ID de la conversación creada
        """
        conversation_id = f"conv_{uuid.uuid4().hex[:16]}"
        
        def _create():
            conn = self.get_connection()
            cursor = conn.cursor()
            
            cursor.execute("""
                INSERT INTO conversations 
                (conversation_id, user_id, title, model, agents)
                VALUES (?, ?, ?, ?, ?)
            """, (
                conversation_id,
                user_id,
                title,
                model,
                json.dumps(agents) if agents else None
            ))
            
            conn.commit()
            conn.close()
        
        await asyncio.get_event_loop().run_in_executor(executor, _create)
        return conversation_id
    
    async def add_message(
        self,
        conversation_id: str,
        role: str,
        content: str,
        agent_id: Optional[str] = None,
        metadata: Optional[Dict] = None
    ) -> str:
        """
        Agrega un mensaje a una conversación.
        
        Args:
            conversation_id: ID de la conversación
            role: 'user' o 'assistant'
            content: Contenido del mensaje
            agent_id: ID del agente (si es respuesta)
            metadata: Metadata adicional
            
        Returns:
            ID del mensaje creado
        """
        message_id = f"msg_{uuid.uuid4().hex[:16]}"
        
        def _add():
            conn = self.get_connection()
            cursor = conn.cursor()
            
            # Insertar mensaje
            cursor.execute("""
                INSERT INTO messages 
                (message_id, conversation_id, role, content, agent_id, metadata)
                VALUES (?, ?, ?, ?, ?, ?)
            """, (
                message_id,
                conversation_id,
                role,
                content,
                agent_id,
                json.dumps(metadata) if metadata else None
            ))
            
            # Actualizar contador y timestamp de conversación
            cursor.execute("""
                UPDATE conversations 
                SET message_count = message_count + 1,
                    updated_at = CURRENT_TIMESTAMP
                WHERE conversation_id = ?
            """, (conversation_id,))
            
            conn.commit()
            conn.close()
        
        await asyncio.get_event_loop().run_in_executor(executor, _add)
        return message_id
    
    async def get_conversations(
        self,
        user_id: str,
        limit: int = 50,
        offset: int = 0,
        include_archived: bool = False
    ) -> List[Dict]:
        """
        Obtiene las conversaciones de un usuario.
        
        Args:
            user_id: ID del usuario
            limit: Número máximo de conversaciones
            offset: Offset para paginación
            include_archived: Incluir archivadas
            
        Returns:
            Lista de conversaciones
        """
        def _get():
            conn = self.get_connection()
            cursor = conn.cursor()
            
            query = """
                SELECT 
                    conversation_id,
                    title,
                    created_at,
                    updated_at,
                    message_count,
                    model,
                    agents,
                    is_pinned,
                    is_archived
                FROM conversations
                WHERE user_id = ?
            """
            
            if not include_archived:
                query += " AND is_archived = 0"
            
            query += " ORDER BY is_pinned DESC, updated_at DESC LIMIT ? OFFSET ?"
            
            cursor.execute(query, (user_id, limit, offset))
            results = cursor.fetchall()
            conn.close()
            
            return [dict(row) for row in results]
        
        return await asyncio.get_event_loop().run_in_executor(executor, _get)
    
    async def get_conversation_messages(
        self,
        conversation_id: str,
        limit: int = 100
    ) -> List[Dict]:
        """
        Obtiene los mensajes de una conversación.
        
        Args:
            conversation_id: ID de la conversación
            limit: Número máximo de mensajes
            
        Returns:
            Lista de mensajes
        """
        def _get():
            conn = self.get_connection()
            cursor = conn.cursor()
            
            cursor.execute("""
                SELECT 
                    message_id,
                    role,
                    content,
                    agent_id,
                    timestamp,
                    metadata
                FROM messages
                WHERE conversation_id = ?
                ORDER BY timestamp ASC
                LIMIT ?
            """, (conversation_id, limit))
            
            results = cursor.fetchall()
            conn.close()
            
            messages = []
            for row in results:
                msg = dict(row)
                if msg['metadata']:
                    msg['metadata'] = json.loads(msg['metadata'])
                messages.append(msg)
            
            return messages
        
        return await asyncio.get_event_loop().run_in_executor(executor, _get)
    
    async def update_conversation_title(
        self,
        conversation_id: str,
        title: str
    ) -> bool:
        """Actualiza el título de una conversación"""
        def _update():
            conn = self.get_connection()
            cursor = conn.cursor()
            
            cursor.execute("""
                UPDATE conversations 
                SET title = ?, updated_at = CURRENT_TIMESTAMP
                WHERE conversation_id = ?
            """, (title, conversation_id))
            
            affected = cursor.rowcount
            conn.commit()
            conn.close()
            return affected > 0
        
        return await asyncio.get_event_loop().run_in_executor(executor, _update)
    
    async def delete_conversation(self, conversation_id: str) -> bool:
        """Elimina una conversación y sus mensajes"""
        def _delete():
            conn = self.get_connection()
            cursor = conn.cursor()
            
            # Eliminar mensajes
            cursor.execute("DELETE FROM messages WHERE conversation_id = ?", (conversation_id,))
            
            # Eliminar conversación
            cursor.execute("DELETE FROM conversations WHERE conversation_id = ?", (conversation_id,))
            
            affected = cursor.rowcount
            conn.commit()
            conn.close()
            return affected > 0
        
        return await asyncio.get_event_loop().run_in_executor(executor, _delete)
    
    async def archive_conversation(
        self,
        conversation_id: str,
        archived: bool = True
    ) -> bool:
        """Archiva o desarchivar una conversación"""
        def _archive():
            conn = self.get_connection()
            cursor = conn.cursor()
            
            cursor.execute("""
                UPDATE conversations 
                SET is_archived = ?, updated_at = CURRENT_TIMESTAMP
                WHERE conversation_id = ?
            """, (1 if archived else 0, conversation_id))
            
            affected = cursor.rowcount
            conn.commit()
            conn.close()
            return affected > 0
        
        return await asyncio.get_event_loop().run_in_executor(executor, _archive)
    
    async def pin_conversation(
        self,
        conversation_id: str,
        pinned: bool = True
    ) -> bool:
        """Fija o desfija una conversación"""
        def _pin():
            conn = self.get_connection()
            cursor = conn.cursor()
            
            cursor.execute("""
                UPDATE conversations 
                SET is_pinned = ?, updated_at = CURRENT_TIMESTAMP
                WHERE conversation_id = ?
            """, (1 if pinned else 0, conversation_id))
            
            affected = cursor.rowcount
            conn.commit()
            conn.close()
            return affected > 0
        
        return await asyncio.get_event_loop().run_in_executor(executor, _pin)
    
    async def save_response(
        self,
        user_id: str,
        agent_id: str,
        agent_name: str,
        content: str,
        title: Optional[str] = None,
        conversation_id: Optional[str] = None,
        message_id: Optional[str] = None,
        tags: Optional[List[str]] = None,
        category: Optional[str] = None
    ) -> str:
        """
        Guarda una respuesta individual de un agente.
        
        Args:
            user_id: ID del usuario
            agent_id: ID del agente
            agent_name: Nombre del agente
            content: Contenido de la respuesta
            title: Título personalizado
            conversation_id: ID de conversación origen
            message_id: ID del mensaje origen
            tags: Tags para organización
            category: Categoría
            
        Returns:
            ID de la respuesta guardada
        """
        response_id = f"resp_{uuid.uuid4().hex[:16]}"
        
        def _save():
            conn = self.get_connection()
            cursor = conn.cursor()
            
            cursor.execute("""
                INSERT INTO saved_responses 
                (response_id, user_id, conversation_id, message_id, 
                 agent_id, agent_name, content, title, tags, category)
                VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?)
            """, (
                response_id,
                user_id,
                conversation_id,
                message_id,
                agent_id,
                agent_name,
                content,
                title or f"Respuesta de {agent_name}",
                json.dumps(tags) if tags else None,
                category
            ))
            
            conn.commit()
            conn.close()
        
        await asyncio.get_event_loop().run_in_executor(executor, _save)
        return response_id
    
    async def get_saved_responses(
        self,
        user_id: str,
        category: Optional[str] = None,
        limit: int = 50,
        offset: int = 0
    ) -> List[Dict]:
        """Obtiene las respuestas guardadas de un usuario"""
        def _get():
            conn = self.get_connection()
            cursor = conn.cursor()
            
            query = """
                SELECT 
                    response_id,
                    agent_id,
                    agent_name,
                    content,
                    title,
                    tags,
                    category,
                    created_at,
                    is_favorite
                FROM saved_responses
                WHERE user_id = ?
            """
            
            params = [user_id]
            
            if category:
                query += " AND category = ?"
                params.append(category)
            
            query += " ORDER BY is_favorite DESC, created_at DESC LIMIT ? OFFSET ?"
            params.extend([limit, offset])
            
            cursor.execute(query, params)
            results = cursor.fetchall()
            conn.close()
            
            responses = []
            for row in results:
                resp = dict(row)
                if resp['tags']:
                    resp['tags'] = json.loads(resp['tags'])
                responses.append(resp)
            
            return responses
        
        return await asyncio.get_event_loop().run_in_executor(executor, _get)
    
    async def delete_saved_response(self, response_id: str) -> bool:
        """Elimina una respuesta guardada"""
        def _delete():
            conn = self.get_connection()
            cursor = conn.cursor()
            
            cursor.execute("DELETE FROM saved_responses WHERE response_id = ?", (response_id,))
            
            affected = cursor.rowcount
            conn.commit()
            conn.close()
            return affected > 0
        
        return await asyncio.get_event_loop().run_in_executor(executor, _delete)
    
    async def search_conversations(
        self,
        user_id: str,
        query: str,
        limit: int = 20
    ) -> List[Dict]:
        """Busca conversaciones por título o contenido"""
        def _search():
            conn = self.get_connection()
            cursor = conn.cursor()
            
            search_pattern = f"%{query}%"
            
            cursor.execute("""
                SELECT DISTINCT
                    c.conversation_id,
                    c.title,
                    c.created_at,
                    c.updated_at,
                    c.message_count
                FROM conversations c
                LEFT JOIN messages m ON c.conversation_id = m.conversation_id
                WHERE c.user_id = ? 
                AND (c.title LIKE ? OR m.content LIKE ?)
                ORDER BY c.updated_at DESC
                LIMIT ?
            """, (user_id, search_pattern, search_pattern, limit))
            
            results = cursor.fetchall()
            conn.close()
            
            return [dict(row) for row in results]
        
        return await asyncio.get_event_loop().run_in_executor(executor, _search)


# Instancia global del servicio
_service_instance: Optional[ConversationService] = None


def get_conversation_service() -> ConversationService:
    """Obtiene la instancia global del servicio (singleton)"""
    global _service_instance
    if _service_instance is None:
        _service_instance = ConversationService()
    return _service_instance
