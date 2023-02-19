from rest_framework.serializers import ModelSerializer, CharField, SerializerMethodField
from ..models.client import ClientSystem


class ClientBaseSerializer(ModelSerializer):

    fio = SerializerMethodField()

    class Meta:
        model = ClientSystem
        fields = ('fio', 'uuid')

    def get_fio(self, obj):
        return str(obj)
