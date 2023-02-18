import secrets
import uuid
import random
import string
import warnings
from datetime import timedelta
from django.db.models import Model, UUIDField, CharField, BooleanField, DateTimeField, ForeignKey
from django.db.models.deletion import CASCADE
from django.utils import timezone
from django.conf import settings


def get_expire_time():
    """Получение константы времени протухания токена авторизации.

    Notes:
        - Токен может быть задан параметром EXPIRED_CLIENT_TOKEN прописанным в django settings
        - По умолчанию время протухания 10 минут.

    Returns:
        int: Время истечения токена авторизации.
    """
    if not hasattr(settings, 'EXPIRED_CLIENT_TOKEN'):
        warnings.warn(
            'Возможно вы забыли указать в настройках значение для настройки времени протухания оперативного'
            ' токена авторизации подключенных систем EXPIRED_CLIENT_TOKEN, по умолчанию значение 10'
        )
        return 10
    else:
        return settings.EXPIRED_CLIENT_TOKEN


def get_token():
    """Функция генерации токена в виде хеша в 50 символов

    Returns:
        str: сгенерированная строка токена состоящая из 25 символов.
    """
    return secrets.token_hex(50)


def get_secret():
    """Функция генерации случайной строки состоящей из 32 anscii букв, цифр и знаков пунктуации.

    Notes:
        - Генерируемая строка содержит 32 символа.
        - В генерации используются только буквы, цифры. знаки пунктуации anscii кодировки.

    Returns:
        str: сгенерированная строка
    """
    return ''.join([random.choice(string.ascii_letters + string.digits + string.punctuation) for n in range(16)])


class ClientSystem(Model):
    """Модель авторизационных данных клиентской системы, которому разрешены манипуляции с объектами АД при помощи апи.

    Fields:
        uuid (UUIDField): уникальный идентификатор клиента.
        active (BooleanField): флаг активности клиента.
        created (DateTimeField): дата и время создания клиента.
        secret (CharField): закрытый ключ авторизации, генерируется функцией get_secret.
        read_only (BooleanField): флаг показывающий, что клиент не может ничего менять.
        last_login (DateTimeField): дата и время последнего входа.
        last_use (DateTimeField): дата и время последнего использования апи.
    """
    # TODO: Регулярка на поле хоста
    uuid = UUIDField(verbose_name='UUID клиента', default=uuid.uuid4, primary_key=True)
    login = CharField(unique=True, max_length=35, verbose_name='Логин')
    last_name = CharField(max_length=100, verbose_name='Фамилия')
    first_name = CharField(max_length=100, verbose_name='Имя')
    middle_name = CharField(max_length=100, blank=True, null=True, verbose_name='Отчество')
    group = CharField(max_length=100, blank=True, null=True, verbose_name='Группа')
    active = BooleanField(default=True, verbose_name='Активный')
    created = DateTimeField(auto_now_add=True, verbose_name='Дата создания')
    password = CharField(max_length=16, default=get_secret, blank=True, unique=True, verbose_name='Секретный токен')
    is_student = BooleanField(default=True, verbose_name='Студент')
    is_teacher = BooleanField(default=False, verbose_name='Преподаватель')

    last_login = DateTimeField(null=True, blank=True)
    last_use = DateTimeField(null=True, blank=True)
    # ToDo: Удалить все deprecated методы

    def __str__(self):
        return "{} {}{}".format(
            self.last_name,
            self.first_name,
            " " + self.middle_name if self.middle_name else ""
        )

    def regenerate_current_token(self):
        """Функцию перегенерации токена (Deprecated)

        Returns:
            str: Сгенерированный токен акторизации.
        """
        return get_token()

    def is_expired(self):
        """Функция проверки токена на истеченеие по времени(Deprecated)

        Returns:
            bool: флаг протухания
        """
        if self.last_use > timezone.now() - timezone.timedelta(minutes=get_expire_time()):
            return True
        else:
            return False

    def clean_current(self):
        """Очистка текущего временного токена (Deprecated)

        Returns:
            ничего
        """
        # self.current = None
        self.last_use = None
        self.save()

    def set_used(self):
        """Проставление даты использования

        Returns:
             ничего
        """
        self.last_use = timezone.now()
        self.save()

    class Meta:
        verbose_name = 'Клиент'
        verbose_name_plural = 'Клиенты'

    def check_token(self, token):
        """Функция проверки наличия не протухшего временного токена сгенерированного для этого клиента

        Args:
            token (str): токен для проверки
        Returns:
            bool: флаг доступности токена
        """
        try:
            token = self.tokens.get(token=token).first()
            if token.check_available():
                return True
            else:
                token.delete()
        except self.tokens.model.DoesNotExist:
            pass
        return False

    def create_token(self):
        """Создание нового временного токена

        Returns:
            ClientSystemToken: объект токена авторизации
        """
        return self.tokens.create(system=self)

    def clear_expired_tokens(self):
        """Функция очистик всех протухших на данный момент времени токенов

        Returns:
            ничего
        """
        expired = self.tokens.filter(created__lt=timezone.now() - timedelta(minutes=get_expire_time() + 5))
        expired.delete()


class ClientSystemToken(Model):
    """
    Модель хранения временного токена с которым можно выполнять запросы к апи

    Fields:
        system (ForeignKey): клиент для которого сгенерирован токен
        token (CharField): строка токена
        created (DateTimeField): дата создания токена
    """
    system = ForeignKey(to=ClientSystem, on_delete=CASCADE, related_name='tokens')
    token = CharField(max_length=100, default=get_token, unique=True)
    created = DateTimeField(auto_now_add=True)

    def check_available(self):
        """Проверка токена на протухание при помощи временной констант

        Returns:
            bool: флаг протухания
        """
        if self.created <= timezone.now() + timedelta(minutes=get_expire_time()):
            return True
        return False