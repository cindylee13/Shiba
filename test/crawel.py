import requests
import time
from datetime import datetime
import sqlite3
import json
import redis
import os
import random
from threading import Thread
import threading
import Queue
import websocket
from websocket import create_connection
#Bittrex
# 155 156 243 244
exchange = ['Bittrex','Cex','Bitfinex','Cryptopia']
cointype = ['BTC','ETH','BTG','BCH','ZEC']
formatBitifinex=['channelId','Bid','Bid_SIZE','Ask','Ask_SIZE','DAILY_CHANGE','DAILY_CHANGE_PERC','LAST_PRICE','VOLUME','HIGH','LOW']
QueueResult = {}
url = {
        "BTCUSD":{ "Bittrex":"https://bittrex.com/api/v1.1/public/getticker?market=USDT-BTC",
                   "Bitfinex":"BTCUSD", 
                   "Cex":"https://cex.io/api/ticker/BTC/USD",
                   "Cryptopia":"https://www.cryptopia.co.nz/api/GetMarket/BTC_USDT"},
        "ETHBTC":{"Bittrex":"https://bittrex.com/api/v1.1/public/getticker?market=BTC-ETH",
                  "Bitfinex":"ETHBTC",
                  "Cex":"https://cex.io/api/ticker/ETH/BTC",
                  "Cryptopia":"https://www.cryptopia.co.nz/api/GetMarket/ETH_BTC"
                },
        "ETHUSD":{"Bittrex":"https://bittrex.com/api/v1.1/public/getticker?market=USDT-ETH",
                  "Bitfinex":"ETHUSD",
                  "Cex":"https://cex.io/api/ticker/ETH/USD",
                  "Cryptopia":"https://www.cryptopia.co.nz/api/GetMarket/ETH_USDT"
                },
        'BCHBTC':{
                    "Bittrex":"https://bittrex.com/api/v1.1/public/getticker?market=BTC-BCH", 
                    "Cex":"https://cex.io/api/ticker/BCH/BTC", 
                    "Bitfinex":"BCHBTC", 
                    "Cryptopia":"https://www.cryptopia.co.nz/api/GetMarket/BCH_BTC"
                },
        'BCHETH':{
                    "Bittrex":"https://bittrex.com/api/v1.1/public/getticker?market=ETH-BCH",
                    "Bitfinex":"BCHETH", 
                },
        'BCHUSD':{
                    "Bittrex":"https://bittrex.com/api/v1.1/public/getticker?market=USDT-BCH", 
                    "Cex":"https://cex.io/api/ticker/BCH/USD", 
                    "Bitfinex":"BCHUSD", 
                    "Cryptopia":"https://www.cryptopia.co.nz/api/GetMarket/BCH_USDT"
                },
        'ZECBTC':{
                    "Bittrex":"https://bittrex.com/api/v1.1/public/getticker?market=BTC-ZEC", 
                    "Cex":"https://cex.io/api/ticker/ZEC/BTC", 
                    "Bitfinex":"ZECBTC", 
                    "Cryptopia":"https://www.cryptopia.co.nz/api/GetMarket/ZEC_BTC"
                },
        'ZECETH':
                {
                    "Bittrex":"https://bittrex.com/api/v1.1/public/getticker?market=ETH-ZEC"
                },
        'ZECUSD':
                {
                    "Bittrex":"https://bittrex.com/api/v1.1/public/getticker?market=USDT-ZEC", 
                    "Cex":"https://cex.io/api/ticker/ZEC/USD", 
                    "Bitfinex":"ZECUSD", 
                    "Cryptopia":"https://www.cryptopia.co.nz/api/GetMarket/ZEC_USDT"
                },
        'BTGBTC':
                {
                    "Bittrex":"https://bittrex.com/api/v1.1/public/getticker?market=BTC-BTG", 
                    "Cex":"https://cex.io/api/ticker/BTG/BTC", 
                    "Bitfinex":"BTGBTC", 
                    "Cryptopia":"https://www.cryptopia.co.nz/api/GetMarket/BTG_BTC"
                },
        'BTGETH':
                {
                    "Bittrex":"https://bittrex.com/api/v1.1/public/getticker?market=ETH-BTG", 
                },
        'BTGUSD':
                {
                    "Bittrex":"https://bittrex.com/api/v1.1/public/getticker?market=USDT-BTG", 
                    "Cex":"https://cex.io/api/ticker/BTG/USD", 
                    "Bitfinex":"BTGUSD", 
                }
            }
def BitifinexConnect():
    for key in url:
        print key
        if("Bitfinex" in url[key]):
            QueueResult[key] = Queue.Queue()
            ws[key] = create_connection("wss://api2.bitfinex.com:3000/ws")
            ws[key].send(json.dumps({
                "event": "subscribe",
                "channel": "Ticker",
                "pair": key,
            }))
            result = ws[key].recv()
            result = ws[key].recv()
    return ws
infor = { 
        'BTCUSD':{"Bittrex":{}, "Cex":{}, "Bitfinex":{}, "Cryptopia":{}},
        'ETHBTC':{"Bittrex":{}, "Cex":{}, "Bitfinex":{}, "Cryptopia":{}},
        'ETHUSD':{"Bittrex":{}, "Cex":{}, "Bitfinex":{}, "Cryptopia":{}},
        'BCHBTC':{"Bittrex":{}, "Cex":{}, "Bitfinex":{}, "Cryptopia":{}},
        'BCHETH':{"Bittrex":{}, "Cex":{}, "Bitfinex":{}, "Cryptopia":{}},
        'BCHUSD':{"Bittrex":{}, "Cex":{}, "Bitfinex":{}, "Cryptopia":{}},
        'ZECBTC':{"Bittrex":{}, "Cex":{}, "Bitfinex":{}, "Cryptopia":{}},
        'ZECETH':{"Bittrex":{}, "Cex":{}, "Bitfinex":{}, "Cryptopia":{}},
        'ZECUSD':{"Bittrex":{}, "Cex":{}, "Bitfinex":{}, "Cryptopia":{}},
        'BTGBTC':{"Bittrex":{}, "Cex":{}, "Bitfinex":{}, "Cryptopia":{}},
        'BTGETH':{"Bittrex":{}, "Cex":{}, "Bitfinex":{}, "Cryptopia":{}},
        'BTGUSD':{"Bittrex":{}, "Cex":{}, "Bitfinex":{}, "Cryptopia":{}}
        }
sessionbittrex = requests.Session()
sessioncex = requests.Session()
sessioncryptopia = requests.Session()
def CrawlBittrex(url,cointype,nowtime):
    quote_page = url
    response = sessionbittrex.get(quote_page)
    data = response.json()['result']
    # print session.params
    if(cointype == 'BTCUSD'):
        Insert('bittrex','btc',data['Bid'],data['Ask'],data['Last'],nowtime)
    return {'transection':"Bittrex","Bid":float(data['Bid']),"Ask":float(data['Ask']),"Last":float(data['Last'])}
def CrawlCex(url,cointype,nowtime):
    quote_page = url
    response = sessioncex.get(quote_page)
    data = response.json()
    print data
    if(cointype == 'BTCUSD'):
        Insert('cex','btc',data['bid'],data['ask'],data['last'],nowtime)
    return {'transection':"Cex","Bid":float(data['bid']),"Ask":float(data['ask']),"Last":float(data['last'])}
def CrawlBitfinex(url,cointype,nowtime):
    global ws
    try:
        result = ws[url].recv()
    except websocket.WebSocketConnectionClosedException:
        ws = BitifinexConnect()
        result = ws[url].recv()
    result = json.loads(result)
    print "!!",result,result[1]
    if(result[1]=='hb'):
        a = QueueResult[url].get()
        QueueResult[url].put(a)
        if(cointype == 'BTCUSD'):
            Insert('cryptopia','btc',a['Bid'],a['Ask'],a['LAST_PRICE'],nowtime)
        return {'transection':"Bitfinex","Bid":float(a['Bid']),"Ask":float(a['Ask']),"Last":float(a['LAST_PRICE'])}
    zipbObj = zip(formatBitifinex, result)
    a = dict(zipbObj)
    if(not QueueResult[url].empty()):
        QueueResult[url].get()
    QueueResult[url].put(a)
    if(cointype == 'BTCUSD'):
        Insert('cryptopia','btc',a['Bid'],a['Ask'],a['LAST_PRICE'],nowtime)
    return {'transection':"Bitfinex","Bid":float(a['Bid']),"Ask":float(a['Ask']),"Last":float(a['LAST_PRICE'])}
def CrawlCryptopia(url,cointype,nowtime):
    quote_page = url
    response = requests.get(quote_page)
    data = response.json()['Data']
    if(cointype == 'BTCUSD'):
        Insert('cryptopia','btc',data['BidPrice'],data['AskPrice'],data['LastPrice'],nowtime)
    return {'transection':"Cryptopia","Bid":float(data['BidPrice']),"Ask":float(data['AskPrice']),"Last":float(data['LastPrice'])}

switch={"Bittrex":CrawlBittrex,"Bitfinex":CrawlBitfinex,"Cex":CrawlCex,"Cryptopia":CrawlCryptopia}

def all(url):
    t=threading.Timer(10,all,args=(url,))
    t.start()
    print "create!!!!!!"
    localtime=datetime.now()#time.asctime(time.localtime(time.time()))
    nowtime=localtime.strftime('%Y-%m-%d %H:%M:%S')
    for cointype, urls in url.iteritems():
        for exchange,url in urls.iteritems():
            #print exchange,cointype#,switch[exchange](url,cointype,nowtime),url
            infor[cointype][exchange] = switch[exchange](url,cointype,nowtime)
    #print infor
    r = redis.StrictRedis(host='localhost', port=6379, db=0)
    r.set('PriceToAlg',json.dumps(infor),ex=3)
    alg = threading.Thread(target = RunAlg)
    alg.start()
    #print infor
def RunAlg():
    SaveDirectory = os.getcwd()
    #alg1 = os.path.join(SaveDirectory,"transection","alg1.py")
    #alg2 = os.path.join(SaveDirectory,"transection","alg2.py")
    alg2 = os.path.join(SaveDirectory,"make.py")
    #os.system('python ' + alg1)
    os.system('python ' + alg2)
def Insert(exchange,cointype,bid,ask,last,created_at):
    conn = sqlite3.connect("db.sqlite3")
    cursor = conn.cursor()
    sql = '''INSERT INTO {} (ask,bid,last,created_at) VALUES (?,?,?,?)'''.format('trips_'+exchange+cointype+'table')
    cursor.execute(sql,(ask,bid,last,created_at))
    conn.commit()
def Update(transection,bid,ask,created_at):
    coin={'transection':transection,'bid':float(bid),'ask':float(ask) ,'created_at':created_at}
    infor = json.dumps(coin)
    SendToWeb('price',infor)
    return infor
def SendToWeb(portname,objectname):
    r = redis.StrictRedis(host='localhost', port=6379, db=0)
    r.publish(portname, objectname)
def main():
    global ws
    ws = BitifinexConnect()
    all(url)
#main()
ws={}
main()
#all(url)
"""
def Crawel():
        r = redis.StrictRedis(host='localhost', port=6379, db=0)
        r.set('PriceToAlg',json.dumps(infor),ex=3)"""
"""def UpdateOrCreate(transection,table,bid,ask,last):
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
  return result.bid"""
