from django.conf.urls import url

from .endpoints import BattleDetailsEndpoint


urlpatterns = [
    url(r'^battles/(?P<pk>[\w-]+)$', BattleDetailsEndpoint.as_view(), name='battle-details')
]
