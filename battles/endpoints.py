from rest_framework import generics

from battles.models import Battle
from battles.permissions import IsInBattle
from battles.serializers import BattleSerializer


class BattleDetailsEndpoint(generics.RetrieveAPIView):
    queryset = Battle.objects.all()
    serializer_class = BattleSerializer
    permission_classes = (IsInBattle, )
