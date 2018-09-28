# -*- coding: utf-8 -*-
from __future__ import unicode_literals
from django.contrib import admin
from .models import LineBot,BotRecord
admin.site.register(BotRecord)
admin.site.register(LineBot)      #-----1
