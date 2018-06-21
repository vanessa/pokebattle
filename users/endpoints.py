from rest_framework import exceptions, generics

from users.helpers import get_user_from_session_key
from users.models import User
from users.serializers import UserSerializer


class UserDetailsEndpoint(generics.RetrieveAPIView):
    model = User
    serializer_class = UserSerializer

    def get_object(self):
        session_key = self.request.query_params.get('session')
        if not session_key:
            raise exceptions.ParseError(
                'You have to pass session key as a querystring called `session`.')
        user = get_user_from_session_key(session_key)
        return user
