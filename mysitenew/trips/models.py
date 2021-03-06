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
from users.models import User
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
		#return "%s" % self.datetime
		return "%s" % self.created_at#  , "%s" % self.created_at
class BittrexETHTable(models.Model):
	ask = models.FloatField(default=0)#CharField(max_length=100)
	bid = models.FloatField(default=0)#CharField(max_length=100)
	last = models.CharField(max_length=100)
	created_at = models.DateTimeField(auto_now=True)
	class Meta:
		ordering = ['created_at']
	def __str__(self):
		#return "%s" % self.datetime
		return "%s" % self.created_at#  , "%s" % self.created_at
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
		return "%s" % self.created_at#  , "%s" % self.created_at
		#return self.created_at
class CexETHTable(models.Model):
	ask = models.FloatField(default=0)#CharField(max_length=100)
	bid = models.FloatField(default=0)#CharField(max_length=100)
	last = models.CharField(max_length=100)
	created_at = models.DateTimeField(auto_now=True)
	class Meta:
		ordering = ['created_at']
	def __str__(self):
		return "%s" % self.created_at#  , "%s" % self.created_at
		#return self.created_at
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
class BinanceETHTable(models.Model):
	ask = models.FloatField(default=0)#CharField(max_length=100)
	bid = models.FloatField(default=0)#CharField(max_length=100)
	last = models.CharField(max_length=100)
	created_at = models.DateTimeField(auto_now=True)
	class Meta:
		ordering = ['created_at']
	def __str__(self):
		return self.created_at
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
class BitfinexETHTable(models.Model):
	ask = models.FloatField(default=0)#CharField(max_length=100)
	bid = models.FloatField(default=0)#CharField(max_length=100)
	last = models.CharField(max_length=100)
	created_at = models.DateTimeField(auto_now=True)
	class Meta:
		ordering = ['created_at']
	def __str__(self):
		return self.created_at
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
class CryptopiaETHTable(models.Model):
	ask = models.FloatField(default=0)#CharField(max_length=100)
	bid = models.FloatField(default=0)#CharField(max_length=100)
	last = models.CharField(max_length=100)
	created_at = models.DateTimeField(auto_now=True)
	class Meta:
		ordering = ['created_at']
	def __str__(self):
		return self.created_at
#Cryptopia----------------------------------Cryptopia------------------------------------Cryptopia----5


#Purse--------------------------------------
class Purse(models.Model):
    Bittrexmoney = models.FloatField(default=0.0)
    Binancemoney = models.FloatField(default=0.0)
    CexBTC = models.FloatField(default=0.0)
    BittrexBTC = models.FloatField(default=0.0)
    BinanceBTC = models.FloatField(default=0.0)
    Cexmoney = models.FloatField(default=0.0)
    userID = models.ForeignKey(User)
#purse--------------------------------------
#Apple
class Apple(models.Model):
	userID = models.ForeignKey(User)
	transectionA = models.CharField(max_length = 64)
	transectionB = models.CharField(max_length = 64)
	cointype = models.CharField(max_length = 64)
	def __str__(self):
		return self.userID
#BiBi
class BiBi(models.Model):
	userID = models.ForeignKey(User)
	transectionA = models.CharField(max_length = 64)
	transectionB = models.CharField(max_length = 64)
	cointypeA = models.CharField(max_length = 64)
	cointypeB = models.CharField(max_length = 64)
	def __str__(self):
		return self.userID
#choose for arbitrage
class AlgTypeByUser(models.Model):
	userID = models.IntegerField(max_length = 20)
	Head = models.CharField(max_length = 64)
	Foot = models.CharField(max_length = 64)
	created_at = models.DateTimeField(auto_now=True)

class AlgTypeByUserData(models.Model):
	userID = models.IntegerField(max_length = 20)
	Head = models.CharField(max_length = 64)
	Foot = models.CharField(max_length = 64)
	created_at = models.DateTimeField(auto_now=True)
#TransectionRecord--------------------------
class TransectionRecord(models.Model):
    userID = models.ForeignKey(User)
    Fee = models.FloatField(default=0.0)
    BidTransection = models.CharField(max_length=100)
    AskTransection = models.CharField(max_length=100)
    Bid = models.FloatField(default=0.0)
    Ask = models.FloatField(default=0.0)
    created_at = models.DateTimeField()
    flag = models.CharField(max_length=1,default='0')
#TransectionRecord--------------------------
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