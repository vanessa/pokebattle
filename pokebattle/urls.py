from django.conf import settings
from django.conf.urls import include, url  # noqa
from django.contrib import admin
from django.views.generic import TemplateView

import django_js_reverse.views

from battles.views import PokemonListAPIView


urlpatterns = [
    url(r'^admin/', admin.site.urls, name='admin'),
    url(r'^jsreverse/$', django_js_reverse.views.urls_js, name='js_reverse'),

    # Pokebattle

    url(r'^', include('users.urls', namespace='auth')),
    url(r'^$', TemplateView.as_view(template_name='common/index.html'), name='home'),
    url(r'^battles/', include('battles.urls', namespace='battles')),

    # api
    url(r'^api/pokemon/$', PokemonListAPIView.as_view(), name='api-pokemon-list'),
]

if settings.DEBUG:
    import debug_toolbar
    urlpatterns = [
        url(r'^__debug__/', include(debug_toolbar.urls)),
    ] + urlpatterns
