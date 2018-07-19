from django.utils.html import format_html

from dal import autocomplete
from rest_framework import generics, permissions

from pokemons.models import Pokemon
from pokemons.serializers import PokemonSerializer


class PokemonListEndpoint(generics.ListAPIView):
    serializer_class = PokemonSerializer
    permission_classes = (permissions.IsAuthenticated, )
    queryset = Pokemon.objects.all()


class PokemonAutocompleteEndpoint(autocomplete.Select2QuerySetView):
    def get_queryset(self):
        if not self.request.user.is_authenticated():
            return Pokemon.objects.none()

        queryset = Pokemon.objects.all()
        if self.q:
            queryset = queryset.filter(name__icontains=self.q)

        return queryset

    def get_selected_result_label(self, item):
        return item.name

    def get_result_label(self, item):  # noqa
        return format_html('<img src="{}"> {} | A: {}, D: {}, HP: {}',
                           item.sprite, item.name, item.attack, item.defense, item.hp)
