# -*- coding: utf-8 -*-
# Generated by Django 1.11.10 on 2018-08-28 16:39
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('bot', '0001_initial'),
    ]

    operations = [
        migrations.AddField(
            model_name='linebot',
            name='IdentifyingCode',
            field=models.CharField(default='SOME STRING', max_length=20),
        ),
    ]
