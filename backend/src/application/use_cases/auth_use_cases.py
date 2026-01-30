import secrets
from src.domain.ports.input.auth_use_cases import LoginUseCasePort, LoginInputDTO, RegisterUseCasePort, RegisterInputDTO, AuthResponseDTO
from src.domain.ports.output.user_repository import UserRepositoryPort
from src.domain.entities.user import User
from src.domain.exceptions.domain_exceptions import UnauthorizedException, ValidationException
from src.shared.password_hasher import PasswordHasherPort
from app.auth import jwt_manager
from datetime import timedelta

class LoginUseCase(LoginUseCasePort):
    def __init__(self, user_repo: UserRepositoryPort, hasher: PasswordHasherPort):
        self.user_repo = user_repo
        self.hasher = hasher

    async def execute(self, input_data: LoginInputDTO) -> AuthResponseDTO:
        user = self.user_repo.find_by_username(input_data.username)
        if not user:
            user = self.user_repo.find_by_email(input_data.username)
            
        if not user or not self.hasher.verify(input_data.password, user.password_hash):
            raise UnauthorizedException("Credenciales inválidas")
            
        if not user.is_active:
            raise UnauthorizedException("Usuario inactivo")
            
        # Generar token
        token_data = {
            "user_id": user.id,
            "username": user.username,
            "role": user.role,
            "user_code": user.user_code
        }
        
        access_token = jwt_manager.create_access_token(
            data=token_data,
            expires_delta=timedelta(hours=24)
        )
        
        return AuthResponseDTO(
            access_token=access_token,
            user={
                "id": user.id,
                "username": user.username,
                "email": user.email,
                "role": user.role,
                "user_code": user.user_code
            },
            expires_in=86400
        )

class RegisterUseCase(RegisterUseCasePort):
    def __init__(self, user_repo: UserRepositoryPort, hasher: PasswordHasherPort):
        self.user_repo = user_repo
        self.hasher = hasher

    async def execute(self, input_data: RegisterInputDTO) -> AuthResponseDTO:
        if self.user_repo.find_by_username(input_data.username):
            raise ValidationException("El nombre de usuario ya existe")
            
        if self.user_repo.find_by_email(input_data.email):
            raise ValidationException("El email ya está registrado")
            
        # Generar código de usuario único
        user_code = self._generate_unique_code()
        
        password_hash = self.hasher.hash(input_data.password)
        
        new_user = User.create(
            username=input_data.username,
            email=input_data.email,
            password_hash=password_hash,
            user_code=user_code,
            role="free"
        )
        
        saved_user = self.user_repo.save(new_user)
        
        # Reutilizar lógica de login para devolver token
        login_use_case = LoginUseCase(self.user_repo, self.hasher)
        return await login_use_case.execute(LoginInputDTO(username=input_data.username, password=input_data.password))

    def _generate_unique_code(self) -> str:
        while True:
            code = f"#{secrets.token_hex(2).upper()}"
            if not self.user_repo.find_by_code(code):
                return code
