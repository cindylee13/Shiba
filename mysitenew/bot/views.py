from django.conf import settings
from django.http import HttpResponse, HttpResponseBadRequest, HttpResponseForbidden
from django.views.decorators.csrf import csrf_exempt
from .models import CreatePerson,SendMessageByUserId
from linebot import LineBotApi, WebhookParser
from linebot.exceptions import InvalidSignatureError, LineBotApiError
from linebot.models import MessageEvent, TextSendMessage
from django.shortcuts import render

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
            if isinstance(event, MessageEvent):
                #CreatePerson(event)
                print event.source.user_id
                #print MessageEvent
        return HttpResponse()
    else:
        return HttpResponseBadRequest()

def test(request):
    """message = TextSendMessage(text="Hi")
    line_bot_api.push_message(
                    "Ue57fa91c43eaa81668118fc713a7d47f",
                   message
                )"""
    a=request.POST#.data
    print "aaaaa=",a
    SendMessageByUserId(1,a)
    return render(request,"trading.html")
