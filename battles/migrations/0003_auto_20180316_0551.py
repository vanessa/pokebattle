# -*- coding: utf-8 -*-
# Generated by Django 1.11.11 on 2018-03-16 05:51
from __future__ import unicode_literals

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('battles', '0002_battle_date_created'),
    ]

    operations = [
        migrations.AlterField(
            model_name='chosenpokemons',
            name='battle_related',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='chosen_pokemons', to='battles.Battle'),
        ),
    ]
