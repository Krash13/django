from rest_framework.serializers import ModelSerializer, CharField, SerializerMethodField
from ..models.client import ClientSystem


class RegistrationSerializer(ModelSerializer):
    """
    Базовый сериалайзер реагенты
    """
    class Meta:
        model = ClientSystem
        fields = ('last_name', 'first_name', 'middle_name', 'login', 'group')