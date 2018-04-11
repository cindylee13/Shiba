import os
from models import BittrexBTC,CryptopiaBTC,BinanceBTC,BitfinexBTC,CexBTC
import time
def RunForSecond():
	print "12312312313"
	for i in range(0,6):
		BittrexBTC()
		CryptopiaBTC()
		BitfinexBTC()
		BinanceBTC()
		CexBTC()
		time.sleep(10)