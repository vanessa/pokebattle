
from rest_framework import permissions

from battles.models import Battle  # noqa
from users.helpers import get_user_from_session_key


class IsSessionAuthenticated(permissions.BasePermission):
    def validate_session_key(self, key):
        user = get_user_from_session_key(key)
        if not user.is_authenticated():
            return False
        return True

    def has_permission(self, request, view):
        session_key = request.query_params.get('session')
        return self.validate_session_key(session_key)


class IsInBattle(permissions.BasePermission):

    def has_object_permission(self, request, view, obj):
        pass
