"""
Модуль содержащий настройки административной части проекта для модуля clients
"""
from django.contrib.admin import site, ModelAdmin
from ..models.client import ClientSystem


class ClientSystemModelAdmin(ModelAdmin):
    """
    Класс настройки администрирования для модели клиентской системы
    """
    pass


site.register(ClientSystem, ClientSystemModelAdmin)
