from __future__ import absolute_import, unicode_literals
from celery import shared_task
import os
from .models import BittrexBTC,CexBTC,BinanceBTC,BitfinexBTC,CryptopiaBTC,CheckSave
import time
@shared_task
def hello_world():
    with open("output.txt", "a") as f:
        f.write("hello world")
        f.write("\n")
@shared_task
def BittrexForSecond():
		BittrexBTC()
		CexBTC()
		BinanceBTC()
		#BitfinexBTC()
		CryptopiaBTC()
		CheckSave()