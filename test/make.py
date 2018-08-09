import json
import numpy as np
with open("ison.json","r") as loadfile:
    loaddict = json.load(loadfile)
    print loaddict["BTCUSD"]["Bittrex"]["Bid"]
    coinList = ["BTCUSD","ETHBTC","ETHUSD"]
    exchangeList = ["Bittrex","Cex","Bitfinex","Cryptopia"]
    typelist = ["Bid","Ask"]
for(i)
