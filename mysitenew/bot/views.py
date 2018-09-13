# -*- coding: utf-8 -*-
from __future__ import unicode_literals
from django.conf import settings
from django.http import HttpResponse, HttpResponseBadRequest, HttpResponseForbidden
from django.views.decorators.csrf import csrf_exempt
from .models import IdentifyPerson,SendMessage
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
            a=event.message.text
            if (event.message.text)[0] == "#":
                message = TextSendMessage(text="綁定成功!!")
                try:
                    IdentifyPerson(event)
                except:
                    print "IdentifyFail"
                    message = TextSendMessage(text="綁定失敗請確認有無輸入錯誤!!")
                line_bot_api.reply_message(event.reply_token,message)
                print event.source.user_id
            elif isinstance(event, MessageEvent):
                message = TextSendMessage(text="閉嘴")
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
    SendMessage(a)
    print "!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!"
    print a
    return render(request,"trading.html")




