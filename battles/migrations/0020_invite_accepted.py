# -*- coding: utf-8 -*-
# Generated by Django 1.11.13 on 2018-05-21 16:31
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('battles', '0019_auto_20180516_2204'),
    ]

    operations = [
        migrations.AddField(
            model_name='invite',
            name='accepted',
            field=models.BooleanField(default=False, verbose_name='User has accepted this invite'),
        ),
    ]
