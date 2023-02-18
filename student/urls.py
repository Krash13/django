from django.urls import path, include
from rest_framework.routers import SimpleRouter
from .views.student_works import TeacherStudentWorksModelViewSet, \
    TodayStudentWorksModelViewSet

base_router = SimpleRouter()
base_router.register(prefix='teacher/works', viewset=TeacherStudentWorksModelViewSet, basename='teacher|works')
base_router.register(prefix='works', viewset=TodayStudentWorksModelViewSet, basename='student|works')
# inventory_router.register(prefix='works', viewset=WorksModelViewSet, basename='works')

# work_reagents_router = SimpleRouter()
# work_reagents_router.register(prefix='reagents', viewset=WorkReagentsModelViewSet, basename='work|reagents')
# profession_router = SimpleRouter()
# profession_router.register(prefix='professions', viewset=ProfessionModelViewSet, basename='professions')

urlpatterns = [
    path('', include(base_router.urls)),
    # path('works/<int:work_id>/', include(work_reagents_router.urls)),
    # path('', include(profession_router.urls)),
]
