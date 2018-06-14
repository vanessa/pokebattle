from rest_framework import generics, permissions

from battles.models import Battle

from .serializers import BattleSerializer


class BattleDetailsEndpoint(generics.RetrieveAPIView):
    queryset = Battle.objects.all()
    serializer_class = BattleSerializer
    permission_classes = [permissions.IsAuthenticated]
