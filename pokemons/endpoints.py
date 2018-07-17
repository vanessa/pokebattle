from rest_framework import generics, permissions

from pokemons.models import Pokemon
from pokemons.serializers import PokemonSerializer


class PokemonListEndpoint(generics.ListAPIView):
    serializer_class = PokemonSerializer
    permission_classes = (permissions.IsAuthenticated, )
    queryset = Pokemon.objects.all()
