import json
from django.utils import timezone
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework.status import HTTP_401_UNAUTHORIZED, HTTP_204_NO_CONTENT
from rest_framework.exceptions import PermissionDenied, NotAuthenticated, AuthenticationFailed
from ..models import ClientSystem


class LoginForClientSystem(APIView):
    """Класс обработчика запроса для авторизации клинетской системы по идентификатору и ключу.

    Methods:
        post (dict): обработчик запроса авторизации,
    """
    permission_classes = []

    def post(self, request, **kwargs):
        password = request.data['password']
        login = request.data['login']
        client: ClientSystem = None
        try:
            client = ClientSystem.objects.get(login=login, password=password)
        except ClientSystem.DoesNotExist:
            return Response(
                data={
                    'detail': 'Пароль или логин неверные',
                },
                status=HTTP_401_UNAUTHORIZED
            )
        client.last_login = timezone.now()
        client.last_use = timezone.now()
        # token.current = token.regenerate_current_token()
        client.save()
        client.clear_expired_tokens()
        token = client.create_token()
        return Response(
            data={
                'token': token.token
            }
        )


