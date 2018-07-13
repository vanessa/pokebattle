from django.conf.urls import url

from .endpoints import PokemonListEndpoint


urlpatterns = [
    url(r'^pokemon/$', PokemonListEndpoint.as_view(), name='list'),
]
