"""
Файл содержащий URL доступных запросов модуля clients

Urls:
    login: запрос авторизации
    logout: запрос деавторизации
"""
from django.urls import path
from .views.login import LoginForClientSystem
from .views.registration import RegistrationStudentView
from .views.logout import LogoutForClientSystem


urlpatterns = [
    path('login/', LoginForClientSystem.as_view()),
    path('registration/student/', RegistrationStudentView.as_view()),
    # path('logout/', LoginForClientSystem.as_view())
]
