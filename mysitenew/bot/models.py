# -*- coding: utf-8 -*-
from __future__ import unicode_literals
import json
from django.db import models
from users.models import User
from linebot import LineBotApi, WebhookParser
from linebot.exceptions import InvalidSignatureError, LineBotApiError
from linebot.models import MessageEvent, TextSendMessage, TemplateSendMessage, ButtonsTemplate, MessageTemplateAction, CarouselTemplate, CarouselColumn, TemplateAction
from django.conf import settings
from trips.models import AlgTypeByUser
from django.db.models import Count
from users.models import GetUserID
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
    # UserId = models.ForeignKey(User)#CharField(max_length=100)
    UserId = models.CharField(max_length=20)
    IdentifyingCode = models.CharField(max_length=20, default='SOME STRING')
    LineId = models.CharField(max_length=20)#CharField(max_length=100)
    def __str__(self):
        return self.LineId

def CreateLinePerson(userID):
    IdentifyingCode="#"+GetRndStr()
    LineBot.objects.create(UserId=userID,IdentifyingCode=IdentifyingCode)
    return IdentifyingCode
    
def IdentifyPerson(event):
     print event.message.text
     user=LineBot.objects.select_for_update().filter(IdentifyingCode=event.message.text)[0]#這行原本是比對username 現在改為比對亂碼即可
     user.LineId = event.source.user_id#如果比對符合就創建
     user.save()
     ########!!!!!!!!要多寫一個比對不符合的防呆!!!!!!!!!#############
     print event.message.text



def SendMessage(paths):
    for path in paths:
            # print "!"
            # print path["Path"][0][1]
        i=0
        Carousel_template = TemplateSendMessage(
            alt_text='Carousel template',
            template=CarouselTemplate(
                columns=Makecolumn(path["Path"])
            )
        )
        SendMessageByUserId(1,Carousel_template)
    # # message = TextSendMessage(text="Hijiji")
    #     # exchanges = AlgTypeByUser.objects.values('Head','Foot').annotate(num = Count('userID'))#知道有哪些交易所配對
        head = path["Path"][0]
        foot = path["Path"][len(path["Path"]-1)]
        id = AlgTypeByUser.objects.filter(Head = head,Foot = foot).values('userID')#尋找每個符合配對交易所的user們
        # print type(paths)
        
        for people in id:
            print people['userID']
            try:#寄送訊息 用try主因是怕有order但他卻沒註冊linebot
                lineId = LineBot.objects.get(UserId = people['userID'])
                print lineId
                line_bot_api.push_message(lineId.LineId,Carousel_template)
            except:
                print "this person is not in bot's db"
                
        i=i+1
def Makecolumn(exchanges):
    columns = []
    i=0
    for num in range(0,len(exchanges),+3):
        
        column = CarouselColumn(
                    thumbnail_image_url = "https://i.imgur.com/NLs4V15.png",
                    title='part'+str(i+1),
                    text='part'+str(i+1),
                    actions=MakeAction(exchanges,num)
                 )
        columns.append(column)
        if num+2 >= len(exchanges):
            return columns
        i=i+1
    return columns

def MakeAction(exchanges,nums):
    actions = []
    # print exchanges[nums]
    for num in range(nums,nums+3):
        action = MessageTemplateAction(label='請點擊我!!!',text=exchanges[num][0]+exchanges[num][1]+"->"+exchanges[num+1][0]+exchanges[num+1][1])
        actions.append(action)
        if num+2 >= len(exchanges):
            break
    action = MessageTemplateAction(label="___",text="___")
    if len(actions) % 3 == 1:
        actions.append(action)
        actions.append(action)
    elif len(actions) % 3 == 2:
        actions.append(action)
    return actions

def SendMessageByUserId(userID,message): 
    #user = User.objects.get(userID='1') 
    #user=User.objects.get(username='testbot') 
    lineId = LineBot.objects.get(UserId = userID) 
    #print "~~~",lineId 
    #a=request.GET.get('user', '') 
    #message = TextSendMessage(text="123") 
    line_bot_api.push_message(lineId.LineId,message) 