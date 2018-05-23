from django.utils.crypto import get_random_string


def create_invite_key():
    key = get_random_string(12).lower()
    return key
