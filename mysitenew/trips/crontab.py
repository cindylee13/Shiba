import os
from models import BittrexBTC,CryptopiaBTC,BinanceBTC,BitfinexBTC,CexBTC
import time
def RunForSecond():
	for i in range(0,6):
		print "runrunrun!"
		BittrexBTC()
		CryptopiaBTC()
		BitfinexBTC()
		BinanceBTC()
		CexBTC()
		time.sleep(10)