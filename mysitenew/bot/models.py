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

import os
import base64

def GetRndStr():    
    rndByte = os.urandom(6)
    b64Str = base64.urlsafe_b64encode(rndByte)
    return b64Str

#Line Bot-----------------------------------------------
class LineBot(models.Model):
    UserId = models.ForeignKey(User)#CharField(max_length=100)
    IdentifyingCode = models.CharField(max_length=20, default='SOME STRING')
    LineId = models.CharField(max_length=20)#CharField(max_length=100)
    def __str__(self):
        return self.LineId

def CreateLinePerson(userID):
    LineBot.objects.create(UserId=userID,IdentifyingCode="#"+GetRndStr())
    def __str__(self):
        return self.IdentifyingCode

# Create your models here.
def IdentifyPerson(event):
     print event.message.text
     user=LineBot.objects.select_for_update().filter(IdentifyingCode=event.message.text)[0]#這行原本是比對username 現在改為比對亂碼即可
     user.LineId = event.source.user_id#如果比對符合就創建
     user.save()
     ########!!!!!!!!要多寫一個比對不符合的防呆!!!!!!!!!#############
     print event.message.text
def SendMessage():
    message = TextSendMessage(text="Hijiji")
    exchanges = AlgTypeByUser.objects.values('Head','Foot').annotate(num = Count('userID'))#知道有哪些交易所配對
    for exchange in exchanges:
        id = AlgTypeByUser.objects.filter(Head = exchange['Head'],Foot = exchange['Foot']).values('userID')#尋找每個符合配對交易所的user們
        for people in id:
            print people['userID']
            try:#寄送訊息 用try主因是怕有order但他卻沒註冊linebot
                lineId = LineBot.objects.get(UserId = people['userID'])
                print lineId
                line_bot_api.push_message(lineId.LineId,message)
            except:
                print "this person is not in bot's db"
