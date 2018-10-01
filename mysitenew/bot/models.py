# -*- coding: utf-8 -*-
from __future__ import unicode_literals
import json
from django.db import models
from users.models import User
from linebot import LineBotApi, WebhookParser
from linebot.exceptions import InvalidSignatureError, LineBotApiError
from linebot.models import MessageEvent, TextSendMessage, TemplateSendMessage, ButtonsTemplate, MessageTemplateAction, CarouselTemplate, CarouselColumn, TemplateAction, URIAction, MessageAction
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
class BotRecord(models.Model):
    userID = models.ForeignKey(User)
    HeadTransection = models.CharField(max_length=100)
    FootTransection = models.CharField(max_length=100)
    Profit = models.FloatField(default = 0.0)
#Line Bot-----------------------------------------------
class LineBot(models.Model):
    # UserId = models.ForeignKey(User)#CharField(max_length=100)
    UserId = models.CharField(max_length=20)
    IdentifyingCode = models.CharField(max_length=20, default='SOME STRING')
    LineId = models.CharField(max_length=50)#CharField(max_length=100)
    def __str__(self):
        return self.LineId

class Feedback(models.Model):
    Opinion = models.CharField(max_length=512, default='SOME STRING')
    LineId = models.CharField(max_length=50)
    def __str__(self):
        return self.LineId

def CreateLinePerson(userID):
    IdentifyingCode="#"+GetRndStr()
    LineBot.objects.create(UserId=userID,IdentifyingCode=IdentifyingCode)
    return IdentifyingCode
    
def IdentifyPerson(event):
     print event.message.text
     user=LineBot.objects.filter(IdentifyingCode=event.message.text)[0]#這行原本是比對username 現在改為比對亂碼即可
     user.LineId = event.source.user_id#如果比對符合就創建
     user.save()
     ########!!!!!!!!要多寫一個比對不符合的防呆!!!!!!!!!#############
     print event.message.text

def CreateFeedback(event):
    text = event.message.text
    Feedback.objects.create(LineId=event.source.user_id,Opinion=text[1:len(text)])
    return event.message.text

def SendMessage(paths):
    for path in paths:
        i=0
        Carousel_template = TemplateSendMessage(
            alt_text='Carousel template',
            template=CarouselTemplate(
                columns=Makecolumn(path["Path"],path["Profit"])
            )
        )
        SendMessageByUserId(2,Carousel_template)
    # # message = TextSendMessage(text="Hijiji")
    #     # exchanges = AlgTypeByUser.objects.values('Head','Foot').annotate(num = Count('userID'))#知道有哪些交易所配對

        head = path["Path"][0][0]
        foot = path["Path"][len(path["Path"])-1][0]
        id = AlgTypeByUser.objects.filter(Head = head,Foot = foot).values('userID')#尋找每個符合配對交易所的user們
        # print type(paths)
        print path["Path"][0][0],path["Path"][len(path["Path"])-1][0],id,"!!!!!!!!!!"
        for people in id:
            print people#['userID']
            try:#寄送訊息 用try主因是怕有order但他卻沒註冊linebot
                lineId = LineBot.objects.get(UserId = people['userID'])
                print lineId.LineId,type(lineId.LineId),"###"
                line_bot_api.push_message(str(lineId.LineId),Carousel_template)
                print "send!"
            except Exception as e:
                print "this person is not in bot's db"
            users = User.objects.get(userID = people['userID'])
            BotRecord.objects.create(userID = users , HeadTransection = head , FootTransection = foot , Profit=path["Profit"])
                
        i=i+1
def Makecolumn(exchanges,profit):
    columns = []
    i=0
    for num in range(0,len(exchanges),+3):
        if num+1 >= len(exchanges):
            return columns
        column = CarouselColumn(
                    thumbnail_image_url = "https://i.imgur.com/NLs4V15.png",
                    title='part'+str(i+1),
                    text='profit' + str(profit),
                    actions=MakeAction(exchanges,num)
                 )
        columns.append(column)
        i=i+1
    return columns

def MakeAction(exchanges,nums):
    actions = []
    
    print len(exchanges)
    for num in range(nums,nums+3):
        text = "《"+exchanges[num][0]+exchanges[num][1]+"->"+exchanges[num+1][0]+exchanges[num+1][1]+"》\n在"+exchanges[num][0]+"賣"+exchanges[num+1][1]+"換"+exchanges[num][1]+"(用"+exchanges[num+1][1]+"買"+exchanges[num][0]+")\n在"+exchanges[num][1]+"賣"+exchanges[num+1][0]+"換"+exchanges[num][0]+"(用"+exchanges[num+1][0]+"買"+exchanges[num][1]+")"
        action = MessageTemplateAction(label=exchanges[num][0][0:5]+"->"+exchanges[num+1][0][0:5],text=text)
        actions.append(action)
        if num+2 >= len(exchanges) or num+1 >= len(exchanges):
            break
    action = MessageTemplateAction(label="___",text="___")
    if len(actions) % 3 == 1:
        actions.append(action)
        actions.append(action)
    elif len(actions) % 3 == 2:
        actions.append(action)
    return actions

def ReplyCommonMessage():
    buttons_template_message = TemplateSendMessage(
        alt_text='Buttons template',
        template=ButtonsTemplate(
            thumbnail_image_url='https://i.imgur.com/NLs4V15.png',
            title='Richer主選單',
            text='有什麼能幫上忙的嗎',
            actions=[
                MessageAction(
                    label='聯絡我們',
                    text='聯絡我們',
                ),
                MessageAction(
                    label='交易所資訊',
                    text='交易所資訊'
                ),
                URIAction(
                    label='Richer是做什麼用的?',
                    uri='https://agile-sea-25500.herokuapp.com/index/'
                ),
                MessageAction(
                    label='意見回饋',
                    text='意見回饋'
                )
            ]
        )
    )
    return buttons_template_message

def AskExchangeInfo():
    buttons_template_message = TemplateSendMessage(
        alt_text='Buttons template',
        template=ButtonsTemplate(
            thumbnail_image_url='https://i.imgur.com/NLs4V15.png',
            title='交易所資訊',
            text='四家交易所網址',
            actions=[
                URIAction(
                label='CEX',
                uri='https://cex.io/btc-usd'
                ),
                URIAction(
                label='Bittrex',
                uri='https://bittrex.com/home/markets'
                ),
                URIAction(
                label='Bitfinex',
                uri='https://www.bitfinex.com/'
                ),
                URIAction(
                label='C ryptopia',
                uri='https://www.cryptopia.co.nz/CoinInfo/?coin=DOT'
                )
            ]
        )
    )
    return buttons_template_message

def SendMessageByUserId(userID,message): 
    #user = User.objects.get(userID='1') 
    #user=User.objects.get(username='testbot') 
    lineId = LineBot.objects.get(UserId = userID) 
    #print "~~~",lineId 
    #a=request.GET.get('user', '') 
    #message = TextSendMessage(text="123") 
    line_bot_api.push_message(lineId.LineId,message) 