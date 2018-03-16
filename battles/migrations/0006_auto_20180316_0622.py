# -*- coding: utf-8 -*-
# Generated by Django 1.11.11 on 2018-03-16 06:22
from __future__ import unicode_literals

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('battles', '0005_auto_20180316_0617'),
    ]

    operations = [
        migrations.AlterField(
            model_name='chosenpokemon',
            name='battle_related',
            field=models.ForeignKey(default=0, on_delete=django.db.models.deletion.CASCADE, related_name='chosen_pokemons', to='battles.Battle'),
            preserve_default=False,
        ),
    ]
