# -*- coding: utf-8 -*-
# Generated by Django 1.11.11 on 2018-03-18 04:15
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('pokemons', '0003_auto_20180316_0626'),
    ]

    operations = [
        migrations.AddField(
            model_name='pokemon',
            name='sprite',
            field=models.URLField(blank=True, verbose_name="Pokemon's picture"),
        ),
    ]