from django.conf.urls import url

from .views import BattlesListView, BattleView, ChoosePokemonTeamView, InviteView


urlpatterns = [
    url(r'^(?:.*)/?$', BattlesListView.as_view(), name='list'),
    url(r'^details/(?P<pk>[\w-]+)$', BattleView.as_view(), name='details'),
    url(r'^details/(?P<pk>[\w-]+)/team$', ChoosePokemonTeamView.as_view(), name='team'),
    url(r'^invite/$', InviteView.as_view(), name='invite')
]
