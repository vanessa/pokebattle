from django.conf.urls import url

from .views import (
    BattlesListView,
    CreateBattleView,
    BattleView
)


urlpatterns = [
    url(r'^$', BattlesListView.as_view(), name='battles-list'),
    url(r'^create$', CreateBattleView.as_view(), name='create-battle'),
    url(r'^details/(?P<pk>[\w-]+)$', BattleView.as_view(), name='details')
]
