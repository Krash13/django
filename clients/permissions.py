"""
Модуль хранящий классы проверки прав на доступ к обработчикам запроса

Permissions:
    IsClientSystem: Класс прав, проверяющий отправлен ли запрос от имени авторизованной клиентской системы.
"""
from rest_framework.permissions import BasePermission


class IsClientSystem(BasePermission):
    """Класс прав, проверяющий отправлен ли запрос от имени авторизованной клиентской системы.
    """

    def has_permission(self, request, view):
        """Проверка прав доступа к обработчику не связанному с объектом, проверяется авторизация клиентской системы.

        Args:
            request (Request): Объект запроса
            view (View): Объект обработчика запроса

        Returns:
            bool: флаг доступа
        """
        if hasattr(request.user, 'is_system') and request.user.is_system and request.user.client is not None:
            return True
        return False

    def has_object_permission(self, request, view, obj):
        """Проверка прав доступа к обработчику связанному с объектом, проверяется авторизация клиентской системы.

        Args:
            request (Request): Объект запроса
            view (View): Объект обработчика запроса
            obj: объект, с которым работает обработчик

        Returns:
            bool: флаг доступа
        """
        return self.has_permission(request, view)


class IsTeacherPermission(BasePermission):
    """Класс прав, проверяющий отправлен ли запрос от имени авторизованной клиентской системы.
    """

    def has_permission(self, request, view):
        """Проверка прав доступа к обработчику не связанному с объектом, проверяется авторизация клиентской системы.

        Args:
            request (Request): Объект запроса
            view (View): Объект обработчика запроса

        Returns:
            bool: флаг доступа
        """
        if hasattr(request.user, 'is_teacher') and request.user.is_teacher:
            return True
        return False

    def has_object_permission(self, request, view, obj):
        """Проверка прав доступа к обработчику связанному с объектом, проверяется авторизация клиентской системы.

        Args:
            request (Request): Объект запроса
            view (View): Объект обработчика запроса
            obj: объект, с которым работает обработчик

        Returns:
            bool: флаг доступа
        """
        return self.has_permission(request, view)


class IsStudentPermission(BasePermission):
    """Класс прав, проверяющий отправлен ли запрос от имени авторизованной клиентской системы.
    """

    def has_permission(self, request, view):
        """Проверка прав доступа к обработчику не связанному с объектом, проверяется авторизация клиентской системы.

        Args:
            request (Request): Объект запроса
            view (View): Объект обработчика запроса

        Returns:
            bool: флаг доступа
        """
        if hasattr(request.user, 'is_student') and request.user.is_student:
            return True
        return False

    def has_object_permission(self, request, view, obj):
        """Проверка прав доступа к обработчику связанному с объектом, проверяется авторизация клиентской системы.

        Args:
            request (Request): Объект запроса
            view (View): Объект обработчика запроса
            obj: объект, с которым работает обработчик

        Returns:
            bool: флаг доступа
        """
        return self.has_permission(request, view)
