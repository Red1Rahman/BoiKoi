# -*- coding: utf-8 -*-
# Generated by Django 1.11 on 2018-04-26 03:03
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('main', '0010_auto_20180426_0827'),
    ]

    operations = [
        migrations.AddField(
            model_name='profile',
            name='address',
            field=models.CharField(blank=True, max_length=500),
        ),
    ]