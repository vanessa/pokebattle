from django.db import models

from pokemons.models import Pokemon
from users.models import User


class Battle(models.Model):
    creator = models.ForeignKey(User, related_name='battle_creator')
    opponent = models.ForeignKey(User, related_name='battle_opponent')
    date_created = models.DateTimeField(auto_now_add=True)
    winner = models.ForeignKey(User, related_name='battle_winner', null=True)

    def __str__(self):
        return '{0} vs. {1}'.format(
            self.creator.get_short_name(),
            self.opponent.get_short_name()
        )


class BattleTeam(models.Model):
    battle_related = models.ForeignKey(Battle, related_name='chosen_pokemons')
    pokemons = models.ManyToManyField(Pokemon, related_name='battle_team')
    trainer = models.ForeignKey(User, related_name='trainer')

    class Meta:
        ordering = ['battle_related']

    def __str__(self):
        return '#{0} / {1} / {2}'.format(
            self.battle_related.id,
            list(self.pokemons.all()),
            self.trainer
        )
