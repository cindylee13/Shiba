import requests
import time
from datetime import datetime
import sqlite3
import json
import redis
from threading import Thread
import threading
#Bittrex
def CrawlBittrexBTCUSDT(session):
        quote_page = "https://bittrex.com/api/v1.1/public/getticker?market=USDT-BTC"
        response = session.get(quote_page)
        data = response.json()['result']
        print session.params
        return data['Bid'],data['Ask'],data['Last']
def CrawlBittrexTUSDBTC(session):
        quote_page = "https://bittrex.com/api/v1.1/public/getticker?market=BTC-TUSD"
        response = session.get(quote_page)
        data = response.json()['result']
        return data['Bid'],data['Ask'],data['Last']#data
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
def CrawlBittrexETHUSDT(session):
        quote_page = "https://bittrex.com/api/v1.1/public/getticker?market=USDT-ETH"
        response = session.get(quote_page)
        data = response.json()['result']
        return data['Bid'],data['Ask'],data['Last']#data
#CEX
def CrawlCexBTCUSD(session):
        quote_page = "https://cex.io/api/ticker/BTC/USD"
        response = session.get(quote_page)
        data = response.json()
        return data['bid'],data['ask'],data['last']
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
#bitfinex
def CrawlBitfinexBTCUSD(session):
        quote_page = "https://api.bitfinex.com/v1/pubticker/BTCUSD"
        response = session.get(quote_page)
        data = response.json()
        return data['bid'],data['ask'],data['last_price']
def CrawlBitfinexETHUSD(session):
        quote_page = "https://api.bitfinex.com/v1/pubticker/ETHUSD"
        response = session.get(quote_page)
        data = response.json()
        return data['bid'],data['ask'],data['last_price']#data
def CrawlBitfinexETHBTC(session):
        quote_page = "https://api.bitfinex.com/v1/pubticker/ETHBTC"
        response = session.get(quote_page)
        data = response.json()
        return data['bid'],data['ask'],data['last_price']#data
#cryptopia
def CrawlCryptopiaBTCUSD(session):
        quote_page = "https://www.cryptopia.co.nz/api/GetMarket/BTC_USDT"
        response = session.get(quote_page)
        data = response.json()['Data']
        return data['BidPrice'],data['AskPrice'],data['LastPrice']
def CrawlCryptopiaETHUSD(session):
        quote_page = "https://www.cryptopia.co.nz/api/GetMarket/ETH_USDT"
        response = session.get(quote_page)
        data = response.json()['Data']
        return data['BidPrice'],data['AskPrice'],data['LastPrice']
def CrawlCryptopiaETHBTC(session):
        quote_page = "https://www.cryptopia.co.nz/api/GetMarket/ETH_BTC"
        response = session.get(quote_page)
        data = response.json()['Data']
        return data['BidPrice'],data['AskPrice'],data['LastPrice']


def Update(transection,bid,ask,created_at):
        coin={'transection':transection,'bid':float(bid),'ask':float(ask) ,'created_at':created_at}
        infor = json.dumps(coin)
        SendToWeb('price',infor)
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
        coin={'transection':transection,'bid':float(bid),'ask':float(ask) ,'created_at':datetime.strftime(result.created_at,'%Y-%m-%d %H:%M:%S')}
        
        infor = json.dumps(coin)
        Update('price',infor)
  #return 'empty'
  result.bid = bid
  result.ask = ask 
  result.last= last
  print type(bid)
  result.save()
  coin={'transection':transection,'bid':float(bid),'ask':float(ask),'created_at':datetime.strftime(result.created_at,'%Y-%m-%d %H:%M:%S')}
  infor = json.dumps(coin)
  Update('price',infor)
  return result.bid
def RunAlg():
        SaveDirectory = os.getcwd()
        path = os.path.join(SaveDirectory,"transection","alg1.py")
        os.system('python ' + path)
def Crawel():
        print "crawel"
        t = threading.Timer(10,Crawel)
        t.start()
        infor={"cex":{},"bittrex":{},"bitfinex":{},"cryptopia":{}}
        sessionBittrex = requests.Session()
        sessionCex = requests.Session()
        sessionBitfinex = requests.Session()
        sessionCryptopia = requests.Session()
        conn = sqlite3.connect("db.sqlite3")
        cursor = conn.cursor()
        localtime=datetime.now()#time.asctime(time.localtime(time.time()))
        nowtime=localtime.strftime('%Y-%m-%d %H:%M:%S')
        #bittrex
        BittrexBTCUSDTBid,BittrexBTCUSDTAsk,BittrexBTCUSDTLast = CrawlBittrexBTCUSDT(sessionBittrex)
        infor['bittrex'] = json.loads(Update('Bittrex',BittrexBTCUSDTBid,BittrexBTCUSDTAsk,nowtime))
        BittrexTUSDBTCBid,BittrexTUSDBTCAsk,BittrexTUSDBTCLast = CrawlBittrexTUSDBTC(sessionBittrex)
        infor['bittrex'] = json.loads(Update('Bittrex',BittrexTUSDBTCBid,BittrexTUSDBTCAsk,nowtime))
        BittrexETHBTCBid,BittrexETHBTCAsk,BittrexETHBTCLast = CrawlBittrexETHBTC(sessionBittrex)
        infor['bittrex'] = json.loads(Update('Bittrex',BittrexETHBTCBid,BittrexETHBTCAsk,nowtime))
        BittrexTUSDETHBid,BittrexTUSDETHAsk,BittrexTUSDETHLast = CrawlBittrexTUSDETH(sessionBittrex)
        infor['bittrex'] = json.loads(Update('Bittrex',BittrexTUSDETHBid,BittrexTUSDETHAsk,nowtime))
        BittrexETHUSDTBid,BittrexETHUSDTAsk,BittrexETHUSDTLast = CrawlBittrexETHUSDT(sessionBittrex)
        infor['bittrex'] = json.loads(Update('Bittrex',BittrexETHUSDTBid,BittrexETHUSDTAsk,nowtime))
        #cex
        CexBTCUSDBid,CexBTCUSDAsk,CexBTCUSDLast = CrawlCexBTCUSD(sessionCex)
        infor['cex'] = json.loads(Update('Cex',CexBTCUSDBid,CexBTCUSDAsk,nowtime))
        CexETHUSDBid,CexETHUSDAsk,CexETHUSDLast = CrawlCexETHUSD(sessionCex)
        infor['cex'] = json.loads(Update('Cex',CexETHUSDBid,CexETHUSDAsk,nowtime))
        CexETHBTCBid,CexETHBTCAsk,CexETHBTCLast = CrawlCexETHBTC(sessionCex)
        infor['cex'] = json.loads(Update('Cex',CexETHBTCBid,CexETHBTCAsk,nowtime))
        #bitfinex
        BitfinexBTCUSDBid,BitfinexBTCUSDAsk,BitfinexBTCUSDLast = CrawlBitfinexBTCUSD(sessionBitfinex)
        infor['Bitfinex'] = json.loads(Update('Bitfinex',BitfinexBTCUSDBid,BitfinexBTCUSDAsk,nowtime))
        BitfinexETHUSDBid,BitfinexETHUSDAsk,BitfinexETHUSDLast = CrawlBitfinexETHUSD(sessionBitfinex)
        infor['Bitfinex'] = json.loads(Update('Bitfinex',BitfinexETHUSDBid,BitfinexETHUSDAsk,nowtime))
        BitfinexETHBTCBid,BitfinexETHBTCAsk,BitfinexETHBTCLast = CrawlBitfinexETHBTC(sessionBitfinex)
        infor['Bitfinex'] = json.loads(Update('Bitfinex',BitfinexETHBTCBid,BitfinexETHBTCAsk,nowtime))
        #cryptopia
        CryptopiaBTCUSDBid,CryptopiaBTCUSDAsk,CryptopiaBTCUSDLast = CrawlCryptopiaBTCUSD(sessionCryptopia)
        infor['Cryptopia'] = json.loads(Update('Cryptopia',CryptopiaBTCUSDBid,CryptopiaBTCUSDAsk,nowtime))
        CryptopiaETHUSDBid,CryptopiaETHUSDAsk,CryptopiaETHUSDLast = CrawlCryptopiaETHUSD(sessionCryptopia)
        infor['Cryptopia'] = json.loads(Update('Cryptopia',CryptopiaETHUSDBid,CryptopiaETHUSDAsk,nowtime))
        CryptopiaETHBTCBid,CryptopiaETHBTCAsk,CryptopiaETHBTCLast = CrawlCryptopiaETHBTC(sessionCryptopia)
        infor['Cryptopia'] = json.loads(Update('Cryptopia',CryptopiaETHBTCBid,CryptopiaETHBTCAsk,nowtime))

        #SQLbittrex
        sql = '''INSERT INTO Bittrex_btcusdt (ask,bid,last,created_at) VALUES (?,?,?,?)'''
        cursor.execute(sql,(BittrexBTCUSDTAsk,BittrexBTCUSDTBid,BittrexBTCUSDTLast,nowtime))
        sql = '''INSERT INTO Bittrex_tusdbtc (ask,bid,last,created_at) VALUES (?,?,?,?)'''
        cursor.execute(sql,(BittrexTUSDBTCAsk,BittrexTUSDBTCBid,BittrexTUSDBTCLast,nowtime))
        sql = '''INSERT INTO Bittrex_ethbtc (ask,bid,last,created_at) VALUES (?,?,?,?)'''
        cursor.execute(sql,(BittrexETHBTCAsk,BittrexETHBTCBid,BittrexETHBTCLast,nowtime))
        sql = '''INSERT INTO Bittrex_tusdeth (ask,bid,last,created_at) VALUES (?,?,?,?)'''
        cursor.execute(sql,(BittrexTUSDETHAsk,BittrexTUSDETHBid,BittrexTUSDETHLast,nowtime))
        sql = '''INSERT INTO Bittrex_ethusdt (ask,bid,last,created_at) VALUES (?,?,?,?)'''
        cursor.execute(sql,(BittrexETHUSDTAsk,BittrexETHUSDTBid,BittrexETHUSDTLast,nowtime))
        #SQLcex
        sql = '''INSERT INTO Cex_tusdeth (ask,bid,last,created_at) VALUES (?,?,?,?)'''
        cursor.execute(sql,(CexBTCUSDAsk,CexBTCUSDBid,CexBTCUSDLast,nowtime))
        sql = '''INSERT INTO Cex_ethusd (ask,bid,last,created_at) VALUES (?,?,?,?)'''
        cursor.execute(sql,(CexETHUSDAsk,CexETHUSDBid,CexETHUSDLast,nowtime))
        sql = '''INSERT INTO Cex_ethbtc (ask,bid,last,created_at) VALUES (?,?,?,?)'''
        cursor.execute(sql,(CexETHBTCAsk,CexETHBTCBid,CexETHBTCLast,nowtime))
        #SQLbitfinex
        sql = '''INSERT INTO Bitfinex_tusdeth (ask,bid,last,created_at) VALUES (?,?,?,?)'''
        cursor.execute(sql,(BitfinexBTCUSDAsk,BitfinexBTCUSDBid,BitfinexBTCUSDLast,nowtime))
        sql = '''INSERT INTO Bitfinex_ethusd (ask,bid,last,created_at) VALUES (?,?,?,?)'''
        cursor.execute(sql,(BitfinexETHUSDAsk,BitfinexETHUSDBid,BitfinexETHUSDLast,nowtime))
        sql = '''INSERT INTO Bitfinex_ethbtc (ask,bid,last,created_at) VALUES (?,?,?,?)'''
        cursor.execute(sql,(BitfinexETHBTCAsk,BitfinexETHBTCBid,BitfinexETHBTCLast,nowtime))
        #SQLcryptopia
        sql = '''INSERT INTO Cryptopia_tusdeth (ask,bid,last,created_at) VALUES (?,?,?,?)'''
        cursor.execute(sql,(CryptopiaBTCUSDAsk,CryptopiaBTCUSDBid,CryptopiaBTCUSDLast,nowtime))
        sql = '''INSERT INTO Cryptopia_ethusd (ask,bid,last,created_at) VALUES (?,?,?,?)'''
        cursor.execute(sql,(CryptopiaETHUSDAsk,CryptopiaETHUSDBid,CryptopiaETHUSDLast,nowtime))
        sql = '''INSERT INTO Cryptopia_ethbtc (ask,bid,last,created_at) VALUES (?,?,?,?)'''
        cursor.execute(sql,(CryptopiaETHBTCAsk,CryptopiaETHBTCBid,CryptopiaETHBTCLast,nowtime))

        conn.commit()
        with open("price.json","w") as f:
                json.dump(infor,f)
                print 'crawel',infor
        r = redis.StrictRedis(host='localhost', port=6379, db=0)
        r.set('PriceToAlg',json.dumps(infor),ex=3)
        alg = threading.Thread(target = RunAlg)
        alg.start()
        
def main():
        t=threading.Timer(10,Crawel)
        t.start()


sessionBittrex = requests.Session()
sessionCex = requests.Session()
sessionBitfinex = requests.Session()
sessionCryptopia = requests.Session()

conn = sqlite3.connect("db.sqlite3")
cursor = conn.cursor()
i=0
t=threading.Timer(10,Crawel)
t.start()
