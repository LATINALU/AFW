import re
from src.domain.exceptions.domain_exceptions import ValidationException

class Email:
    def __init__(self, value: str):
        if not value or not re.match(r"[^@]+@[^@]+\.[^@]+", value):
            raise ValidationException(f"Email inválido: {value}")
        self._value = value

    def get_value(self) -> str:
        return self._value

    def __eq__(self, other):
        if not isinstance(other, Email):
            return False
        return self._value == other._value

class UserRole:
    ADMIN = "admin"
    PREMIUM = "premium"
    FREE = "free"

    @classmethod
    def validate(cls, role: str):
        if role not in [cls.ADMIN, cls.PREMIUM, cls.FREE]:
            raise ValidationException(f"Rol inválido: {role}")
        return role
