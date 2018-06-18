from django.conf import settings
from django.conf.urls import include, url  # noqa
from django.contrib import admin
from django.views.generic import TemplateView

import django_js_reverse.views
from rest_framework.authtoken import views as drf_views

from battles.views import PokemonListAPIView


urlpatterns = [
    url(r'^admin/', admin.site.urls, name='admin'),
    url(r'^admin/statuscheck/', include('celerybeat_status.urls')),
    url(r'^jsreverse/$', django_js_reverse.views.urls_js, name='js_reverse'),
    url(r'^social/', include('social_django.urls', namespace='social')),

    # Pokebattle
    url(r'^', include('users.urls', namespace='auth')),
    url(r'^$', TemplateView.as_view(template_name='common/index.html'), name='home'),
    url(r'^battles/', include('battles.urls', namespace='battles')),

    # API
    url(r'^api/pokemon/$', PokemonListAPIView.as_view(), name='api-pokemon-list'),
    url(r'api/', include('battles.endpoints_urls', namespace='api-battles')),
    url('api-token-auth/', drf_views.obtain_auth_token, name='obtain-auth-token')
]

if settings.DEBUG:
    import debug_toolbar
    urlpatterns = [
        url(r'^__debug__/', include(debug_toolbar.urls)),
    ] + urlpatterns
