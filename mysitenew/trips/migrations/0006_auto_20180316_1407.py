# -*- coding: utf-8 -*-
# Generated by Django 1.11.11 on 2018-03-16 06:07
from __future__ import unicode_literals

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('trips', '0005_auto_20180316_1105'),
    ]

    operations = [
        migrations.DeleteModel(
            name='Post',
        ),
        migrations.DeleteModel(
            name='Price',
        ),
    ]
