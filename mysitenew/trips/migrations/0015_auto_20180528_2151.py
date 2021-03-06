# -*- coding: utf-8 -*-
# Generated by Django 1.11.13 on 2018-05-28 13:51
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('trips', '0014_auto_20180317_1759'),
    ]

    operations = [
        migrations.CreateModel(
            name='Difference',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('BidTransection', models.CharField(max_length=20)),
                ('AskTransection', models.CharField(max_length=20)),
                ('Bid', models.FloatField(default=0)),
                ('Ask', models.FloatField(default=0)),
                ('created_at', models.DateTimeField(auto_now=True)),
            ],
        ),
        migrations.AlterModelOptions(
            name='binancebtctable',
            options={'ordering': ['created_at']},
        ),
        migrations.AlterModelOptions(
            name='bitfinexbtctable',
            options={'ordering': ['created_at']},
        ),
        migrations.AlterModelOptions(
            name='bittrexbtctable',
            options={'ordering': ['created_at']},
        ),
        migrations.AlterModelOptions(
            name='cexbtctable',
            options={'ordering': ['created_at']},
        ),
        migrations.AlterModelOptions(
            name='cryptopiabtctable',
            options={'ordering': ['created_at']},
        ),
    ]
