from django.conf.urls import url

from .endpoints import PokemonAutocompleteEndpoint, PokemonListEndpoint


urlpatterns = [
    url(r'^pokemon/$', PokemonListEndpoint.as_view(), name='list'),
    url(r'^pokemon-autocomplete/$', PokemonAutocompleteEndpoint.as_view(), name='autocomplete'),
]
