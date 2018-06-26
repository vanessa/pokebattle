from rest_framework import generics

from users.models import User
from users.permissions import IsOwner
from users.serializers import UserSerializer


class UserDetailsEndpoint(generics.RetrieveAPIView):
    serializer_class = UserSerializer
    queryset = User.objects.all()
    permission_classes = (IsOwner, )
