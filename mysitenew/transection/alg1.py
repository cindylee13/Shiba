# -*- coding: utf-8 -*-
#from django.db import models
#from datetime import datetime, timedelta
#from django.db.models import F, Sum, FloatField, Avg
import sqlite3
#from .models import CexBTCTable,BittrexBTCTable,Purse,TransectionRecord
import time
import requests
import json
import redis
#from models import CallBotByApple 
#from django.db import models
#from django.conf import settings
r = redis.StrictRedis(host='localhost', port=6379, db=0)
def CrawlBittrexBTCUSDT():
        quote_page = "https://bittrex.com/api/v1.1/public/getticker?market=USDT-BTC"
        response = requests.get(quote_page)
        data = response.json()['result']
        #print session.params
        return data['Bid'],data['Ask'],data['Last']
def CrawlCexBTCUSD():
        quote_page = "https://cex.io/api/ticker/BTC/USD"
        response = requests.get(quote_page)
        data = response.json()
        return data['bid'],data['ask'],data['last']
def GetProfit(data):
  cexPrice=data['cex']
  bittrexPrice=data['bittrex']
  print "!!!",data
  #bittrexbid,bittrexask,bittrexlast = CrawlBittrexBTCUSDT()
  #cexbid,cexask,cexlast = CrawlCexBTCUSD()
  cex = cexPrice['bid']*0.9975  - bittrexPrice['ask']*1.0025
  bittrex = bittrexPrice['bid']*0.9975  - cexPrice['ask']*1.0025
  #cex = bittrexbid - 0.0025*bittrexbid - cexask+0.0025*cexask
  #bittrex = cexbid - 0.0025*cexbid - bittrexask+0.0025*cexask
  big = max([cex,bittrex])
  if(big > 0 and big == cex):
    return {'Ask':'Bittrex','Bid':'Cex','Profit':cex}
  elif(big > 0 and big == bittrex):
    return {'Ask':'Cex','Bid':'Bittrex','Profit':bittrex}
  return {'Ask':'none','Bid':'none','Profit':-1}
def GetAvg(infor):
   Avg=0
   try:
      Avg=sum(infor)/len(infor)
   except ZeroDivisionError:
      Avg=0
   return Avg
def GetProfitLine(mean,var):#(var,mean)
   """a=100/(mean+2*var-0.3)
   b=-(0.3*a) (mean+3*var,0)
   (mean-3*var,0) (mean,100) <-this!
   (mean+2*var,0) (mean+4*var,50)
   """
   mean=abs(mean)
   a=100/(3*var)
   b=100-a*mean
   return a,b
def GetLoseLine(earnMean):#(var,mean):
   """a=100/(mean+2*var-0.3)
   b=-(0.3*a) (mean+2*var,0)
   (earnMean,0)      (1,100)
   """
   #print "~~~",earnMean
   a=90/(1-earnMean)
   b=100
   return a,b
def Found(a,b,num):
   p=a*num+b
   if(p<0):
      return 0
   else:
      return a*num+b
def ChangeToBit(fee,transectionFee):
   return float(fee)/float(transectionFee)
def Sell(transection,number,bid):#sell,bitpurse,purse,number):# fee=ratio*puse
	purse=GetPurse()
	print purse[transection+"BTC"],'number'
	if(purse[transection+"BTC"]<number):
		return False
	UpdatePurse(transection+"BTC",purse[transection+"BTC"]-number)
	UpdatePurse(transection+"money",purse[transection+"money"]+number*bid)
	return True
	#purse[transection+'BTC']-=number#bitpurse-=number
	#UpdatePurse()
	#purse+=number*sell
	#return bitpurse,purse
def Buy(transection,number,ask):
	purse=GetPurse()
	if(purse[transection+"money"]<number*ask):
		return False
	UpdatePurse(transection+"BTC",purse[transection+"BTC"]+number)
	UpdatePurse(transection+"money",purse[transection+"money"]-number*ask)
	return True
   #bitpurse+=number
   #purse-=number*buy
   #return bitpurse,purse
def Transection(buyTransection,sellTransection,fee,bid,ask):
   #cexPurse,bittrexPurse,CexBTC,BittrexBTC=GetPurse()
	number=ChangeToBit(fee,ask)
   #if(CexBTC>number and bittrexPurse>number*ask and fee>1):
	if(Sell(sellTransection,number,bid) and fee >1):
		a=Buy(buyTransection,number,ask)
		return a
	return False
"""def Lose(buyTransection,sellTransection,fee,bid,ask):#fee,pursebitt,pursecex,bitbitt,bitcex,price):
   number=ChangeToBit(fee,ask)
number=ChangeToBit(fee,price[4])
   flag=False
   if(bitbitt>number and pursecex>number*price[4] and fee>1):
      bitbitt,pursebitt=Sell(price[3],bitbitt,pursebitt,number)
      bitcex,pursecex=Buy(price[4],bitcex,pursecex,number)
      flag=True
   return flag,bitcex,bitbitt,pursecex,pursebitt"""

def variance2(l):
   try: 
      ex=float(sum(l))/len(l)
   except ZeroDivisionError:
      return 0
   s=0;
   for i in l:
       s+=(i-ex)**2;
   return (float(s)/len(l))**0.5

def IsHighOutlier(point,all):
   avg=GetAvg(all)
   var=variance2(all)
   print avg,var,avg+2*var,point
   if(avg+2*var<point and avg!=0 and var!=0): #May12-*5
      return True
   return False
def GetMean(num,all):
    Avg=0
    try:
      Avg=all/num
    except ZeroDivisionError:
      #print "zero!!!!!!!!!!!!!!!!!!!!!!!!!!!!"
      Avg=0
    return Avg
def AddTransectionFee(cex,bittrex):
	earnall=[]
	loseall=[]
	for i in range(0,len(cex)):
		cex[i]['bid']=cex[i]['bid']-0.0025*cex[i]['bid']
		cex[i]['ask']=cex[i]['ask']+0.0025*cex[i]['ask']
	for i in range (0,len(bittrex)):
		bittrex[i]['bid']=bittrex[i]['bid']-0.0025*bittrex[i]['bid']
		bittrex[i]['ask']=bittrex[i]['ask']+0.0025*bittrex[i]['ask']
	return cex,bittrex
 
def GetProfitHistory(cex,bittrex):
	history=[]
	for c,b in zip(cex,bittrex):
		cp=c['bid'] - b['ask']
		bp=b['bid'] - c['ask']
		if(cp > 0 or bp > 0):
			history.append(max([cp,bp]))
	return history
			
def main():
  d = r.get('PriceToAlg')
  data = json.loads(d)
  insertfile="/Users/sunny/Desktop/ShibaProject/mysitenew/db.sqlite3"
  conn = sqlite3.connect(insertfile)
  cursor = conn.cursor()
	####get last 3 hours information
  sql='''Select Bid,Ask from trips_CexBTCTable where created_at > (SELECT datetime('now','+5 hours'))'''
  cursor.execute(sql)
  cex = [{'bid':item[0],'ask':item[1]} for item in cursor.fetchall()]
  sql='''Select Bid,Ask from trips_bittrexbtctable where created_at > (SELECT datetime('now','+5 hours'))'''
  cursor.execute(sql)
  bittrex = [{'bid':item[0],'ask':item[1]} for item in cursor.fetchall()]
  cex,bittrex=AddTransectionFee(cex,bittrex)
  profitHistory = GetProfitHistory(cex,bittrex)
  profitPositive = GetProfit(data)
  print profitPositive
  if(IsHighOutlier(profitPositive['Profit'],profitHistory)):
    requests.get('http://127.0.0.1:8000/bot/test/')
  headers = {'content-type': 'application/json'}
  a=requests.post('http://127.0.0.1:8000/bot/test/',data=data,headers=headers)
  #print "~~",a.text
main()
