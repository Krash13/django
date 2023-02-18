import inspect
import re
import copy
from django.conf import settings
from django.urls import get_resolver, URLResolver, URLPattern
from rest_framework.views import APIView
from rest_framework.viewsets import ViewSetMixin
from rest_framework.response import Response
from rest_framework.status import HTTP_200_OK
from rest_framework.permissions import AllowAny


def get_class_that_defined_method(meth):
    '''
    Возвращает класс функции(предполагается использование с вызываемыми классами, т.е. вьюхами)
    :param meth: метод
    :return: класс
    '''
    if inspect.ismethod(meth):
        for cls in inspect.getmro(meth.__self__.__class__):
            if cls.__dict__.get(meth.__name__) is meth:
                return cls
        meth = meth.__func__  # fallback to __qualname__ parsing
    if inspect.isfunction(meth):
        cls = getattr(inspect.getmodule(meth), meth.__qualname__.split('.<locals>', 1)[0].rsplit('.', 1)[0], None)
        if isinstance(cls, type):
            return cls
        elif hasattr(meth, 'view_class'):
            return meth.view_class
    return getattr(meth, '__objclass__', None)  # handle special descriptor objects


class InstanceUrlBaseViewMixin():

    def get_all_urlpaterns(self, resolver, urls, parent_patern='', parent_namespace=[]):
        '''
        Возвращает список всех именованных урлов в проекте
        :param resolver: текущая разбираемая колекция урлов
        :param urls: общий список урлов
        :param parent_patern: патерн родителя в случае вложенности
        :return:
        '''
        include_namespaces = getattr(settings, 'APPEND_NAMESPACES_TO_URLNAME', True)
        # pprint.pprint(dir(resolver))
        new_parent_namespace = parent_namespace.copy()
        if resolver.namespace != '' and resolver.namespace:
            if resolver.namespace not in new_parent_namespace:
                new_parent_namespace += [resolver.namespace]
        for url in resolver.url_patterns:
            if isinstance(url, URLResolver):
                # new_parent_namespace = parent_namespace.copy()
                # if resolver.namespace != '' and resolver.namespace:
                #     if resolver.namespace not in new_parent_namespace:
                #         new_parent_namespace += [resolver.namespace]
                new_parent_patern = self.append_pattern(parent_patern, self.make_pattern(url.pattern))
                self.get_all_urlpaterns(url, urls, new_parent_patern, new_parent_namespace)
            else:
                if url.name != 'api-root':
                    url = copy.copy(url)
                    url.namespace = ':'.join(new_parent_namespace)
                    if parent_namespace and include_namespaces:
                        url.name = f'{"|".join(new_parent_namespace)}|{url.name}'
                    url.pattern = self.append_pattern(parent_patern, str(url.pattern))
                    urls.append(url)


    def append_pattern(self, part1, part2):
        '''
        Расширяет патерн в случае вложенности урла в урл
        '''
        if len(part2) > 0 and part2[0] == '^':
            part2 = part2[1:]
        if len(part1) > 0 and part1[0] == '^':
            part1 = part1[1:]
        return '^' + part1 + part2

    def make_pattern(self, pattern):
        '''
        Превращение reg exp патерна в патерн path like
        :param pattern: патерн
        :return: исправленный патерн
        '''
        pattern = str(pattern)
        pattern = self._change_url_to_path_parameters(pattern)
        pattern = self._clean_url_of_specials(pattern)
        pattern = self._clean_url_of_types(pattern)
        pattern = self._switch_patternt_pk_to_id(pattern)
        return pattern

    def _change_url_to_path_parameters(self, path):
        '''Заменить в шаблоне урла параметры через регулярные выражения на параметры через типы'''
        reg = re.compile(r'(?:\(\?P)(<[^\<\>]+>)(?:[^\)]+\))')
        return reg.sub(r'\1', path)

    def _clean_url_of_types(self, path):
        '''Очистить шаблон урла от типов принимаемых параметров'''
        reg = re.compile(r'(?<=\<)(?:[^\:\<\>]+:)(?=[^\:\<\>]+\>)')
        return reg.sub('', path)

    def _clean_url_of_specials(self, path):
        '''Очистить шаблон урла от спецсимволов $^'''
        path = path.replace('^', '/').replace('$', '')
        return path

    def _switch_patternt_pk_to_id(self, path):
        '''Заменить во всех параметрах шаблона урла pk на id'''
        reg = re.compile(r'(?<=\<)([^\>]*)(?:pk)(?=\>)')
        return reg.sub(r'\1id', path)

    def get_url_parameters(self, pattern: URLPattern):
        '''Получение списка всех параметров'''
        reg = re.compile(r'(?:(?!\<pk\>).)(?:(?<=\<)(?:[^\:\<\>]+\:|(?:))([^\:\<\>]+)(?=\>))')
        parameters = reg.findall(pattern.pattern)
        return parameters

    def _switch_pk(self, parameters):
        return [re.sub('pk$', 'id', parameter) for parameter in parameters]

    def _switch_id(self, parameters):
        return [re.sub('id$', 'pk', parameter) for parameter in parameters]

    def _make_base_dict(self, action, method, pattern, context):
        '''
        Формирование словаря для одного метода их всех описанных для урла
        action - название действия
        method - метод действия
        pattern - шаблон урла с параметрами
        context - дополнительный выводимый контекст
        '''
        return {
            'action': action,
            'method': method,
            'pattern': pattern,
            **context
        }

    def make_view_method_dict(self, pattern, method, origin, view, parameters):
        '''
        Получение всех выводимых параметров для View
        '''
        context = self.get_addition_url_context(pattern=pattern, origin=origin, view=view, method=method, parameters=parameters)
        tpattern=self.make_pattern(pattern.pattern)
        return self._make_base_dict(action=method, method=method, pattern=tpattern, context=context)

    def make_vieset_action_dict(self, pattern, method, origin, view, parameters):
        '''
        Получение всех выводимых параметров для ViewSet
        '''
        action = origin.actions[method]
        view.action = action
        tpattern = self.make_pattern(pattern.pattern)
        context = self.get_addition_url_context(pattern=pattern, origin=origin, view=view, method=action, parameters=parameters)
        return self._make_base_dict(action=action, method=method, pattern=tpattern, context=context)

    def make_url_dict(self, pattern, methods, parameters):
        '''
        Возвращает словарь параметров выводимых для урла в целом.
        name - имя урла
        namespace - область имени
        parameters - список параметров, указываются через запятую
        is_parameterize - логическое значение показывающее параметризован ли урл
        methods - список всех методов описанных для этого урла
        '''
        return {
            'name': pattern.name,
            'namespace': pattern.namespace,
            'parameters': self._switch_pk(parameters),
            'is_parameterize': len(parameters) > 0,
            'methods': methods,
        }

    def get_addition_url_context(self, pattern, origin, view, method, parameters):
        '''
        переопределяетмый дополнительный контекст добавляемый к результату каждогого отдельного метода урла
        '''
        return {}


class InstanceUrlListBaseView(APIView):

    def __init__(self, *args, **kwargs):
        '''
        Добавление игнорируемых урлов из настроек
        '''
        self._indexed = []
        self._urls = []
        super().__init__(*args, **kwargs)
        if hasattr(settings, 'CHECK_ALLOWED_URLS_IGNORED'):
            if type(settings, list):
                self.ignored_urls += settings.CHECK_ALLOWED_URLS_IGNORED

    def check_url(self, patern: URLPattern):
        '''
        Проверяет что бы урл был описан как урл рест, вычленяет патерн и отправляет на определение доступности урла
        :param patern:
        :return:
        '''
        if patern.name not in self._indexed:
            self._indexed.append(patern.name)
            _origin = getattr(patern.callback, '__wrapped__', patern.callback)
            _cls = get_class_that_defined_method(_origin)
            if _cls is None:
                return
            elif issubclass(_cls, ViewSetMixin):
                self.check_viewset(patern, _origin)
            elif issubclass(_cls, APIView):
                self.check_view(patern, _origin)

    def check_viewset(self, pattern: URLPattern, origin):
        '''
        Обработка вьюсета(вычелинение всех экшенов во вьюсете)
        :param pattern: патерн
        :param origin: класс
        :return:
        '''
        view = origin.cls()
        methods = []
        parameters = self.get_url_parameters(pattern)
        for method in origin.actions:
            methods.append(
                self.make_vieset_action_dict(pattern, method, origin, view, parameters)
            )
        self._urls.append(
            self.make_url_dict(pattern, methods, parameters)
        )

    def check_view(self, pattern, origin):
        '''
        Обработка вьюхи(вычленение всех http методов которые реализует эта вьюха)
        :param pattern: патерн
        :param origin: класс
        :return:
        '''
        view = origin.cls()
        methods = []
        parameters = self.get_url_parameters(pattern)
        for method in view.http_method_names:
            if hasattr(view, method) and method != 'options':
                methods.append(
                    self.make_view_method_dict(pattern, method, origin, view, parameters)
                )
        self._urls.append(
            self.make_url_dict(pattern, methods, parameters)
        )

    def get(self, request, *args, **kwargs):
        '''
        Запуск обработки и поиска всех урлов
        '''
        resolver = get_resolver(None)
        urls = []
        self._urls = []
        self._indexed = []
        self.get_all_urlpaterns(resolver, urls)
        for url in urls:
            self.check_url(url)
        return Response(data={'urls': self._urls}, status=HTTP_200_OK)


class UrlsWithPermissionsView(InstanceUrlBaseViewMixin, InstanceUrlListBaseView):
    _urls = []
    _indexed = []
    ignored_urls = ['api-root', 'allowed-urls']
    permission_classes = [AllowAny]

    def get_addition_url_context(self, pattern, origin, view, method, parameters):
        allowed = self._check_permission(view)
        context = {
            'allowed': allowed,
        }
        return context

    def _check_permission(self, view):
        '''
        Проверка права у текущего пользователя на доступ к вьюхе
        :param view: вьюха
        :return: доступность
        '''
        self.request.user._is_superuser = None
        permissions = view.get_permissions()
        allowed = True
        for permission in permissions:
            if not permission.has_permission(self.request, view):
                allowed = False
                break
        return allowed

