"""
Модуль хранящий прослойки которые выполняются до обработки запроса конкретным обработчиком

Middlewares:
    ClientSystemAuthMiddleware: Django Прослойка добавляющая проверку авторизации клиентских систем для каждого запроса
    DRFClientTokenAuthentication: DRF Прослойка добавляющая проверку авторизации клиентских систем для каждого запроса
"""
from django.utils.deprecation import MiddlewareMixin
from django.utils.functional import SimpleLazyObject
from django.utils.translation import gettext_lazy as _
from django.utils import timezone
from rest_framework import exceptions
from rest_framework.authentication import TokenAuthentication, get_authorization_header

from .models import ClientSystemUser, ClientSystem, get_expire_time


def get_user(token):
    user = ClientSystemUser(token)
    return user


class ClientSystemAuthMiddleware(MiddlewareMixin):
    """Django Прослойка добавляющая проверку авторизации клиентских систем для каждого запроса

    Notes:
        - Прослойка выполняется для каждого запроса для проверки правильности авторизационного токена.
        - Для корректной проверки авторизации запрос должен иметь заголовок HTTP запроса с названием Authorization,
            содержащий строку с ключевым слово Token и токеном авторизации.
    """

    def process_request(self, request):
        """Функция работа с request перед выполнением основного тела запроса, для проверки авторизации

        Args:
            request (Request): объект обрабатываемого запроса
        """
        if 'Authorization' in request.headers and 'Token ' in request.headers['Authorization']:
            token = request.headers['Authorization'].split(' ')[1]
            request.user = SimpleLazyObject(
                lambda: get_user(token)
            )


class DRFClientTokenAuthentication(TokenAuthentication):
    """DRF Прослойка добавляющая проверку авторизации клиентских систем для каждого запроса

    Notes:
        - Прослойка выполняется для каждого запроса для проверки правильности авторизационного токена
        - Для корректной проверки авторизации запрос должен иметь заголовок HTTP запроса с названием Authorization,
            содержащий строку с ключевым слово Token и токеном авторизации.
    """

    model = ClientSystem

    def authenticate(self, request):
        """Аутентификация клиента который запрашивает данные с конектора по токену клиента.

        Notes:
            - В данной части аутентификации проверяются различные виды ошибко, наличие нужного хедера и т.д.

        Args:
            request (Request): объект обрабатываемого запроса
        Returns:
            ClientSystemUser, ClientSystem: Объект пользователя связанного с авторизуеммой системой и объект модели
                клиентской системы.
        """
        auth = get_authorization_header(request).split()
        if not auth or auth[0].lower() != self.keyword.lower().encode():
            return None
        if len(auth) == 1:
            msg = _('Invalid token header. No credentials provided.')
            raise exceptions.AuthenticationFailed(msg)
        elif len(auth) > 2:
            msg = _('Invalid token header. Token string should not contain spaces.')
            raise exceptions.AuthenticationFailed(msg)
        try:
            token = auth[1].decode()
        except UnicodeError:
            msg = _('Invalid token header. Token string should not contain invalid characters.')
            raise exceptions.AuthenticationFailed(msg)
        return self.authenticate_credentials(token)

    def authenticate_credentials(self, key):
        """Проверка токена на правильность и соответствие какой-либо клиентской системе.

        Args:
            key (str): токен авторизации

        Returns:
            ClientSystemUser, ClientSystem: Объект пользователя связанного с авторизуеммой системой и объект модели
                клиентской системы.
        """
        model = self.get_model()
        try:
            system: ClientSystem = model.objects.get(
                tokens__token=key,
                last_use__gt=timezone.now() - timezone.timedelta(minutes=get_expire_time())
            )
        except model.DoesNotExist:
            raise exceptions.AuthenticationFailed(_('Invalid token.'))
        if not system.active:
            raise exceptions.AuthenticationFailed(_('User inactive or deleted.'))
        return (ClientSystemUser(key, client=system), system)
