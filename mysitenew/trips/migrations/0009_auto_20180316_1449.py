# -*- coding: utf-8 -*-
# Generated by Django 1.11.11 on 2018-03-16 06:49
from __future__ import unicode_literals

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('trips', '0008_auto_20180316_1440'),
    ]

    operations = [
        migrations.RenameModel(
            old_name='CoinTable',
            new_name='BTCTable',
        ),
    ]
