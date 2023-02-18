from rest_framework.serializers import ModelSerializer
from ..models.works import Work


class BaseWorkSerializer(ModelSerializer):
    """
    Базовый сериалайзер реагенты
    """
    class Meta:
        model = Work
        fields = '__all__'
