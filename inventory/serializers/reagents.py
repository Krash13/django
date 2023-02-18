from rest_framework.serializers import ModelSerializer, CharField, SerializerMethodField
from ..models.reagents import Reagents, WorkReagents


class BaseReagentsSerializer(ModelSerializer):
    """
    Базовый сериалайзер реагенты
    """
    class Meta:
        model = Reagents
        fields = '__all__'


class UpdateReagentsSerializer(ModelSerializer):

    class Meta:
        model = Reagents
        exclude = ('quantity', )


class BaseWorkReagentsSerializer(ModelSerializer):
    """
    Базовый сериалайзер реагенты
    """
    work = SerializerMethodField()
    reagent = SerializerMethodField()
    units = SerializerMethodField()

    class Meta:
        model = WorkReagents
        fields = '__all__'

    def get_work(self, obj):

        return {
            "name": str(obj.work),
            "id": obj.work.id
        }

    def get_reagent(self, obj):
        return {
            "name": str(obj.reagent),
            "id": obj.reagent.id
        }

    def get_units(self, obj):
        return {
            "name": obj.get_units_display(),
            "id": obj.units
        }


class CreateWorkReagentsSerializer(ModelSerializer):

    class Meta:
        model = WorkReagents
        fields = '__all__'
