# -*- coding: utf-8 -*-
from __future__ import unicode_literals
from django.contrib import admin
from .models import LineBot,BotRecord,Feedback
admin.site.register(BotRecord)
admin.site.register(Feedback)   
admin.site.register(LineBot)      #-----1
