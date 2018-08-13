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
coinnp = []
exchangenp = []
exchangetype = ""
cointype = ""
for i in exchangeList:
    for j in  coinList:
        coindict = {"exchange":i,"coin":j}
        mstlist.append(coindict)

def makecoinsort(a,b):
    if((a=="BTC" and b == "ETH") or (a=="USD" and b == "ETH") or (a=="USD" and b == "BTC")):
        return 0
    return 1

# print mstlist
for i in mstlist:
    for j in mstlist:
        cointype = j["coin"]+i["coin"]
        exchangetype = j["exchange"]+i["exchange"]
        if(i["exchange"]==j["exchange"]):
            num = np.inf
        
        elif(i["coin"]==j["coin"]):
            num = np.inf
        else:
            
            if(makecoinsort(j["coin"],i["coin"]) == 0):
                coin = i["coin"]+j["coin"]
                num = (1/loaddict[coin][j["exchange"]]["Ask"])-(1/loaddict[coin][i["exchange"]]["Bid"])
            elif(makecoinsort(j["coin"],i["coin"]) == 1):
                coin = j["coin"]+i["coin"]
                num = loaddict[coin][j["exchange"]]["Ask"]-loaddict[coin][i["exchange"]]["Bid"]
        coinnp.append(cointype)
        mstnp.append(num)
        exchangenp.append(exchangetype)
coinarr = np.array(coinnp)
mst = np.array(mstnp)
exchangearr = np.array(exchangenp)
exchangearr.shape = (12,12)
coinarr.shape = (12,12)
mst.shape = (12,12)
print exchangearr
print coinarr
print mst
print 0.056308-0.056401