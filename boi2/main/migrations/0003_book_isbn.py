# -*- coding: utf-8 -*-
# Generated by Django 1.9 on 2018-04-22 05:06
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('main', '0002_auto_20180404_1331'),
    ]

    operations = [
        migrations.AddField(
            model_name='book',
            name='ISBN',
            field=models.CharField(default='', max_length=20),
        ),
    ]
