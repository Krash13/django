from rest_framework.viewsets import ModelViewSet
from clients.permissions import IsTeacherPermission
from utils.paginations import SelectorPagination
from utils.serializers import MultiSerializerViewSet, ACTIONS
from rest_framework import status
from rest_framework.decorators import action
from rest_framework.response import Response
from ..models.reagents import Reagents, WorkReagents
from ..models.choices import UnitsType
from ..serializers.reagents import BaseReagentsSerializer, \
    UpdateReagentsSerializer, \
    BaseWorkReagentsSerializer, \
    CreateWorkReagentsSerializer


class ReagentsModelViewSet(
    ModelViewSet,
    MultiSerializerViewSet
):
    """
    ViewSet для взаимодействия с реагентами

    Присутствует пагинация с максимальным размером страницы 100 и значением по умолчанию 10
    """
    queryset = Reagents.objects.all()
    serializer_class = BaseReagentsSerializer
    serializers_class = {
        ACTIONS.LIST: BaseReagentsSerializer,
        ACTIONS.RETRIEVE: BaseReagentsSerializer,
        ACTIONS.POST: BaseReagentsSerializer,
        ACTIONS.PUT: UpdateReagentsSerializer
    }
    permission_classes = [
        IsTeacherPermission
    ]
    pagination_class = SelectorPagination

    @action(methods=['POST'], detail=True, url_path='plus')
    def plus(self, request, *args, **kwargs):
        reagents = self.get_object()
        if not (request.data.get('quantity') and request.data.get('units')):
            return Response(
                data={'detail': 'Не передано количество или единицы измерения'},
                status=status.HTTP_400_BAD_REQUEST
            )
        units = next(filter(lambda d: d[0] == request.data.get('units'), UnitsType.choices), None)
        if units is None:
            return Response(
                data={'detail': 'Несуществующие единицы измерения'},
                status=status.HTTP_400_BAD_REQUEST
            )
        reagents.plus(
            request.data.get('quantity'),
            units[1]
        )
        return Response(status=status.HTTP_200_OK)

    @action(methods=['POST'], detail=True, url_path='minus')
    def minus(self, request, *args, **kwargs):
        reagents = self.get_object()
        if not (request.data.get('quantity') and request.data.get('units')):
            return Response(
                data={'detail': 'Не передано количество или единицы измерения'},
                status=status.HTTP_400_BAD_REQUEST
            )
        units = next(filter(lambda d: d[0] == request.data.get('units'), UnitsType.choices), None)
        if units is None:
            return Response(
                data={'detail': 'Несуществующие единицы измерения'},
                status=status.HTTP_400_BAD_REQUEST
            )
        reagents.minus(
            request.data.get('quantity'),
            units[1]
        )
        return Response(status=status.HTTP_200_OK)


class WorkReagentsModelViewSet(
    ModelViewSet,
    MultiSerializerViewSet
):
    """
    ViewSet для взаимодействия с реагентами

    Присутствует пагинация с максимальным размером страницы 100 и значением по умолчанию 10
    """
    queryset = WorkReagents.objects.all()
    serializer_class = BaseWorkReagentsSerializer
    serializers_class = {
        ACTIONS.LIST: BaseWorkReagentsSerializer,
        ACTIONS.RETRIEVE: BaseWorkReagentsSerializer,
        ACTIONS.POST: CreateWorkReagentsSerializer,
        ACTIONS.PUT: CreateWorkReagentsSerializer
    }
    permission_classes = [
        IsTeacherPermission
    ]

    def get_queryset(self):
        qs = super().get_queryset().filter(
            work__id=self.kwargs.get('work_id')
        )
        return qs
