# -*- coding: utf-8 -*-
# Generated by Django 1.11.13 on 2018-05-21 17:00
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('battles', '0021_remove_invite_accepted'),
    ]

    operations = [
        migrations.AddField(
            model_name='invite',
            name='accepted',
            field=models.BooleanField(default=False, verbose_name='User has accepted this invite'),
        ),
    ]