import sqlite3
import json
from typing import List, Optional
from src.domain.entities.conversation import Conversation
from src.domain.ports.output.conversation_repository import ConversationRepositoryPort

class SQLiteConversationRepository(ConversationRepositoryPort):
    def __init__(self, db_path: str):
        self.db_path = db_path

    def _get_connection(self):
        conn = sqlite3.connect(self.db_path)
        conn.row_factory = sqlite3.Row
        return conn

    def save(self, conversation: Conversation) -> None:
        conn = self._get_connection()
        cursor = conn.cursor()
        
        messages_json = json.dumps(conversation.messages)
        agents_json = json.dumps(conversation.agents)
        
        cursor.execute("""
            INSERT OR REPLACE INTO conversations 
            (user_id, conversation_id, title, messages, model, agents, created_at, updated_at)
            VALUES (?, ?, ?, ?, ?, ?, ?, ?)
        """, (
            conversation.user_id, 
            conversation.conversation_id, 
            conversation.title, 
            messages_json, 
            conversation.model, 
            agents_json,
            conversation.created_at.isoformat() if hasattr(conversation.created_at, 'isoformat') else conversation.created_at,
            conversation.updated_at.isoformat() if hasattr(conversation.updated_at, 'isoformat') else conversation.updated_at
        ))
        
        conn.commit()
        conn.close()

    def find_by_conversation_id(self, conv_id: str, user_id: int) -> Optional[Conversation]:
        conn = self._get_connection()
        cursor = conn.cursor()
        cursor.execute("SELECT * FROM conversations WHERE conversation_id = ? AND user_id = ?", (conv_id, user_id))
        row = cursor.fetchone()
        conn.close()
        
        if not row:
            return None
            
        return Conversation(
            id=row["id"],
            user_id=row["user_id"],
            conversation_id=row["conversation_id"],
            title=row["title"],
            messages=json.loads(row["messages"]) if row["messages"] else [],
            model=row["model"],
            agents=json.loads(row["agents"]) if row["agents"] else [],
            created_at=row["created_at"],
            updated_at=row["updated_at"]
        )

    def find_by_user(self, user_id: int) -> List[Conversation]:
        conn = self._get_connection()
        cursor = conn.cursor()
        cursor.execute("""
            SELECT conversation_id, title, created_at, updated_at, model, agents 
            FROM conversations WHERE user_id = ? 
            ORDER BY updated_at DESC
        """, (user_id,))
        
        rows = cursor.fetchall()
        conn.close()
        
        conversations = []
        for row in rows:
            conversations.append(Conversation(
                id=None,
                user_id=user_id,
                conversation_id=row["conversation_id"],
                title=row["title"],
                messages=[], # No cargar mensajes para el resumen
                model=row["model"],
                agents=json.loads(row["agents"]) if row["agents"] else [],
                created_at=row["created_at"],
                updated_at=row["updated_at"]
            ))
        return conversations

    def delete(self, conv_id: str, user_id: int) -> bool:
        conn = self._get_connection()
        cursor = conn.cursor()
        cursor.execute("DELETE FROM conversations WHERE conversation_id = ? AND user_id = ?", (conv_id, user_id))
        deleted = cursor.rowcount > 0
        conn.commit()
        conn.close()
        return deleted
