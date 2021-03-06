from django.conf.urls import url

from .views import BattlesListView, BattleView, ChoosePokemonTeamView, CreateBattleView, InviteView


urlpatterns = [
    url(r'^$', BattlesListView.as_view(), name='list'),
    url(r'^create/$', CreateBattleView.as_view(), name='create-battle'),
    url(r'^details/(?P<pk>[\w-]+)$', BattleView.as_view(), name='details'),
    url(r'^details/(?P<pk>[\w-]+)/team$', ChoosePokemonTeamView.as_view(), name='team'),
    url(r'^invite/$', InviteView.as_view(), name='invite')
]
