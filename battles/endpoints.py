from django.db.models import Q

from rest_framework import generics, permissions
from rest_framework.response import Response

from battles.models import Battle
from battles.permissions import IsInBattle
from battles.serializers import BattleListSerializer, BattleSerializer
from pokemons.serializers import PokemonSerializer


class BattleDetailsEndpoint(generics.RetrieveAPIView):
    queryset = Battle.objects.all()
    serializer_class = BattleSerializer
    permission_classes = (IsInBattle, )


class BattleListEndpoint(generics.ListAPIView):
    serializer_class = BattleListSerializer
    permission_classes = (IsInBattle, )

    def get_queryset(self):
        user = self.request.user
        return Battle.objects.filter(
            Q(creator=user) | Q(opponent=user)
        )


class BattleCreateEndpoint(generics.CreateAPIView):
    serializer_class = BattleSerializer
    permission_classes = (permissions.IsAuthenticated, )

    def post(self, request, *args, **kwargs):
        data = request.data
        battle = dict(
            opponent=data.opponent,
            creator=request.user
        )
        battle = BattleSerializer(data=battle)
        battle.is_valid()
        battle.save()
        creator_team = dict(
            battle_related=battle.id,
            pokemons=PokemonSerializer(data=data.team, many=True)
        )
        # WIP
        return Response(creator_team)
