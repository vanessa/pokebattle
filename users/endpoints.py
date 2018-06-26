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
