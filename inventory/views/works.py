from rest_framework.viewsets import ModelViewSet
from clients.permissions import IsTeacherPermission
from utils.paginations import SelectorPagination
from ..models.works import Work
from ..serializers.works import BaseWorkSerializer


class WorksModelViewSet(
    ModelViewSet,
):
    """
    ViewSet для взаимодействия с лабораторками

    Присутствует пагинация с максимальным размером страницы 100 и значением по умолчанию 10
    """
    queryset = Work.objects.all()
    serializer_class = BaseWorkSerializer
    permission_classes = [
        IsTeacherPermission
    ]
    pagination_class = SelectorPagination
