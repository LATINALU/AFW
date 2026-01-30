from datetime import datetime
from typing import Optional, List
from dataclasses import dataclass, field

@dataclass
class User:
    id: Optional[int]
    username: str
    email: str
    password_hash: str
    user_code: str
    role: str = "free"
    is_active: bool = True
    created_at: datetime = field(default_factory=datetime.now)
    last_login: Optional[datetime] = None

    @staticmethod
    def create(username: str, email: str, password_hash: str, user_code: str, role: str = "free") -> 'User':
        # Validaciones de negocio aquí
        if not username or len(username) < 3:
            raise ValueError("Username inválido")
        return User(
            id=None,
            username=username,
            email=email,
            password_hash=password_hash,
            user_code=user_code,
            role=role
        )
