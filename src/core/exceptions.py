# src/core/exceptions.py

class ApplicationException(Exception):
    """
    Базовый класс для всех кастомных исключений в приложении.
    """
    @property
    def message(self) -> str:
        """Сообщение об ошибке по умолчанию."""
        return "Произошла непредвиденная ошибка в приложении."

    def __str__(self):
        return self.message


class NotFoundException(ApplicationException):
    """
    Выбрасывается, когда запрашиваемый объект не может быть найден.
    """
    def __init__(self, name: str = "Объект"):
        self.name = name

    @property
    def message(self) -> str:
        return f"{self.name} не найден."


class BadRequestException(ApplicationException):
    """
    Выбрасывается, когда запрос или действие некорректны с точки зрения
    бизнес-логики.
    """
    def __init__(self, reason: str):
        self.reason = reason

    @property
    def message(self) -> str:
        return self.reason
