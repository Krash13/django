from django.utils import timezone
from rest_framework.exceptions import NotAuthenticated, AuthenticationFailed
from ..models import ClientSystem, ClientSystemToken


class TokenBaseAPIMixin:
    """Класс дополнительного поведения интегрирующий проверки авторизации

    Добавляет проверку перед выполнением действий какого либо другого класса запроса
    """

    def check_permissions(self, request):
        """
        Функция проверки прав на выполнение запроса

        Args:
            request (Request):  объект запроса

        Returns:
            bool: флаг разрешающий выполнения обработки запроса.
        """
        self.token = None
        if 'Authorization' not in request.headers:
            raise NotAuthenticated(detail='Does not exist Authorization key in request.headers')
        if 'Token' not in request.headers['Authorization']:
            raise NotAuthenticated(detail='Bad format at Authorization key in request.headers')
        token = request.headers['Authorization'].split(' ')[1]
        try:
            self.token = ClientSystemToken.objects.get(
                current=token,
                last_use__gt=timezone.now() - timezone.timedelta(minutes=10)
            )
        except ClientSystem.DoesNotExist:
            raise AuthenticationFailed(detail='Bad temporary api token')
        return super().check_permissions(request)
