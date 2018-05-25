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
        'transection':transection
    })

def ChangeDateGetObjects(table):
    rows = table.objects.all()
    for row in rows:
        row.created_at=row.created_at.strftime('20%y-%m-%dT%H:%M:%S%Z')
    return rows

def index1(request):
    #ans={}
    #ans['head']='hello sunny!'
    a = index1()
    return render(request,'BTC.html',{'ans':a})
