from django.contrib import admin

from .models import Battle, BattleTeam, Invite


admin.site.register(Battle)
admin.site.register(BattleTeam)
admin.site.register(Invite)
