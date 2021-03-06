from django.http import HttpResponse
from django.shortcuts import render
from datetime import datetime
from .models import BittrexBTCTable,CexBTCTable,BinanceBTCTable,BitfinexBTCTable,CryptopiaBTCTable
from .models import BittrexETHTable,CexETHTable,BinanceETHTable,BitfinexETHTable,CryptopiaETHTable
from .transection import main,test
from .models import TransectionRecord
from .models import GetDifference

from django.core import serializers
transection=[BittrexBTCTable,CexBTCTable,BinanceBTCTable,BitfinexBTCTable,CryptopiaBTCTable]

def BTC(request):
    #a = BittrexBTC()    //move to crontab
    BittrexList = ChangeDateGetObjects(BittrexBTCTable)
    #BittrexList = BittrexBTCTable.objects.all()
    #b = CexBTC()
    CexList = ChangeDateGetObjects(CexBTCTable)
    #c = BinanceBTC()
    BinanceList = ChangeDateGetObjects(BinanceBTCTable)

    #d = BitfinexBTC()
    BitfinexList = ChangeDateGetObjects(BitfinexBTCTable)

    #e = CryptopiaBTC()
    CryptopiaList = ChangeDateGetObjects(CryptopiaBTCTable)
    dif=GetDifference()


    return render(request, 'BTC.html', {
        'current_time': str(datetime.now()), 
        'BittrexBTCTable' : BittrexList, 
        'CexBTCTable' : CexList,
        'BinanceBTCTable' : BinanceList,
        'BitfinexBTCTable' : BitfinexList,
        'CryptopiaBTCTable' : CryptopiaList,
        'dif':dif,
    })
def Trading(request):
    #a = BittrexBTC()    #move to crontab
    #print a
    #BittrexList = ChangeDateGetObjects(BittrexBTCTable)
    BittrexList = BittrexBTCTable.objects.all()
    CexList = CexBTCTable.objects.all()
    BinanceList = BinanceBTCTable.objects.all()
    BitfinexList = BitfinexBTCTable.objects.all()
    CryptopiaList = CryptopiaBTCTable.objects.all()

    BittrexETHList = BittrexETHTable.objects.all()
    CexETHList = CexETHTable.objects.all()
    BinanceETHList = BinanceETHTable.objects.all()
    BitfinexETHList = BitfinexETHTable.objects.all()
    CryptopiaETHList = CryptopiaETHTable.objects.all()
    #TransectionRecord=TransectionRecord.objects.all()
    #BittrexList = json.dumps(BittrexList)
    #b = CexBTC()
    #CexList = ChangeDateGetObjects(CexBTCTable)
    #c = BinanceBTC()
    #BinanceList = ChangeDateGetObjects(BinanceBTCTable)

    #d = BitfinexBTC()
    #BitfinexList = ChangeDateGetObjects(BitfinexBTCTable)

    #e = CryptopiaBTC()
    #CryptopiaList = ChangeDateGetObjects(CryptopiaBTCTable)
    records=TransectionRecord.objects.all()
    #dif=GetDifference()
    return render(request, 'trading.html', {
        #'current_time': str(datetime.now()), 
        'BittrexBTCTable' : BittrexList[0:500], 
        'CexBTCTable' : CexList[0:500],
        'BinanceBTCTable' : BinanceList,
        'BitfinexBTCTable' : BitfinexList,
        'CryptopiaBTCTable' : CryptopiaList,
        'BittrexETHTable' : BittrexETHList[0:500], 
        'CexETHTable' : CexETHList[0:500],
        'BinanceETHTable' : BinanceETHList,
        'BitfinexETHTable' : BitfinexETHList,
        'CryptopiaETHTable' : CryptopiaETHList,
        'Transection' : records
    })
def userInfo(request):
    if request.method == "POST":
        firstdate=request.POST.get("firstDate",None)
        lastdate=request.POST.get("lastDate",None)
        aa,bb = main(firstdate,lastdate)

    return render(request,"trading.html",{"a":aa,"b":bb})

def index1(request):
    #ans={}
    #ans['head']='hello sunny!'
    uu=GetUserID()
    a = index1()
    return render(request,'BTC.html',{'ans':a})
