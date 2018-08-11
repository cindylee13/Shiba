import requests
import time
from datetime import datetime
import sqlite3
import json
import redis
import os
from threading import Thread
import threading
def CrawlBittrexBTCUSDT(session):
        quote_page = "https://bittrex.com/api/v1.1/public/getticker?market=USDT-BTC"
        response = session.get(quote_page)
        data = response.json()['result']
        print session.params
        return data['Bid'],data['Ask'],data['Last']
def CrawlCexBTCUSD(session):
        quote_page = "https://cex.io/api/ticker/BTC/USD"
        response = session.get(quote_page)
        data = response.json()
        return data['bid'],data['ask'],data['last']
def CrawlBittrexETHBTC(session):
        quote_page = "https://bittrex.com/api/v1.1/public/getticker?market=BTC-ETH"
        response = session.get(quote_page)
        data = response.json()['result']
        return data['Bid'],data['Ask'],data['Last']#data
def CrawlBittrexTUSDETH(session):
        quote_page = "https://bittrex.com/api/v1.1/public/getticker?market=ETH-TUSD"
        response = session.get(quote_page)
        data = response.json()['result']
        return data['Bid'],data['Ask'],data['Last']#data
def CrawlBittrexETHUSD(session):
        quote_page = "https://bittrex.com/api/v1.1/public/getticker?market=USDT-ETH"
        response = session.get(quote_page)
        data = response.json()['result']
        return data['Bid'],data['Ask'],data['Last']#data
def CrawlCexETHUSD(session):
        quote_page = "https://cex.io/api/ticker/ETH/USD"
        response = session.get(quote_page)
        data = response.json()
        return data['bid'],data['ask'],data['last']#data
def CrawlCexETHBTC(session):
        quote_page = "https://cex.io/api/ticker/ETH/BTC"
        response = session.get(quote_page)
        data = response.json()
        return data['bid'],data['ask'],data['last']#data
def Update(transection,bid,ask,created_at):
        coin={'transection':transection,'bid':float(bid),'ask':float(ask) ,'created_at':created_at}
        infor = json.dumps(coin)
        SendToWeb('price',infor)
        return infor
def changejson(transection,bid,ask,created_at):
    coin={'transection':transection,'bid':float(bid),'ask':float(ask) ,'created_at':created_at}
    infor = json.dumps(coin)
    return infor
def SendToWeb(portname,objectname):
        r = redis.StrictRedis(host='localhost', port=6379, db=0)
        r.publish(portname, objectname)
def UpdateOrCreate(transection,table,bid,ask,last):
  time_threshold = datetime.now() - timedelta(hours=3)
  try:
    result = table.objects.filter(created_at__lt=time_threshold)[0]
  except IndexError:
        result = table.objects.create(bid = bid, ask = ask, last= last)
        coin={'transection':transection,'bid':int(bid),'ask':int(ask) ,'created_at':datetime.strftime(result.created_at,'%Y-%m-%d %H:%M:%S')}
        infor = json.dumps(coin)
        Update('price',infor)
  #return 'empty'
  result.bid = bid
  result.ask = ask 
  result.last= last
  result.save()
  coin={'transection':transection,'bid':int(bid),'ask':int(ask),'created_at':datetime.strftime(result.created_at,'%Y-%m-%d %H:%M:%S')}
  infor = json.dumps(coin)
  Update('price',infor)
  return result.bid
def RunAlg():
        SaveDirectory = os.getcwd()
        alg1 = os.path.join(SaveDirectory,"transection","alg1.py")
        alg2 = os.path.join(SaveDirectory,"transection","alg2.py")
        os.system('python ' + alg1)
        #os.system('python ' + alg2)
def Crawel():
        print "crawel"
#2
        t = threading.Timer(10,Crawel)
        t.start()

        infor={"BTCUSD":{'Bittrex':{},'Cex':{}},"ETHBTC":{'Bittrex':{},'Cex':{}},"ETHUSD":{'Bittrex':{},'Cex':{}}}
        session = requests.Session()
        sessionCex = requests.Session()
        conn = sqlite3.connect("db.sqlite3")
        cursor = conn.cursor()
        localtime=datetime.now()#time.asctime(time.localtime(time.time()))
        nowtime=localtime.strftime('%Y-%m-%d %H:%M:%S')
        
        BittrexBTCUSDTBid,BittrexBTCUSDTAsk,BittrexBTCUSDTLast = CrawlBittrexBTCUSDT(session)
        CexBTCUSDBid,CexBTCUSDAsk,CexBTCUSDLast = CrawlCexBTCUSD(sessionCex)
        
        BittrexETHBTCBid,BittrexETHBTCAsk,BittrexETHBTCLast = CrawlBittrexETHBTC(session)
        BittrexETHUSDBid,BittrexETHUSDAsk,BittrexETHUSDLast = CrawlBittrexETHUSD(session)
        
        CexETHBTCBid,CexETHBTCAsk,CexETHBTCLast = CrawlCexETHBTC(sessionCex)
        CexETHUSDBid,CexETHUSDAsk,CexETHUSDLast = CrawlCexETHUSD(sessionCex)
        
        BTCUSD={'bittrex':{},'cex':{}}
        ETHBTC={'bittrex':{},'cex':{}}
        ETHUSD={'bittrex':{},'cex':{}}

        BTCUSD['bittrex'] = json.loads(Update('Bittrex',BittrexBTCUSDTBid,BittrexBTCUSDTAsk,nowtime))
        ETHBTC['bittrex'] = json.loads(changejson('Bittrex',BittrexETHBTCBid,BittrexETHBTCAsk,nowtime))
        ETHUSD['bittrex'] = json.loads(changejson('Bittrex',BittrexETHUSDBid,BittrexETHUSDAsk,nowtime))
        
        BTCUSD['cex'] = json.loads(Update('Cex',CexBTCUSDBid,CexBTCUSDAsk,nowtime))
        ETHBTC['cex'] = json.loads(changejson('Cex',CexETHBTCBid,CexETHBTCAsk,nowtime))
        ETHUSD['cex'] = json.loads(changejson('Cex',CexETHUSDBid,CexETHUSDAsk,nowtime))

        infor['BTCUSD']['Bittrex'] = BTCUSD['bittrex']
        infor['ETHBTC']['Bittrex'] = ETHBTC['bittrex']
        infor['ETHUSD']['Bittrex'] = ETHUSD['bittrex']

        infor['BTCUSD']['Cex'] = BTCUSD['cex']
        infor['ETHBTC']['Cex'] = ETHBTC['cex']
        infor['ETHUSD']['Cex'] = ETHUSD['cex']
        #print "***",infor


        sql = '''INSERT INTO trips_cexbtctable (ask,bid,last,created_at) VALUES (?,?,?,?)'''
        cursor.execute(sql,(CexBTCUSDAsk,CexBTCUSDBid,CexBTCUSDLast,nowtime))
        sql = '''INSERT INTO trips_bittrexbtctable (ask,bid,last,created_at) VALUES (?,?,?,?)'''
        cursor.execute(sql,(BittrexBTCUSDTAsk,BittrexBTCUSDTBid,BittrexBTCUSDTLast,nowtime))
        conn.commit()
        
        r = redis.StrictRedis(host='localhost', port=6379, db=0)
        r.set('PriceToAlg',json.dumps(infor),ex=3)
        
#1
        alg = threading.Thread(target = RunAlg)
        alg.start()
        
def main():
        t=threading.Timer(10,Crawel)
        t.start()


t=threading.Timer(10,Crawel)
t.start()