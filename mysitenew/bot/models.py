# -*- coding: utf-8 -*-
from __future__ import unicode_literals
import json
from django.db import models
from users.models import User
from linebot import LineBotApi, WebhookParser
from linebot.exceptions import InvalidSignatureError, LineBotApiError
from linebot.models import MessageEvent, TextSendMessage
from django.conf import settings
from trips.models import AlgTypeByUser
from django.db.models import Count
line_bot_api = LineBotApi(settings.LINE_CHANNEL_ACCESS_TOKEN)
parser = WebhookParser(settings.LINE_CHANNEL_SECRET)

#Line Bot-----------------------------------------------
class LineBot(models.Model):
    LineId = models.CharField(max_length=50)#CharField(max_length=100)
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
def SendMessage():
    message = TextSendMessage(text="Hijiji")
    exchanges = AlgTypeByUser.objects.values('Head','Foot').annotate(num = Count('userID'))
    print exchanges#.objects.all()
    for exchange in exchanges:
        id = AlgTypeByUser.objects.filter(Head = exchange['Head'],Foot = exchange['Foot']).values('userID')
        for people in id:
            print people['userID']
            try:
                lineId = LineBot.objects.get(UserId = people['userID'])
                print lineId
                line_bot_api.push_message(lineId.LineId,message)
            except:
                print "this person is not in bot's db"
