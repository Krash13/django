import json
from django.utils import timezone
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework.status import HTTP_401_UNAUTHORIZED, HTTP_204_NO_CONTENT
from ..serializers.registration import RegistrationSerializer
from ..models import ClientSystem


class RegistrationStudentView(APIView):

    permission_classes = []

    def post(self, request, **kwargs):
        serializer = RegistrationSerializer(
            data=request.data
        )
        serializer.is_valid(raise_exception=True)
        client = serializer.create(serializer.validated_data)
        client.last_login = timezone.now()
        client.last_use = timezone.now()
        client.save()
        client.clear_expired_tokens()
        token = client.create_token()
        return Response(
            data={
                'login': client.login,
                'password': client.password,
                'token': token.token
            }
        )
