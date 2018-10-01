# -*- coding: utf-8 -*-
from __future__ import unicode_literals
from django.conf import settings
from django.http import HttpResponse, HttpResponseBadRequest, HttpResponseForbidden
from django.views.decorators.csrf import csrf_exempt
from .models import IdentifyPerson,SendMessage, ReplyCommonMessage, AskExchangeInfo, CreateFeedback
from linebot import LineBotApi, WebhookParser
from linebot.exceptions import InvalidSignatureError, LineBotApiError
from linebot.models import MessageEvent, TextSendMessage , JoinEvent
from django.shortcuts import render
import json
line_bot_api = LineBotApi(settings.LINE_CHANNEL_ACCESS_TOKEN)
parser = WebhookParser(settings.LINE_CHANNEL_SECRET)

@csrf_exempt
def callback(request):
    if request.method == 'POST':
        signature = request.META['HTTP_X_LINE_SIGNATURE']
        body = request.body.decode('utf-8')
        try:
            events = parser.parse(body, signature)
        except InvalidSignatureError:
            return HttpResponseForbidden()
        except LineBotApiError:
            return HttpResponseBadRequest()
        #print events[0].source.userId
        for event in events:
            # a=event.message.text
            if (event.message.text)[0] == "#":
                message = TextSendMessage(text="綁定成功!!")
                try:
                    IdentifyPerson(event)
                except Exception as e:
                    print "IdentifyFail!",e
                    message = TextSendMessage(text="綁定失敗請確認有無輸入錯誤!!")
                line_bot_api.reply_message(event.reply_token,message)
                print event.source.user_id
            elif (event.message.text)[0] == "$":
                message = TextSendMessage(text="已收到您的建議 謝謝您!")
                CreateFeedback(event)
                line_bot_api.reply_message(event.reply_token,message)
                print event.source.user_id
            elif (event.message.text)[0] == "《":
                print event.source.user_id
            elif (event.message.text) == "聯絡我們":
                message = TextSendMessage(text="Richer電話:\n0915-010-368\n服務時間:週一至週五 09:00-18:00")
                line_bot_api.reply_message(event.reply_token,message)
            elif (event.message.text) == "交易所資訊":
                message = AskExchangeInfo()
                line_bot_api.reply_message(event.reply_token,message)
            elif (event.message.text) == "意見回饋":
                message =  TextSendMessage(text="只要在訊息的最前面加上$號就能將意見回饋給我們唷!!\n EX: $我覺得你們這個網頁做的很棒 幫我縮減很多時間 我看到你們的可塑性!")
                line_bot_api.reply_message(event.reply_token,message)
            elif isinstance(event, MessageEvent):
                message = ReplyCommonMessage()
                line_bot_api.reply_message(event.reply_token,message)
                print event.source.user_id
                #print MessageEvent
        return HttpResponse()
    else:
        return HttpResponseBadRequest()

def test(request):
    message = TextSendMessage(text="Hi 使用者你好請至信箱收取您的驗證碼/n並回傳給本帳戶我們將會進行綁定")
    line_bot_api.push_message(
                    "Ufb17e663bbe69c3b0e43b659364c269b",
                   message
                )
    a=request.POST#.data
    print "aaaaa=",a
    # SendMessageByUserId(1,a)
    return render(request,"trading.html")
def call(request):
    a = json.loads(request.body.decode('utf-8'))
    print a,"~~~"
    SendMessage(a)
    return render(request,"trading.html")




