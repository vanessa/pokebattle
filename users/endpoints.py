from rest_framework import generics, permissions
from rest_framework.response import Response

from users.models import User
from users.serializers import UserSerializer


class UserDetailsEndpoint(generics.GenericAPIView):
    serializer_class = UserSerializer
    queryset = User.objects.all()
    permission_classes = (permissions.IsAuthenticated, )

    def get(self, request):
        user_data = self.serializer_class(request.user).data
        return Response(user_data)


class UsersEndpoint(generics.ListAPIView):
    # Endpoint to see the users you can invite to a battle,
    # which is everyone, except you
    permission_classes = (permissions.IsAuthenticated, )
    serializer_class = UserSerializer

    def get_queryset(self):
        return User.objects.exclude(email=self.request.user.email)
