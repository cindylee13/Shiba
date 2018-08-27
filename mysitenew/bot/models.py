# -*- coding: utf-8 -*-
from __future__ import unicode_literals
import json
from django.db import models
from users.models import User
from linebot import LineBotApi, WebhookParser
from linebot.exceptions import InvalidSignatureError, LineBotApiError
from linebot.models import MessageEvent, TextSendMessage
from django.conf import settings
line_bot_api = LineBotApi(settings.LINE_CHANNEL_ACCESS_TOKEN)
parser = WebhookParser(settings.LINE_CHANNEL_SECRET)

#Line Bot-----------------------------------------------
class LineBot(models.Model):
    LineId = models.CharField(max_length=20)#CharField(max_length=100)
    UserId = models.ForeignKey(User)#CharField(max_length=100)
    def __str__(self):
        return self.LineId

# Create your models here.
def CreatePerson(event):
     print event.message.text
     user=User.objects.get(username = event.message.text)#這行原本是比對username 現在改為比對亂碼即可
     #user = User.objects.get(userID='2')
     LineBot.objects.create(LineId = event.source.user_id,UserId=user)#如果比對符合就創建
     ########!!!!!!!!要多寫一個比對不符合的防呆!!!!!!!!!#############
     print event.message.text
def SendMessageByUserId(Id,message):
    #user = User.objects.get(userID='1')
    #user=User.objects.get(username='testbot')
    lineId = LineBot.objects.get(UserId = Id)
    #print "~~~",lineId
    #a=request.GET.get('user', '')
    #message = TextSendMessage(text="123")
    line_bot_api.push_message(lineId.LineId,message)
