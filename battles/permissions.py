from importlib import import_module

from django.conf import settings
from django.contrib.auth import BACKEND_SESSION_KEY, SESSION_KEY, load_backend
from django.contrib.auth.models import AnonymousUser

from rest_framework import permissions

from battles.models import Battle  # noqa


class IsSessionAuthenticated(permissions.BasePermission):
    def validate_session_key(self, key):
        engine = import_module(settings.SESSION_ENGINE)
        session = engine.SessionStore(key)

        try:
            user_id = session[SESSION_KEY]
            backend_path = session[BACKEND_SESSION_KEY]
            backend = load_backend(backend_path)
            user = backend.get_user(user_id) or AnonymousUser()
        except KeyError:
            user = AnonymousUser()

        if not user.is_authenticated():
            return False
        return True

    def has_permission(self, request, view):
        session_key = request.query_params['session_id']
        return self.validate_session_key(session_key)


class IsInBattle(permissions.BasePermission):

    def has_object_permission(self, request, view, obj):
        pass
