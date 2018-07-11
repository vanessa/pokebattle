from django.conf.urls import url

from .views import BattlesListView, BattleView, ChoosePokemonTeamView


urlpatterns = [
    url(r'^$|^(create)/$', BattlesListView.as_view(), name='list'),
    url(r'^details/(?P<pk>[\w-]+)$', BattleView.as_view(), name='details'),
    url(r'^details/(?P<pk>[\w-]+)/team$', ChoosePokemonTeamView.as_view(), name='team'),
]
