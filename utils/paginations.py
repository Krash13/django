from django.conf import settings
from rest_framework.pagination import PageNumberPagination
from rest_framework.utils.urls import remove_query_param, replace_query_param


class SelectorPagination(PageNumberPagination):
    """
    Наш стандарный класс пагинатор

    Attributes:
        page_size (int): Дефолтный размер страницы
        page_size_query_param (str): Параметр, отвечающий за размер страницы
        max_page_size (int): Максимальный размер страницы
    """
    page_size = 10
    page_size_query_param = 'size'
    max_page_size = 100

