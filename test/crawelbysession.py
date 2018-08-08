import requests
import time
from datetime import datetime
import sqlite3
#Bittrex
def CrawlBittrexBTCUSDT(session):
        quote_page = "https://bittrex.com/api/v1.1/public/getticker?market=USDT-BTC"
        response = session.get(quote_page)
        data = response.json()['result']
        # print session.params
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
        try:
                data = response.json()['Data']
        except:
                print data
        return data['BidPrice'],data['AskPrice'],data['LastPrice']
def CrawlCryptopiaETHUSD(session):
        quote_page = "https://www.cryptopia.co.nz/api/GetMarket/ETH_USDT"
        response = session.get(quote_page)
        try:
                data = response.json()['Data']
        except:
                print data
        return data['BidPrice'],data['AskPrice'],data['LastPrice']
def CrawlCryptopiaETHBTC(session):
        quote_page = "https://www.cryptopia.co.nz/api/GetMarket/ETH_BTC"
        response = session.get(quote_page)
        try:
                data = response.json()['Data']
        except:
                print data
        return data['BidPrice'],data['AskPrice'],data['LastPrice']



sessionBittrex = requests.Session()
sessionCex = requests.Session()
sessionBitfinex = requests.Session()
sessionCryptopia = requests.Session()


conn = sqlite3.connect("test.db")
cursor = conn.cursor()
while(1):
        localtime=datetime.now()#time.asctime(time.localtime(time.time()))
        nowtime=localtime.strftime('%Y-%m-%d %H:%M:%S')
        #bittrexcrawel
        BittrexBTCUSDTBid,BittrexBTCUSDTAsk,BittrexBTCUSDTLast = CrawlBittrexBTCUSDT(sessionBittrex)
        BittrexTUSDBTCBid,BittrexTUSDBTCAsk,BittrexTUSDBTCLast = CrawlBittrexTUSDBTC(sessionBittrex)
        BittrexETHBTCBid,BittrexETHBTCAsk,BittrexETHBTCLast = CrawlBittrexETHBTC(sessionBittrex)
        BittrexTUSDETHBid,BittrexTUSDETHAsk,BittrexTUSDETHLast = CrawlBittrexTUSDETH(sessionBittrex)
        BittrexETHUSDTBid,BittrexETHUSDTAsk,BittrexETHUSDTLast = CrawlBittrexETHUSDT(sessionBittrex)
        #cexcrawel
        CexBTCUSDBid,CexBTCUSDAsk,CexBTCUSDLast = CrawlCexBTCUSD(sessionCex)
        CexETHUSDBid,CexETHUSDAsk,CexETHUSDLast = CrawlCexETHUSD(sessionCex)
        CexETHBTCBid,CexETHBTCAsk,CexETHBTCLast = CrawlCexETHBTC(sessionCex)
        #bitfinexcrawel
        BitfinexBTCUSDBid,BitfinexBTCUSDAsk,BitfinexBTCUSDLast = CrawlBitfinexBTCUSD(sessionBitfinex)
        BitfinexETHUSDBid,BitfinexETHUSDAsk,BitfinexETHUSDLast = CrawlBitfinexETHUSD(sessionBitfinex)
        BitfinexETHBTCBid,BitfinexETHBTCAsk,BitfinexETHBTCLast = CrawlBitfinexETHBTC(sessionBitfinex)
        #cryptopiacrawel
        CryptopiaBTCUSDBid,CryptopiaBTCUSDAsk,CryptopiaBTCUSDLast = CrawlCryptopiaBTCUSD(sessionCryptopia)
        CryptopiaETHUSDBid,CryptopiaETHUSDAsk,CryptopiaETHUSDLast = CrawlCryptopiaETHUSD(sessionCryptopia)
        CryptopiaETHBTCBid,CryptopiaETHBTCAsk,CryptopiaETHBTCLast = CrawlCryptopiaETHBTC(sessionCryptopia)
        #SQLbittrex
        sql = '''INSERT INTO Bittrex_BTC_USDT (ask,bid,last,created_at) VALUES (?,?,?,?)'''
        cursor.execute(sql,(BittrexBTCUSDTAsk,BittrexBTCUSDTBid,BittrexBTCUSDTLast,nowtime))
        sql = '''INSERT INTO Bittrex_TUSD_BTC (ask,bid,last,created_at) VALUES (?,?,?,?)'''
        cursor.execute(sql,(BittrexTUSDBTCAsk,BittrexTUSDBTCBid,BittrexTUSDBTCLast,nowtime))
        sql = '''INSERT INTO Bittrex_ETH_BTC (ask,bid,last,created_at) VALUES (?,?,?,?)'''
        cursor.execute(sql,(BittrexETHBTCAsk,BittrexETHBTCBid,BittrexETHBTCLast,nowtime))
        sql = '''INSERT INTO Bittrex_TUSD_ETH (ask,bid,last,created_at) VALUES (?,?,?,?)'''
        cursor.execute(sql,(BittrexTUSDETHAsk,BittrexTUSDETHBid,BittrexTUSDETHLast,nowtime))
        sql = '''INSERT INTO Bittrex_ETH_USDT (ask,bid,last,created_at) VALUES (?,?,?,?)'''
        cursor.execute(sql,(BittrexETHUSDTAsk,BittrexETHUSDTBid,BittrexETHUSDTLast,nowtime))
        #SQLcex
        sql = '''INSERT INTO Cex_BTC_USD (ask,bid,last,created_at) VALUES (?,?,?,?)'''
        cursor.execute(sql,(CexBTCUSDAsk,CexBTCUSDBid,CexBTCUSDLast,nowtime))
        sql = '''INSERT INTO Cex_ETH_USD (ask,bid,last,created_at) VALUES (?,?,?,?)'''
        cursor.execute(sql,(CexETHUSDAsk,CexETHUSDBid,CexETHUSDLast,nowtime))
        sql = '''INSERT INTO Cex_ETH_BTC (ask,bid,last,created_at) VALUES (?,?,?,?)'''
        cursor.execute(sql,(CexETHBTCAsk,CexETHBTCBid,CexETHBTCLast,nowtime))
        #SQLbitfinex
        sql = '''INSERT INTO Bitfinex_BTC_USD (ask,bid,last,created_at) VALUES (?,?,?,?)'''
        cursor.execute(sql,(BitfinexBTCUSDAsk,BitfinexBTCUSDBid,BitfinexBTCUSDLast,nowtime))
        sql = '''INSERT INTO Bitfinex_ETH_USD (ask,bid,last,created_at) VALUES (?,?,?,?)'''
        cursor.execute(sql,(BitfinexETHUSDAsk,BitfinexETHUSDBid,BitfinexETHUSDLast,nowtime))
        sql = '''INSERT INTO Bitfinex_ETH_BTC (ask,bid,last,created_at) VALUES (?,?,?,?)'''
        cursor.execute(sql,(BitfinexETHBTCAsk,BitfinexETHBTCBid,BitfinexETHBTCLast,nowtime))
        #SQLcryptopia
        sql = '''INSERT INTO Cryptopia_BTC_USD (ask,bid,last,created_at) VALUES (?,?,?,?)'''
        cursor.execute(sql,(CryptopiaBTCUSDAsk,CryptopiaBTCUSDBid,CryptopiaBTCUSDLast,nowtime))
        sql = '''INSERT INTO Cryptopia_ETH_USD (ask,bid,last,created_at) VALUES (?,?,?,?)'''
        cursor.execute(sql,(CryptopiaETHUSDAsk,CryptopiaETHUSDBid,CryptopiaETHUSDLast,nowtime))
        sql = '''INSERT INTO Cryptopia_ETH_BTC (ask,bid,last,created_at) VALUES (?,?,?,?)'''
        cursor.execute(sql,(CryptopiaETHBTCAsk,CryptopiaETHBTCBid,CryptopiaETHBTCLast,nowtime))

        conn.commit()
        time.sleep(10)
        # i+=1

def Update(portname,objectname):
  r = redis.StrictRedis(host='localhost', port=6379, db=0)
  r.publish(portname, objectname)

"""
CREATE TABLE Bittrex_BTC_USDT(
   id integer primary key autoincrement,
   bid float,
   ask float,
   last float,
   created_at datetime Not Null
);
CREATE TABLE Bittrex_TUSD_BTC(
   id integer primary key autoincrement,
   bid float,
   ask float,
   last float,
   created_at datetime Not Null
);
CREATE TABLE Bittrex_ETH_BTC(
   id integer primary key autoincrement,
   bid float,
   ask float,
   last float,
   created_at datetime Not Null
);
CREATE TABLE Bittrex_TUSD_ETH(
   id integer primary key autoincrement,
   bid float,
   ask float,
   last float,
   created_at datetime Not Null
);
CREATE TABLE Bittrex_ETH_USDT(
   id integer primary key autoincrement,
   bid float,
   ask float,
   last float,
   created_at datetime Not Null
);

CREATE TABLE Cex_BTC_USD(
   id integer primary key autoincrement,
   bid float,
   ask float,
   last float,
   created_at datetime Not Null
);
CREATE TABLE Cex_ETH_USD(
   id integer primary key autoincrement,
   bid float,
   ask float,
   last float,
   created_at datetime Not Null
);
CREATE TABLE Cex_ETH_BTC(
   id integer primary key autoincrement,
   bid float,
   ask float,
   last float,
   created_at datetime Not Null
);

CREATE TABLE Bitfinex_BTC_USD(
   id integer primary key autoincrement,
   bid float,
   ask float,
   last float,
   created_at datetime Not Null
);
CREATE TABLE Bitfinex_ETH_USD(
   id integer primary key autoincrement,
   bid float,
   ask float,
   last float,
   created_at datetime Not Null
);
CREATE TABLE Bitfinex_ETH_BTC(
   id integer primary key autoincrement,
   bid float,
   ask float,
   last float,
   created_at datetime Not Null
);

CREATE TABLE Cryptopia_BTC_USD(
   id integer primary key autoincrement,
   bid float,
   ask float,
   last float,
   created_at datetime Not Null
);
CREATE TABLE Cryptopia_ETH_USD(
   id integer primary key autoincrement,
   bid float,
   ask float,
   last float,
   created_at datetime Not Null
);
CREATE TABLE Cryptopia_ETH_BTC(
   id integer primary key autoincrement,
   bid float,
   ask float,
   last float,
   created_at datetime Not Null
);


delete from BittrexBTC_USDT;
delete from BittrexETH_USD;
delete from BittrexTUSD_ETH;
delete from BittrexETH_BTC;
delete from CexBTC_USD;
delete from CexETH_BTC;
delete from CexETH_USD;
"""