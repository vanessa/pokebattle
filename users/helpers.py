from importlib import import_module

from django.conf import settings
from django.contrib.auth import BACKEND_SESSION_KEY, SESSION_KEY, load_backend
from django.contrib.auth.models import AnonymousUser


def get_user_from_session_key(session_key):
    engine = import_module(settings.SESSION_ENGINE)
    session = engine.SessionStore(session_key)

    try:
        user_id = session[SESSION_KEY]
        backend_path = session[BACKEND_SESSION_KEY]
        backend = load_backend(backend_path)
        user = backend.get_user(user_id) or AnonymousUser()
    except KeyError:
        user = AnonymousUser()
    return user
