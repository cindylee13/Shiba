# -*- coding: utf-8 -*-
from __future__ import unicode_literals
import json
from django.db import models
from users.models import User

#Line Bot-----------------------------------------------
class LineBot(models.Model):
	LineId = models.CharField(max_length=20)#CharField(max_length=100)
	UserId = models.ForeignKey(User)#CharField(max_length=100)
	def __str__(self):
		return '%s' % (self.LineId)

# Create your models here.
def FindPerson(event):
     print event.message.text
     user=User.objects.get(username=event.message.text)
     #user = User.objects.get(userID='2')
     LineBot.objects.create(LineId=event.source.user_id,UserId=user)
     print event.message.text
def SendMessageByUserId(event,Id):
    lineId = LineBot.objects.filiter(userID=Id)['LineId']
