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
exchangecointnp = []
exchangecointtype = ""
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
        exchangecointtype = j["exchange"]+j["coin"]+"->"+i["exchange"]+i["coin"]
        if(i["exchange"]==j["exchange"]):
            num = np.inf
        
        elif(i["coin"]==j["coin"]):
            num = np.inf    
        else:
            
            if(makecoinsort(j["coin"],i["coin"]) == 0):
                coin = i["coin"]+j["coin"]
                num = (1/loaddict[coin][i["exchange"]]["Ask"])-(1/loaddict[coin][j["exchange"]]["Bid"])
            elif(makecoinsort(j["coin"],i["coin"]) == 1):
                coin = j["coin"]+i["coin"]
                num = loaddict[coin][i["exchange"]]["Ask"]-loaddict[coin][j["exchange"]]["Bid"]
        exchangecointnp.append(exchangecointtype)
        mstnp.append(num)
mst = np.array(mstnp)
exchangecointarr = np.array(exchangecointnp)
exchangecointarr.shape = (12,12)
mst.shape = (12,12)
print exchangecointarr
print mst

# array:
#      BTC         ->        ETH
# X元ETH買1元BTC(ETHBTC_BID)        1元BTC買X元ETH(ETHBTC_ASK)

#      ETH         ->        BTC
# X元BTC買1元ETH(ETHBTC_BID)        1元ETH買X元BTC(ETHBTC_ASK)