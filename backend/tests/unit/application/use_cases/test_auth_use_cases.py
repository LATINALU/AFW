import pytest
from unittest.mock import MagicMock, AsyncMock
from src.application.use_cases.auth_use_cases import LoginUseCase, LoginInputDTO
from src.domain.ports.output.user_repository import UserRepositoryPort
from src.shared.password_hasher import PasswordHasherPort
from src.domain.entities.user import User
from src.domain.exceptions.domain_exceptions import UnauthorizedException

@pytest.fixture
def mock_user_repo():
    return MagicMock(spec=UserRepositoryPort)

@pytest.fixture
def mock_hasher():
    return MagicMock(spec=PasswordHasherPort)

@pytest.fixture
def login_use_case(mock_user_repo, mock_hasher):
    return LoginUseCase(mock_user_repo, mock_hasher)

@pytest.mark.asyncio
async def test_login_success(login_use_case, mock_user_repo, mock_hasher):
    # Arrange
    username = "testuser"
    password = "CorrectPassword123"
    password_hash = "hashed_password"
    user = User(
        id=1,
        username=username,
        email="test@example.com",
        password_hash=password_hash,
        user_code="UC123",
        role="free"
    )
    
    mock_user_repo.find_by_username.return_value = user
    mock_hasher.verify.return_value = True
    
    input_dto = LoginInputDTO(username=username, password=password)
    
    # Act
    result = await login_use_case.execute(input_dto)
    
    # Assert
    assert result.user["username"] == username
    assert result.access_token is not None
    mock_user_repo.find_by_username.assert_called_once_with(username)
    mock_hasher.verify.assert_called_once_with(password, password_hash)

@pytest.mark.asyncio
async def test_login_user_not_found(login_use_case, mock_user_repo):
    # Arrange
    mock_user_repo.find_by_username.return_value = None
    input_dto = LoginInputDTO(username="nonexistent", password="any")
    
    # Act & Assert
    with pytest.raises(UnauthorizedException) as exc:
        await login_use_case.execute(input_dto)
    assert "inválidas" in str(exc.value)

@pytest.mark.asyncio
async def test_login_invalid_password(login_use_case, mock_user_repo, mock_hasher):
    # Arrange
    user = User(1, "user", "e", "hash", "code")
    mock_user_repo.find_by_username.return_value = user
    mock_hasher.verify.return_value = False
    
    input_dto = LoginInputDTO(username="user", password="wrong")
    
    # Act & Assert
    with pytest.raises(UnauthorizedException):
        await login_use_case.execute(input_dto)

@pytest.fixture
def register_use_case(mock_user_repo, mock_hasher):
    from src.application.use_cases.auth_use_cases import RegisterUseCase
    return RegisterUseCase(mock_user_repo, mock_hasher)

@pytest.mark.asyncio
async def test_register_success(register_use_case, mock_user_repo, mock_hasher):
    # Arrange
    from src.application.use_cases.auth_use_cases import RegisterInputDTO
    username = "newuser"
    password = "Password123!"
    input_dto = RegisterInputDTO(username=username, email="new@example.com", password=password)
    
    user = User(1, username, "new@example.com", "hashed_pass", "code")
    
    # First call to find_by_username returns None (doesn't exist), second call (during login) returns the user
    mock_user_repo.find_by_username.side_effect = [None, user]
    mock_user_repo.find_by_email.return_value = None
    mock_user_repo.save.return_value = user
    mock_hasher.hash.return_value = "hashed_pass"
    mock_hasher.verify.return_value = True
    
    # Act
    result = await register_use_case.execute(input_dto)
    
    # Assert
    assert result.user["username"] == username
    assert mock_user_repo.save.called
    mock_hasher.hash.assert_called_once_with(password)
