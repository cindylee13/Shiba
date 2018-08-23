import sqlite3
import time
import requests
import json
import redis
r = redis.StrictRedis(host='localhost', port=6379, db=0)
d = r.get('PriceToAlg')
data = json.loads(d)
print data