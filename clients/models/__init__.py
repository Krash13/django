"""
Модуль содержащий модели clients, а так же базовый класс авторизуемой системы
"""
from django.utils import timezone
from .client import ClientSystem, ClientSystemToken, get_expire_time
# from django.contrib.auth.models import AbstractUser


class ClientSystemUser:
    """
    Класс авторизуемой системы который устанавливается в request.user

    Attributes:
        _client (ClientSystem): объект модели клиентской системы
        _token (str): строка конкретного токена подключения
    """
    _client = None
    _token = None

    def __init__(self, token, client: ClientSystem = None):
        """Инициализация объекта

        Args:
            token (str): строка конкретного токена авторизации;
            client (ClientSystem): объект клиентской системы которая авторизовалась при помощи токена;
        """
        self._token = token
        if client:
            self._client = client
        # self._client = client

    def __str__(self):
        """Строковое представление объекта.

        Returns:
            str: строковое представление объекта.
        """
        return f'ClientSystemUser({self._token})'

    def __eq__(self, other):
        """Функция проверки объекта на равенство при помощи проверки равенства клиентских систем

        Args:
            other (ClientSystemUser): объект, с которым проводится проверка сравнения

        Returns:
            bool: результат сравнения
        """
        return isinstance(other, self.__class__) and self._client == other._client

    def __hash__(self):
        """Хеширование объекта для возможности использовать его в качестве ключа в словарях, хешируется uuid клиента.

        Returns:
            hash: хеш полученный из строкового представления uuid объекта клиентской системы.
        """
        if self._client is not None:
            return hash(str(self._client.uuid))
        else:
            return hash(str(None))

    @property
    def client(self) -> ClientSystem:
        """Вычисляемый атрибут, который возвращает клиент системы, найденный по токену или заданный заранее.

        Notes:
            - Клиент ищется по токену и времени протухания токена, если токен слишком старый то клиент найден не будет.

        Returns:
            ClientSystem:
                - Если клиент был заранее подан при инициализации объекта то вернется именно он.
                - Если клиент не был подан, то если есть токен, будет произведена попытка найти клиента и вернуть его.
                - Если нет ни клиента ни токена, или если клиента по токену найти не удалось, то вернется None

        """
        # print('ClientSystemUser', self._token)
        if self._client is None and self._token is not None:
            try:
                self._client = ClientSystem.objects.get(
                    tokens__token=self._token,
                    last_use__gt=timezone.now() - timezone.timedelta(minutes=get_expire_time())
                )
            except ClientSystem.DoesNotExist:
                self._client = None
                self._token = None
        return self._client

    def save(self):
        """Заблокированная функция сохранение этого объекта.
        """
        raise NotImplementedError("Django doesn't provide a DB representation for AnonymousUser.")

    def delete(self):
        """Заблокированная функция удаления этого объекта.
        """
        raise NotImplementedError("Django doesn't provide a DB representation for AnonymousUser.")

    def set_password(self, raw_password):
        """Заблокированная функция установки пароля этого объекта.
        """
        raise NotImplementedError("Django doesn't provide a DB representation for AnonymousUser.")

    def check_password(self, raw_password):
        """Заблокированная функция проверки пароля этого объекта.
        """
        raise NotImplementedError("Django doesn't provide a DB representation for AnonymousUser.")

    @property
    def is_anonymous(self):
        """Вычисляемое свойство анонимности, по умолчанию объект не анонимен.
        """
        return False

    @property
    def is_authenticated(self):
        """Вычисляемое свойство аутентифицированности, по умолчанию объект аутентифицирован.
        """
        return True

    @property
    def is_teacher(self):
        return self._client.is_teacher

    @property
    def is_student(self):
        return self._client.is_student

    @property
    def is_active(self):
        """Вычисляемое свойство активности, по умолчанию объект активен.
        """
        return True

    @property
    def is_system(self):
        """Вычисляемое свойство показывающее принадлежность к внешним системам, по умолчанию объект внешняя система.
        """
        return True
