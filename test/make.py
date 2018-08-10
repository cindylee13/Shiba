import json
import numpy as np
with open("Json.json","r") as loadfile:
    loaddict = json.load(loadfile)

# print loaddict["BTCUSD"]["Bittrex"]["Bid"]
coinList = ["BTC","ETH","USD"]
exchangeList = ["Bittrex","Cex","Bitfinex","Cryptopia"]
typelist = ["Bid","Ask"]

mstlist =[]
mstnp = []
for i in exchangeList:
    for j in  coinList:
        coindict = {"exchange":i,"coin":j}
        mstlist.append(coindict)

def makecoinsort(a,b):
    if(a == "ETH"):
        return a+b
    elif(b == "ETH"):
        return b+a
    elif(a == "BTC"):
        return a+b
    elif(b == "BTC"):
        return b+a

# print mstlist
for i in mstlist:
    for j in mstlist:
        if(i["exchange"]==j["exchange"]):
            num = np.inf
        
        elif(i["coin"]==j["coin"]):
            num = np.inf
        else:
            coin = makecoinsort(i["coin"],j["coin"])
            num = loaddict[coin][j["exchange"]]["Ask"]-loaddict[coin][i["exchange"]]["Bid"]
        mstnp.append(num)
mst = np.array(mstnp)
mst.shape = (12,12)
print mst