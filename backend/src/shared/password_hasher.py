import secrets
import hashlib
from abc import ABC, abstractmethod

class PasswordHasherPort(ABC):
    @abstractmethod
    def hash(self, password: str) -> str:
        pass

    @abstractmethod
    def verify(self, password: str, password_hash: str) -> bool:
        pass

class PBKDF2PasswordHasher(PasswordHasherPort):
    def hash(self, password: str) -> str:
        salt = secrets.token_hex(16)
        pwd_hash = hashlib.pbkdf2_hmac('sha256', password.encode(), salt.encode(), 100000)
        return f"{salt}${pwd_hash.hex()}"

    def verify(self, password: str, password_hash: str) -> bool:
        try:
            salt, pwd_hash = password_hash.split('$')
            new_hash = hashlib.pbkdf2_hmac('sha256', password.encode(), salt.encode(), 100000)
            return new_hash.hex() == pwd_hash
        except Exception:
            return False
