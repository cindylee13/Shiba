# -*- coding: utf-8 -*-
from django.http import HttpResponse
from django.shortcuts import render
from datetime import datetime
from .models import BittrexBTCTable, BittrexBTC 
from .models import CexBTCTable, CexBTC
from .models import BinanceBTCTable, BinanceBTC
from .models import BitfinexBTCTable, BitfinexBTC 
from .models import CryptopiaBTCTable, CryptopiaBTC,GetDifference

transection=[BittrexBTCTable,CexBTCTable,BinanceBTCTable,BitfinexBTCTable,CryptopiaBTCTable]

def BTC(request):
    #a = BittrexBTC()    //move to crontab
    BittrexList = BittrexBTCTable.objects.all()

    #b = CexBTC()
    CexList = CexBTCTable.objects.all()

    #c = BinanceBTC()
    BinanceList = BinanceBTCTable.objects.all()

    #d = BitfinexBTC()
    BitfinexList = BitfinexBTCTable.objects.all()

    #e = CryptopiaBTC()
    CryptopiaList = CryptopiaBTCTable.objects.all()
    dif=GetDifference()
    return render(request, 'BTC.html', {
        'current_time': str(datetime.now()), 
        'BittrexBTCTable' : BittrexList, 
        'CexBTCTable' : CexList,
        'BinanceBTCTable' : BinanceList,
        'BitfinexBTCTable' : BitfinexList,
        'CryptopiaBTCTable' : CryptopiaList,
        'dif':dif,
        'transection':transection
    })


def index1(request):
    #ans={}
    #ans['head']='hello sunny!'
    a = index1()
    return render(request,'BTC.html',{'ans':a})
