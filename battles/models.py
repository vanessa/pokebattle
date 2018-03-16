from django.db import models

from pokemons.models import Pokemon
from users.models import User


class Battle(models.Model):
    creator = models.ForeignKey(User, related_name='battle_creator')
    opponent = models.ForeignKey(User, related_name='battle_opponent')
    date_created = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return '{0} x {1}'.format(self.creator, self.opponent)

class ChosenPokemons(models.Model):
    battle_related = models.ForeignKey(Battle, related_name='battle')
    first = models.ForeignKey(Pokemon, related_name='battle_first_pokemon')
    second = models.ForeignKey(Pokemon, related_name='battle_second_pokemon')
    third = models.ForeignKey(Pokemon, related_name='battle_third_pokemon')
    trainer = models.ForeignKey(User, related_name='who_chose')
