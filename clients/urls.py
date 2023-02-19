"""
Файл содержащий URL доступных запросов модуля clients

Urls:
    login: запрос авторизации
    logout: запрос деавторизации
"""
from django.urls import path
from .views.login import LoginForClientSystem
from .views.registration import RegistrationStudentView
from .views.selector import StudentSelectorView


urlpatterns = [
    path('login/', LoginForClientSystem.as_view()),
    path('registration/student/', RegistrationStudentView.as_view()),
    path('selector/student/', StudentSelectorView.as_view()),
]
