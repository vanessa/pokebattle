# -*- coding: utf-8 -*-
# Generated by Django 1.11.13 on 2018-05-16 22:04
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('battles', '0018_invite_key'),
    ]

    operations = [
        migrations.AlterField(
            model_name='invite',
            name='key',
            field=models.CharField(blank=True, max_length=12, null=True, unique=True, verbose_name='Invitation key'),
        ),
    ]
