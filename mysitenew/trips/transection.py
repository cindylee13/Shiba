# -*- coding: utf-8 -*-
from django.db import models
from datetime import datetime, timedelta
from django.db.models import F, Sum, FloatField, Avg
import time
from .models import CexBTCTable,BittrexBTCTable,Purse,TransectionRecord
import time
import requests
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
   if(point>100 and avg+3*var<point and avg!=0 and var!=0): #May12-*5
      return True
   return False
def IsLowOutlier(point,all):
   avg=GetAvg(all)
   var=variance2(all)
   if(avg + 3*var < point and avg!=0 and var!=0): #May12-*5
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
def main(firstDate,lastDate):
	tempearn=0
	templose=-200
	a=[]
	####get first id by date 
	firstId=CexBTCTable.objects.filter(created_at__icontains = firstDate)[0].id
	####get last id by date 
	lastId=CexBTCTable.objects.filter(created_at__icontains = lastDate).order_by('-id')[0].id
	####get last 1000 information
	cexlast = CexBTCTable.objects.filter(id__range=(firstId-1000, firstId-1)).values('bid', 'ask')#.annotate(ask='ask').annotate(time='created_at')
	bittrexlast = BittrexBTCTable.objects.filter(id__range=(firstId-1000, firstId-1)).values('bid', 'ask')#.annotate(ask='ask').annotate(time='created_at')
	####get information by date
	cex = CexBTCTable.objects.filter(id__range=(firstId, lastId)).values('bid', 'ask','created_at')#.annotate(ask='ask').annotate(time='created_at')
	bittrex = BittrexBTCTable.objects.filter(id__range=(firstId, lastId)).values('bid', 'ask')[0::]#.annotate(ask='ask').annotate(time='created_at')
	#add transection fee
	cex,bittrex=AddTransectionFee(cex,bittrex)
	#last 1000 records amount of earn and lose 
	earnall,loseall=GetRecord(cexlast,bittrexlast)
	#get purse 
	#if earn
	i=0
	for b,c in zip(bittrex,cex):
		earn=c['bid']-b['ask']
		lose=b['bid']-c['ask']
		earnall.append(earn)
		loseall.append(lose)
		if(IsHighOutlier(earn,earnall) and tempearn + 5 < earn and earn > 0):
			if(DoWin(b,c,earnall,loseall,earn,c['created_at'])):
				tempearn=earn
				#InsertTransectionRecord(1,)
		if(not IsHighOutlier(earn,earnall)):
			tempearn=0
		#print GetEarn()
		profitAvg=GetEarn()
		#if(len(profitAvg)==0)
		#	Avg=ProfitAvg
		#print "~~~~~~",profitAvg
		#print profitAvg,lose
		#print 'threadhold=',profitAvg*0.9,'num=',lose,'date=',profitAvg*0.9>abs(lose),'all=',lose > templose + 5,'lose=',lose,templose
		if(IsLowOutlier(lose,loseall) and profitAvg*0.75>abs(lose) and lose > templose + 5):
			if(DoLose(b,c,profitAvg,c['created_at'])):
				print "do!"
				templose=lose
				a.append(lose)
				ChangeTransection(1,profitAvg)
			#print "do!"
		if(profitAvg*0.75<=abs(lose)):
			templose=-200
		#print GetEarn()['ProfitAvg']
		#print i,"#",earn,"~~~",'avg=',GetAvg(earnall),'var=',variance2(earnall),'all=',GetAvg(earnall)+2*variance2(earnall),'aaa=',IsHighOutlier(earn,earnall)
		if(len(earnall)>1000):
			del earnall[0]
		if(len(loseall)>1000):
			del loseall[0]
		i+=1
		#a.append(earn)
	return a, lastId
def InsertTransectionRecord(userId,fee,bidTransection,askTransection,bid,ask,flag,time1):
	#temp=datetime.now()
	now=time1.strftime('%Y-%m-%d %H:%M:%S')
	print time1,"~~~",now
	TransectionRecord.objects.create(userID_id = 1, Fee = fee, BidTransection= bidTransection,AskTransection=askTransection,Bid=bid,Ask=ask,created_at=now,flag=flag)
	"""try:
		result = TransectionRecord.objects.filter(userID_id = 1,(F('Bid')-F('Ask'))__gt=avg)#,created_at__lt=time_threshold)[0]
	except IndexError:
		"""
def test():
	return "abc"
def ChangeTransection(userId,avg):
	result = TransectionRecord.objects.filter(userID_id = 1,Bid__gte=avg+F('Ask'),flag=0)[0]#,created_at__lt=time_threshold)[0]
	result.flag=2
	result.save()
def GetEarn():
	records=TransectionRecord.objects.filter(userID=1,flag=0).aggregate(ProfitAvg=Avg('Bid')-Avg('Ask'))
	#except:
	#	return 0
	if(records['ProfitAvg']==None):
		return 0
	else:
		return records['ProfitAvg']
	#if (get):
	#	return 0
	"""for record in records:
		amount=record.Bid-record.Ask
		if(amount>0):
			earn.append(amount)"""
	#return records
def UpdatePurse(purse,amount):
	#kw = {field_name:purse}
	f=Purse.objects.get(userID=1)#.update(**kw=amount)#.format(purse)
	setattr(f, purse, amount)
	f.save()
def GetPurse():
	purse = Purse.objects.filter(userID=1)[0]#).values('CexMoney','Bittrexmoney','CexBTC','BittrexBTC')[0]
	cexPurse=purse.Cexmoney
	bittrexPurse=purse.Bittrexmoney
	CexBTC=purse.CexBTC
	BittrexBTC=purse.BittrexBTC#,bittrexPurse,cexBTCPurse,bittrexBTCPurse
	return {'Cexmoney':cexPurse,'Bittrexmoney':bittrexPurse,'CexBTC':CexBTC,'BittrexBTC':BittrexBTC}

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
def GetRecord(cex,bittrex):
	earnall=[]
	loseall=[]
	for c,b in zip(cex,bittrex):
		earnall.append(c['bid']-b['ask'])
		loseall.append(b['bid']-c['ask'])
	return earnall,loseall
#def GetFee():

def DoWin(bittrex,cex,earnall,loseall,profit,time):
	#cexPurse,bittrexPurse,cexBTCPurse,bittrexBTCPurse = User.objects.filter(userID=1).values('Cexmoney','Bittrexmoney','CexBTC','BittrexBTC')[0]
	purse=GetPurse()
	a,b=GetProfitLine(GetAvg(loseall),variance2(loseall))
	ratio=Found(a,b,profit)
	fee=ratio*purse['Bittrexmoney']*0.01#Earn(buyTransection,sellTransection,fee,bid,ask)
	do = Transection('Bittrex','Cex',fee,cex['bid'],bittrex['ask'])
	if(do):
		print "do!",fee,ratio,cex['bid'],bittrex['ask']
		InsertTransectionRecord(1,fee,'cex','bittrex',cex['bid'],bittrex['ask'],0,time)
		return True
	return False

def DoLose(bittrex,cex,earnAvg,time):
	purse=GetPurse()
	a,b=GetLoseLine(earnAvg)
	fee=Found(a,b,abs(cex['ask']-bittrex['bid']))*(purse['Cexmoney']-(purse['Cexmoney']+purse['Bittrexmoney'])/2)*0.01
	print "fee=",fee
	do=Transection('Cex','Bittrex',fee,bittrex['bid'],cex['ask'])
	#print "do=",do
	if(do):
		#print "do!",fee,ratio,cex['bid'],bittrex['ask']
		InsertTransectionRecord(1,fee,'bittrex','cex',bittrex['bid'],cex['ask'],1,time)
		return True
	return False