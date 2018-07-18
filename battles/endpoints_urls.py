from django.conf.urls import url

from .endpoints import BattleCreateEndpoint, BattleDetailsEndpoint, BattleListEndpoint


urlpatterns = [
    url(r'^battles/(?P<pk>[\w-]+)$', BattleDetailsEndpoint.as_view(), name='battle-details'),
    url(r'^battles/$', BattleListEndpoint.as_view(), name='battle-list'),
    url(r'^battles/create/$', BattleCreateEndpoint.as_view(), name='create-battle')
]
