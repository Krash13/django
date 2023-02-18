from rest_framework.serializers import ModelSerializer, SerializerMethodField, CharField, IntegerField
from rest_framework.exceptions import ValidationError
from ..models.student_works import StudentWork, StudentWorkReagents
from inventory.serializers.works import BaseWorkSerializer


class ReagentBaseSerializer(ModelSerializer):

    reagent = CharField(source='reagent.reagent.name')
    units = CharField(source='reagent.get_units_display')
    quantity = IntegerField(source='reagent.quantity')

    class Meta:
        model = StudentWorkReagents
        exclude = ("student_work",)


class BaseStudentWorkSerializer(ModelSerializer):

    work = BaseWorkSerializer()
    student = SerializerMethodField()
    reagents = ReagentBaseSerializer(
        many=True,
        source="reagents.all"
    )

    class Meta:
        model = StudentWork
        fields = '__all__'

    def get_student(self, obj):
        return {
            "uuid": obj.student.uuid,
            "student": str(obj.student),
            "group": obj.student.group
        }


class CreateStudentWorkSerializer(ModelSerializer):

    class Meta:
        model = StudentWork
        fields = '__all__'

    def validate(self, attrs):
        if not attrs.get('student').is_student:
            raise ValidationError(
                detail={
                    'detail': 'Пользователь не является студентом'
                }
            )
        return attrs


class BaseStudentByStudentWorkSerializer(ModelSerializer):

    work = BaseWorkSerializer()
    reagents = ReagentBaseSerializer(
        many=True,
        source="reagents.all"
    )

    class Meta:
        model = StudentWork
        exclude = ("student", "date")


