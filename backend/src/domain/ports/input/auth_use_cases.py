from abc import ABC, abstractmethod
from dataclasses import dataclass
from typing import Dict, Any, Optional

@dataclass
class LoginInputDTO:
    username: str
    password: str

@dataclass
class RegisterInputDTO:
    username: str
    email: str
    password: str

@dataclass
class AuthResponseDTO:
    access_token: str
    user: Dict[str, Any]
    expires_in: int

class LoginUseCasePort(ABC):
    @abstractmethod
    async def execute(self, input: LoginInputDTO) -> AuthResponseDTO:
        pass

class RegisterUseCasePort(ABC):
    @abstractmethod
    async def execute(self, input: RegisterInputDTO) -> AuthResponseDTO:
        pass
