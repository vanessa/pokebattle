# -*- coding: utf-8 -*-
# Generated by Django 1.11.11 on 2018-03-16 06:26
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('pokemons', '0002_auto_20180316_0625'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='pokemon',
            name='_id',
        ),
        migrations.AlterField(
            model_name='pokemon',
            name='id',
            field=models.SmallIntegerField(primary_key=True, serialize=False, verbose_name="Pokemon's ID"),
        ),
    ]