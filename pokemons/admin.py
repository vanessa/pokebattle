from django.contrib import admin

from .models import Pokemon


class PokemonAdmin(admin.ModelAdmin):
    list_display = ('id', 'name')


admin.site.register(Pokemon, PokemonAdmin)
