# -*- coding: utf-8 -*-
# Generated by Django 1.11 on 2018-05-05 11:52
from __future__ import unicode_literals

from django.db import migrations, models
import django.utils.timezone


class Migration(migrations.Migration):

    dependencies = [
        ('main', '0023_servermessage'),
    ]

    operations = [
        migrations.AddField(
            model_name='listing',
            name='date',
            field=models.DateTimeField(default=django.utils.timezone.now),
        ),
    ]
