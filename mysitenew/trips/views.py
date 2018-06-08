from django.http import HttpResponse
from django.shortcuts import render
from datetime import datetime
from .models import BittrexBTCTable, BittrexBTC 
from .transection import main,test
from .models import CexBTCTable, CexBTC
from .models import BinanceBTCTable, BinanceBTC,TransectionRecord
from .models import BitfinexBTCTable, BitfinexBTC
from .models import CryptopiaBTCTable, CryptopiaBTC,GetDifference
from pyspark import SQLContext,SparkConf,SparkContext
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
def TestSpark(request):
    sc = SparkContext("local", "first app")
    spark=SparkSession.builder.master("local").appName("first app").config("spark.some.config.option","some-value").getOrCreate()
    logFile = "file:///Users/sunny/Desktop/CheckIn.csv"
    logData = sc.textFile(logFile)
    Data=logData.map(lambda a:a.split(','))
    people = Data.map(lambda p: (p[0], regex(str(p[1])) ,p[2],p[3],p[4].strip()))
    return render(request,"error.html",{"a":people})


def Trading(request):
    #a = BittrexBTC()    #move to crontab
    #print a
    BittrexList = ChangeDateGetObjects(BittrexBTCTable)
    #BittrexList = BittrexBTCTable.objects.all()
    b = CexBTC()
    CexList = ChangeDateGetObjects(CexBTCTable)
    c = BinanceBTC()
    BinanceList = ChangeDateGetObjects(BinanceBTCTable)

    d = BitfinexBTC()
    BitfinexList = ChangeDateGetObjects(BitfinexBTCTable)

    e = CryptopiaBTC()
    CryptopiaList = ChangeDateGetObjects(CryptopiaBTCTable)
    records=TransectionRecord.objects.all()
    #dif=GetDifference()
    return render(request, 'trading.html', {
        #'current_time': str(datetime.now()), 
        'BittrexBTCTable' : BittrexList[0:500], 
        'CexBTCTable' : CexList[0:500],
        'BinanceBTCTable' : BinanceList,
        'BitfinexBTCTable' : BitfinexList,
        'CryptopiaBTCTable' : CryptopiaList,
    })

def ChangeDateGetObjects(table):
    rows = table.objects.all()
    for row in rows[0:500]:
        row.created_at=row.created_at.strftime('20%y-%m-%d %H:%M:%S')
    return rows
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
