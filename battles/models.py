from django.db import models

from common.models import IndexedTimeStampedModel
from pokemons.models import Pokemon
from users.models import User

from .choices import BATTLE_STATUS


class Battle(models.Model):
    creator = models.ForeignKey(User, related_name='battle_creator')
    opponent = models.ForeignKey(User, related_name='battle_opponent')
    date_created = models.DateTimeField(auto_now_add=True)
    winner = models.ForeignKey(User, related_name='battle_winner', null=True)
    status = models.CharField(max_length=2, choices=BATTLE_STATUS, default='O')

    def __str__(self):
        return '{0} vs. {1}'.format(
            self.creator.get_short_name(),
            self.opponent.get_short_name()
        )

    def get_status_label(self):
        return self.get_status_display().lower()


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


class Invite(IndexedTimeStampedModel):
    inviter = models.ForeignKey(User, related_name='invites')
    invitee = models.EmailField()
    key = models.CharField('Invitation key', max_length=12, blank=True, null=True, unique=True)
    accepted = models.BooleanField('User has accepted this invite', default=False)

    def __str__(self):
        return 'from {inviter} to {invitee}'.format(
            inviter=self.inviter,
            invitee=self.invitee
        )
