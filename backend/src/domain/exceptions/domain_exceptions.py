class DomainException(Exception):
    """Clase base para todas las excepciones del dominio"""
    pass

class UnauthorizedException(DomainException):
    pass

class ValidationException(DomainException):
    pass

class EntityNotFoundException(DomainException):
    pass
