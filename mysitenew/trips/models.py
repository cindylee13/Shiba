# -*- coding: utf-8 -*-
from urllib import urlopen
from bs4 import BeautifulSoup
from django.db import models
from django.utils import timezone
import pandas as pd
import json
import requests
import redis
import time
from datetime import datetime, timedelta
from django.db.models import F, Sum, FloatField, Avg
from django.core import serializers
#transection=[BittrexBTCTable,CexBTCTable,BinanceBTCTable,BitfinexBTCTable,CryptopiaBTCTable

#Bittrex-----------------------------------Bittrex----------------------------------------Bittrex-----1
class BittrexBTCTable(models.Model):
	ask = models.FloatField(default=0)#CharField(max_length=100)
	bid = models.FloatField(default=0)#CharField(max_length=100)
	last = models.CharField(max_length=100)
	created_at = models.DateTimeField(auto_now=True)
	class Meta:
		ordering = ['created_at']
	def __str__(self):
		return self.created_at

def CrawlBittrexBTC():
	quote_page = "https://bittrex.com/api/v1.1/public/getticker?market=USDT-BTC"
	response = requests.get(quote_page)
	data = response.json()
	result = data['result']
	return result

def BittrexBTC():
	from trips.models import BittrexBTCTable
	data = CrawlBittrexBTC()
	a=UpdateOrCreate('Bittrex',BittrexBTCTable,data['Bid'],data['Ask'],data['Last'])
	return a
#Bittrex-----------------------------------Bittrex----------------------------------------Bittrex-----1

#Cex----------------------------------------Cex-----------------------------------------Cex-----------2
class CexBTCTable(models.Model):
	ask = models.FloatField(default=0)#CharField(max_length=100)
	bid = models.FloatField(default=0)#CharField(max_length=100)
	last = models.CharField(max_length=100)
	created_at = models.DateTimeField(auto_now=True)
	class Meta:
		ordering = ['created_at']
	def __str__(self):
		return self.created_at

def CrawlCexBTC():
	quote_page = "https://cex.io/api/ticker/BTC/USD"
	response = requests.get(quote_page)
	data = response.json()
	return data

def CexBTC():
	from trips.models import CexBTCTable
	data = CrawlCexBTC()
	a=UpdateOrCreate('Cex',CexBTCTable,data['bid'],data['ask'],data['last'])
	return a
#Cex----------------------------------------Cex-----------------------------------------Cex-----------2

#Binance-----------------------------------Binance--------------------------------------Binance-------3
class BinanceBTCTable(models.Model):
	ask = models.FloatField(default=0)#CharField(max_length=100)
	bid = models.FloatField(default=0)#CharField(max_length=100)
	last = models.CharField(max_length=100)
	created_at = models.DateTimeField(auto_now=True)
	class Meta:
		ordering = ['created_at']
	def __str__(self):
		return self.created_at

def CrawlBinanceBTC():
	quote_page = "https://api.binance.com/api/v1/ticker/24hr?symbol=BTCUSDT"
	response = requests.get(quote_page)
	data = response.json()
	return data

def BinanceBTC():
	from trips.models import BinanceBTCTable
	data = CrawlBinanceBTC()
	a=UpdateOrCreate('Binance',BinanceBTCTable,data['bidPrice'],data['askPrice'],data['lastPrice'])
	return a
#Binance-----------------------------------Binance--------------------------------------Binance-------3

#Bitfinex----------------------------------Bitfinex-------------------------------------Bitfinex------4
class BitfinexBTCTable(models.Model):
	ask = models.FloatField(default=0)#CharField(max_length=100)
	bid = models.FloatField(default=0)#CharField(max_length=100)
	last = models.CharField(max_length=100)
	created_at = models.DateTimeField(auto_now=True)
	class Meta:
		ordering = ['created_at']
	def __str__(self):
		return self.created_at

def CrawlBitfinexBTC():
	quote_page = "https://api.bitfinex.com/v1/pubticker/BTCUSD"
	response = requests.get(quote_page)
	data = response.json()
	return data

def BitfinexBTC():
	from trips.models import BitfinexBTCTable
	data = CrawlBitfinexBTC()
	a=UpdateOrCreate('Bitfinex',BitfinexBTCTable,data['bid'],data['ask'],data['last_price'])
	return a
#Bitfinex----------------------------------Bitfinex-------------------------------------Bitfinex------4

#Cryptopia----------------------------------Cryptopia------------------------------------Cryptopia----5
class CryptopiaBTCTable(models.Model):
	ask = models.FloatField(default=0)#CharField(max_length=100)
	bid = models.FloatField(default=0)#CharField(max_length=100)
	last = models.CharField(max_length=100)
	created_at = models.DateTimeField(auto_now=True)
	class Meta:
		ordering = ['created_at']
	def __str__(self):
		return self.created_at

def CrawlCryptopiaBTC():
	quote_page = "https://www.cryptopia.co.nz/api/GetMarket/BTC_USDT"
	response = requests.get(quote_page)
	data = response.json()
	result = data['Data']
	return result

def CryptopiaBTC():
	from trips.models import CryptopiaBTCTable
	data = CrawlCryptopiaBTC()
	a=UpdateOrCreate('Cryptopia',CryptopiaBTCTable,data['BidPrice'],data['AskPrice'],data['LastPrice'])
	return a
#Cryptopia----------------------------------Cryptopia------------------------------------Cryptopia----5
#if auto_now time>5minute update ,if not create.--------------------------------------
def UpdateOrCreate(transection,table,bid,ask,last):
	time_threshold = datetime.now() - timedelta(hours=3)
	try:
		result = table.objects.filter(created_at__lt=time_threshold)[0]
	except IndexError:
		table.objects.create(bid = bid, ask = ask, last= last)
		#coin = serializers.serialize('json', table.objects.all())
		coin={'transection':transection,'bid':bid,'ask':ask,'last':last,'created_at':time.time()}
		#a = json.dumps(coin)
		Update('price',coin)
		return 'empty'
	result.bid = bid
	result.ask = ask 
	result.last= last
	result.save()
	#coin = serializers.serialize('json', table.objects.all())
	temp=datetime.now()
	now=temp.strftime('%Y-%m-%d %H:%M:%S')
	coin={'transection':transection,'bid':bid,'ask':ask,'created_at':now}
	infor = json.dumps(coin)
	#a = json.dumps(coin)
	#print a
	Update('price',infor)
	return result.bid
#difference load in sqilte--------------------------
class Difference(models.Model):
	BidTransection = models.CharField(max_length=20)#CharField(max_length=100)
	AskTransection = models.CharField(max_length=20)#CharField(max_length=100)
	Bid = models.FloatField(default=0)#CharField(max_length=100)
	Ask = models.FloatField(default=0)#CharField(max_length=100)
	created_at = models.DateTimeField(auto_now=True)
	def __str__(self):
		return '%s %s %s %s' % ((self.Bid-self.Ask)/self.Ask,self.BidTransection, self.AskTransection , self.created_at)
#Get the bid and ask difference----------------------------------------------------------
def GetBidAsk():   #bid-ask
	bid={}
	ask={}
	bid['CryptopiaBid']=CryptopiaBTCTable.objects.all().aggregate(Avg('bid'))

	bid['CexBid']=CexBTCTable.objects.all().aggregate(Avg('bid'))

	bid['BittrexBid']=BittrexBTCTable.objects.all().aggregate(Avg('bid'))

	bid['BitfinexBid']=BitfinexBTCTable.objects.all().aggregate(Avg('bid'))

	bid['BinanceBid']=BinanceBTCTable.objects.all().aggregate(Avg('bid'))

	ask['CryptopiaAsk']=CryptopiaBTCTable.objects.all().aggregate(Avg('ask'))

	ask['CexAsk']=CexBTCTable.objects.all().aggregate(Avg('ask'))

	ask['BittrexAsk']=BittrexBTCTable.objects.all().aggregate(Avg('ask'))

	ask['BitfinexAsk']=BitfinexBTCTable.objects.all().aggregate(Avg('ask'))

	ask['BinanceAsk']=BinanceBTCTable.objects.all().aggregate(Avg('ask'))
	return bid,ask
def GetDifference():
	bids,asks=GetBidAsk()
	difference={}
	tran={}
	index=[]
	transections=['Bittrex','Cex','Binance','Bitfinex','Cryptopia']
	for i in range(0,len(transections)):
		bid=bids[transections[i]+'Bid']['bid__avg']
		for j in range(0,len(transections)):
			if(i==j):
				continue
			ask= asks[transections[j]+'Ask']['ask__avg']
			difference.update({transections[j]:float(bid-ask)})
		tran.update({transections[i]:difference})
		difference={}
		index.append(transections[i])
		print tran
	return tran
def GetPrice(table1,table2):
	set1=table1.objects.order_by('-id')[0]
	set2=table2.objects.order_by('-id')[0]
	return set1.bid,set2.ask

def CheckSave():
	from trips.models import BittrexBTCTable
	from trips.models import CexBTCTable
	from trips.models import BinanceBTCTable
	from trips.models import BitfinexBTCTable
	from trips.models import CryptopiaBTCTable
	bids={}
	asks={}
	transections=[BittrexBTCTable,CexBTCTable,BinanceBTCTable,CryptopiaBTCTable]
	transectionName=['BittrexBTCTable','CexBTCTable','BinanceBTCTable','CryptopiaBTCTable']
	for i in range (0,len(transections)):
		bids[transectionName[i]],asks[transectionName[i]]=GetPrice(transections[i],transections[i])
	for i in range(0,len(transections)):
		for j in range(0,len(transections)):
			if(i==j):
				continue
			bid,ask=bids[transectionName[i]],asks[transectionName[j]]
			percent=float((bid-ask)/ask)*100
			if(percent>0.5):
				Difference.objects.create(BidTransection = transectionName[i], AskTransection = transectionName[j] , Bid=bid , Ask=ask)
				print str(transectionName[i]),str(transectionName[j]),bid,ask,percent

	#	Difference.objects.create(BidTransection = bidTransection, AskTransection = askTransection , bid=bid , ask=ask)
#realtime web-------------------------------------------------------------
def Update(portname,objectname):
	r = redis.StrictRedis(host='localhost', port=6379, db=0)
	r.publish(portname, objectname)
'''
def crawal():
	#url = 'https://bittrex.com/api/v1.1/public/getticker?market=USDT-BTC'
	#response = requests.get(url)
	#data = response.json()
	#dict  = {'Bid' : data['result']['Bid'], 'Ask' : data['result']['Ask'], 'Last' : data['result']['Last']} 
	#df = pd.DataFrame(dict, index = range(1))
	#return df
	
	datalist = []  #陣列用法
	datalist.append('Bid :' + str(data['result']['Bid']))   
	datalist.append('Ask :' + str(data['result']['Ask']))
	datalist.append('Last :' + str(data['result']['Last']))
	df = pd.DataFrame(datalist)
	return df
'''