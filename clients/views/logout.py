from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework.status import HTTP_204_NO_CONTENT
from ..models import ClientSystem, ClientSystemToken


class LogoutForClientSystem(APIView):
    """Класс обработчика запроса аннулирования авторизационного токена для клиентской системы

    Methods:
        post (dict): Обработчик зарпоса деавторизации
    """

    def post(self, request, **kwargs):
        """Обработчик деавторизационного запроса

        Args:
            request (Request): объект запроса
                data.token - деавторизуемый токен
            kwargs: словарь параметров передаваемых как аргумент урла

        Returns:
            Response: объект ответа, пустой
        """
        token = request.data['token']
        try:
            token: ClientSystemToken = ClientSystemToken.objects.get(token=token)
            token.delete()
        except ClientSystem.DoesNotExist:
            pass
        return Response(data={}, status=HTTP_204_NO_CONTENT)