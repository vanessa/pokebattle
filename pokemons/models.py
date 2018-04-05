from django.db import models


class Pokemon(models.Model):
    id = models.SmallIntegerField('Pokemon\'s ID', primary_key=True)
    name = models.CharField('Pokemon\'s name', max_length=60)
    sprite = models.URLField('Pokemon\'s picture', blank=True)

    """ Attributes """
    attack = models.SmallIntegerField('Attack')
    defense = models.SmallIntegerField('Defense')
    hp = models.SmallIntegerField('HP')

    def __str__(self):
        return self.name
