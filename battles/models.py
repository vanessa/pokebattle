from django.db import models

from pokemons.models import Pokemon
from users.models import User

from .choices import POKEMON_ORDER_CHOICES


class Battle(models.Model):
    creator = models.ForeignKey(User, related_name='battle_creator')
    opponent = models.ForeignKey(User, related_name='battle_opponent')
    date_created = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return '{0} x {1}'.format(self.creator, self.opponent)

class BattleTeam(models.Model):
    battle_related = models.ForeignKey(Battle, related_name='chosen_pokemons')
    order = models.CharField(choices=POKEMON_ORDER_CHOICES, max_length=1)
    pokemons = models.ManyToManyField(Pokemon, related_name='pokemons')
    trainer = models.ForeignKey(User, related_name='trainer')

    class Meta:
        ordering = ['order']

    def __str__(self):
        return '#{0} / {1} / {2}'.format(
            self.battle_related.id,
            self.pokemons.name,
            self.trainer
        )
