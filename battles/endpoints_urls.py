from django.conf.urls import url

from .endpoints import BattleDetailsEndpoint, BattleListEndpoint


urlpatterns = [
    url(r'^battles/(?P<pk>[\w-]+)$', BattleDetailsEndpoint.as_view(), name='battle-details'),
    url(r'^battles/$', BattleListEndpoint.as_view(), name='battle-list')
]
