from rest_framework import status
from rest_framework.views import APIView
from rest_framework.response import Response
from ..models.client import ClientSystem
from ..permissions import IsTeacherPermission
from ..serializers.client import ClientBaseSerializer


class StudentSelectorView(APIView):
    permission_classes = [IsTeacherPermission, ]

    def get(self, request, *args, **kwargs):
        students = ClientSystem.objects.filter(
            is_student=True,
            active=True
        )
        serializer = ClientBaseSerializer(
            instance=students,
            many=True
        )
        return Response(data=serializer.data, status=status.HTTP_200_OK)