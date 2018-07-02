from rest_framework import generics

from battles.models import Battle
from battles.permissions import IsInBattle
from battles.serializers import BattleListSerializer, BattleSerializer


class BattleDetailsEndpoint(generics.RetrieveAPIView):
    queryset = Battle.objects.all()
    serializer_class = BattleSerializer
    permission_classes = (IsInBattle, )


class BattleListEndpoint(generics.ListAPIView):
    queryset = Battle.objects.all()
    serializer_class = BattleListSerializer
    permission_classes = (IsInBattle, )
