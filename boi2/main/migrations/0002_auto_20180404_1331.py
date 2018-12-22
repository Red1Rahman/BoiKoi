# -*- coding: utf-8 -*-
# Generated by Django 1.9 on 2018-04-04 07:31
from __future__ import unicode_literals

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('main', '0001_initial'),
    ]

    operations = [
        migrations.CreateModel(
            name='Friend',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('date', models.DateField(default='2000-01-01')),
            ],
        ),
        migrations.CreateModel(
            name='Listing',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('amount', models.IntegerField(default=1)),
                ('mode', models.CharField(max_length=10)),
            ],
        ),
        migrations.CreateModel(
            name='TransferLog',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('date', models.DateField(default='2000-01-01')),
            ],
        ),
        migrations.RenameModel(
            old_name='Booklist',
            new_name='Book',
        ),
        migrations.AlterField(
            model_name='profile',
            name='joinDate',
            field=models.DateField(default='2000-01-01'),
        ),
        migrations.AddField(
            model_name='transferlog',
            name='book',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='main.Book'),
        ),
        migrations.AddField(
            model_name='transferlog',
            name='provider',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='Provider', to='main.Profile'),
        ),
        migrations.AddField(
            model_name='transferlog',
            name='receiver',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='Receiver', to='main.Profile'),
        ),
        migrations.AddField(
            model_name='listing',
            name='book',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='main.Book'),
        ),
        migrations.AddField(
            model_name='listing',
            name='user',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='main.Profile'),
        ),
        migrations.AddField(
            model_name='friend',
            name='user1',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='Friend1', to='main.Profile'),
        ),
        migrations.AddField(
            model_name='friend',
            name='user2',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='Friend2', to='main.Profile'),
        ),
    ]