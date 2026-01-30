import sqlite3
from typing import List, Optional
from src.domain.entities.user import User
from src.domain.ports.output.user_repository import UserRepositoryPort

class SQLiteUserRepository(UserRepositoryPort):
    def __init__(self, db_path: str):
        self.db_path = db_path

    def _get_connection(self):
        conn = sqlite3.connect(self.db_path)
        conn.row_factory = sqlite3.Row
        return conn

    def save(self, user: User) -> User:
        conn = self._get_connection()
        cursor = conn.cursor()
        
        if user.id:
            cursor.execute("""
                UPDATE users SET 
                username = ?, email = ?, password_hash = ?, role = ?, is_active = ?, last_login = ?
                WHERE id = ?
            """, (user.username, user.email, user.password_hash, user.role, user.is_active, 
                  user.last_login.isoformat() if user.last_login else None, user.id))
        else:
            cursor.execute("""
                INSERT INTO users (username, email, password_hash, user_code, role, is_active, created_at)
                VALUES (?, ?, ?, ?, ?, ?, ?)
            """, (user.username, user.email, user.password_hash, user.user_code, user.role, 
                  user.is_active, user.created_at.isoformat()))
            user.id = cursor.lastrowid
            
        conn.commit()
        conn.close()
        return user

    def find_by_id(self, user_id: int) -> Optional[User]:
        conn = self._get_connection()
        cursor = conn.cursor()
        cursor.execute("SELECT * FROM users WHERE id = ?", (user_id,))
        row = cursor.fetchone()
        conn.close()
        return self._map_row_to_user(row)

    def find_by_username(self, username: str) -> Optional[User]:
        conn = self._get_connection()
        cursor = conn.cursor()
        cursor.execute("SELECT * FROM users WHERE username = ?", (username,))
        row = cursor.fetchone()
        conn.close()
        return self._map_row_to_user(row)

    def find_by_email(self, email: str) -> Optional[User]:
        conn = self._get_connection()
        cursor = conn.cursor()
        cursor.execute("SELECT * FROM users WHERE email = ?", (email,))
        row = cursor.fetchone()
        conn.close()
        return self._map_row_to_user(row)

    def find_by_code(self, user_code: str) -> Optional[User]:
        conn = self._get_connection()
        cursor = conn.cursor()
        cursor.execute("SELECT * FROM users WHERE user_code = ?", (user_code,))
        row = cursor.fetchone()
        conn.close()
        return self._map_row_to_user(row)

    def get_all(self, admin_id: int = None) -> List[User]:
        conn = self._get_connection()
        cursor = conn.cursor()
        cursor.execute("SELECT * FROM users")
        rows = cursor.fetchall()
        conn.close()
        return [self._map_row_to_user(row) for row in rows]

    def _map_row_to_user(self, row) -> Optional[User]:
        if not row: return None
        from datetime import datetime
        return User(
            id=row["id"],
            username=row["username"],
            email=row["email"],
            password_hash=row["password_hash"],
            user_code=row["user_code"],
            role=row["role"],
            is_active=row["is_active"],
            created_at=datetime.fromisoformat(row["created_at"]) if isinstance(row["created_at"], str) else row["created_at"],
            last_login=datetime.fromisoformat(row["last_login"]) if row["last_login"] else None
        )
