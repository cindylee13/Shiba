# -*- coding: utf-8 -*-
<<<<<<< Updated upstream
# Generated by Django 1.11.13 on 2018-09-17 20:55
=======
# Generated by Django 1.11.13 on 2018-09-17 20:32
>>>>>>> Stashed changes
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('trips', '0017_algtypebyuser'),
    ]

    operations = [
        migrations.CreateModel(
            name='BinanceETHTable',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('ask', models.FloatField(default=0)),
                ('bid', models.FloatField(default=0)),
                ('last', models.CharField(max_length=100)),
                ('created_at', models.DateTimeField(auto_now=True)),
            ],
            options={
                'ordering': ['created_at'],
            },
        ),
        migrations.CreateModel(
            name='BitfinexETHTable',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('ask', models.FloatField(default=0)),
                ('bid', models.FloatField(default=0)),
                ('last', models.CharField(max_length=100)),
                ('created_at', models.DateTimeField(auto_now=True)),
            ],
            options={
                'ordering': ['created_at'],
            },
        ),
        migrations.CreateModel(
            name='BittrexETHTable',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('ask', models.FloatField(default=0)),
                ('bid', models.FloatField(default=0)),
                ('last', models.CharField(max_length=100)),
                ('created_at', models.DateTimeField(auto_now=True)),
            ],
            options={
                'ordering': ['created_at'],
            },
        ),
        migrations.CreateModel(
            name='CexETHTable',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('ask', models.FloatField(default=0)),
                ('bid', models.FloatField(default=0)),
                ('last', models.CharField(max_length=100)),
                ('created_at', models.DateTimeField(auto_now=True)),
            ],
            options={
                'ordering': ['created_at'],
            },
        ),
        migrations.CreateModel(
            name='CryptopiaETHTable',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('ask', models.FloatField(default=0)),
                ('bid', models.FloatField(default=0)),
                ('last', models.CharField(max_length=100)),
                ('created_at', models.DateTimeField(auto_now=True)),
            ],
            options={
                'ordering': ['created_at'],
            },
        ),
    ]
