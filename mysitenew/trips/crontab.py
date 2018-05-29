import os
from models import BittrexBTC,CryptopiaBTC,BinanceBTC,BitfinexBTC,CexBTC,GetDifference
import time
def RunForSecond():
	for i in range(0,6):
		BittrexBTC()
		CryptopiaBTC()
		#BitfinexBTC()
		BinanceBTC()
		CexBTC()
		#GetDifference()
		time.sleep(10)