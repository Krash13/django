from rest_framework.viewsets import GenericViewSet


class ACTIONS:
    LIST = 'list'
    PUT = 'update'
    PATCH = 'partial_update'
    POST = 'create'
    RETRIEVE = 'retrieve'
    DELETE = 'destroy'


class GetActionViewSet(GenericViewSet):
    actions_expand = {
        ACTIONS.LIST: ACTIONS.RETRIEVE,
        ACTIONS.PUT: ACTIONS.POST,
        ACTIONS.PATCH: ACTIONS.POST
    }

    def get_expanded_action(self, for_dict, action_expand=None):
        if action_expand is None:
            action_expand = self.actions_expand
        action = self.action
        if action not in for_dict and action in action_expand:
            action = action_expand[action]
            if isinstance(action, dict):
                return self.get_expanded_action(action)
        return action


class MultiSerializerViewSet(GetActionViewSet):
    serializers_class = {}

    def get_serializer_expanded_action(self):
        return self.get_expanded_action(self.serializers_class)

    def get_serializer_class(self):
        action = self.get_serializer_expanded_action()
        if action in self.serializers_class:
            self.serializer_class = self.serializers_class.get(action)
        return super().get_serializer_class()