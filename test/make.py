# -*- coding: UTF-8 -*-
import json
import numpy as np
from scipy.spatial.distance import pdist, squareform
import matplotlib.pyplot as plt
import redis
import csv
import datetime
import requests
import urllib
with open("111.json","r") as loadfile:
    loaddict = json.load(loadfile)
r = redis.StrictRedis(host='localhost', port=6379, db=0)
#d = r.get('PriceToAlg')
#loaddict = json.loads(d)
# print loaddict["BTCUSD"]["Bittrex"]["Bid"]
coinList = ["BTC","ETH","USD","BCH","ZEC","BTG"]
vertices=24
exchangeList = ["Bittrex","Cex","Bitfinex","Cryptopia"] #cex 每一行的4 5 6 (345) 中的 5(4) 是 cexeth
typelist = ["Bid","Ask"]
exchangeNum = 4
coinTypeNum = 6
mstlist =[]
mstnp = []
exchangecointnp = []
exchangecointtype = ""
AllPath = []
time = datetime.datetime.now()
for i in exchangeList:
    for j in  coinList:
        coindict = {"exchange":i,"coin":j}
        mstlist.append(coindict)
def makecoinsort(a,b):
    if((a=="BTC" and b == "ETH") or (a=="USD" and b == "ETH") or (a=="USD" and b == "BTC")\
        or (a=="USD" and b == "BTG") or (a=="USD" and b == "ZEC") or (a=="USD" and b == "BCH")\
        or (a=="BTC" and b == "BCH") or (a=="BTC" and b == "ZEC") or (a=="BTC" and b == "BTG")\
        or (a=="ETH" and b == "BCH") or (a=="ETH" and b == "ZEC") or (a=="ETH" and b == "BTG")):
        return 1
    return 0
def Find(a):
    return exchangeList[a/coinTypeNum],coinList[a%coinTypeNum]
def FindCoinType(index,last):
    coinType = index % coinTypeNum
    exchange = index / coinTypeNum
    lastcoinType = last % coinTypeNum
    lastcexchange = last / coinTypeNum
    return coinList[lastcoinType],exchangeList[lastcexchange],coinList[coinType],exchangeList[exchange]
def minimum_spanning_tree(visited_vertices,X, copy_X=True):
    """X are edge weights of fully connected graph"""
    if X.shape[0] != X.shape[1]:
        raise ValueError("X needs to be square matrix")
    if copy_X:
        X = X.copy()
    n_vertices = X.shape[0] #n*n return n
    spanning_edges = []
    # initialize with node 0:                                                                                         
    profit=[100]                                                                                            
    num_visited = 1
    # exclude self connections:
    diag_indices = np.arange(n_vertices)

    while num_visited != n_vertices:
        new_edge = np.argmax(X[visited_vertices], axis = None)#已經走過的最大的路徑
        # 2d encoding of new_edge from flat, get correct indices
        new_edge = divmod(new_edge, n_vertices)
        a,b,c,d = FindCoinType(new_edge[1],visited_vertices[new_edge[0]])
        if(makecoinsort(a,c)):
            last = 1/loaddict[c+a][b]['Bid']
            nextone = 1/loaddict[c+a][d]['Ask']
        else:
            last = loaddict[a+c][b]['Ask']
            nextone = loaddict[a+c][d]['Bid']
        p = profit[new_edge[0]] * nextone
        profit.append(p)
        new_edge = [visited_vertices[new_edge[0]], new_edge[1]]#[0]商(列) [1]餘（行） 
        # add edge to tree
        spanning_edges.append(new_edge)
        visited_vertices.append(new_edge[1])
        #print visited_vertices
        # remove all edges inside current tree
        X[visited_vertices, new_edge[1]] = -(np.inf)
        X[new_edge[1], visited_vertices] = -(np.inf)
        num_visited += 1
    return np.vstack(spanning_edges),profit,visited_vertices
def GetPath(edge,exchange,profit):
    num = len(edge) - 1
    p = 0
    path = {'Profit':profit,'Path':[Find(exchange)]}
    for i in range(0,len(edge)):
        if(edge[num - i][1] == exchange):
            path['Path'].append(Find(edge[num - i][0]))
            exchange = edge[num - i][0]
    AllPath.append(path)
    return path['Path'][0][0],path['Path'][-1][0]
def SendMessage():
    print "send~~~"
mydict={}
for i in mstlist:
    mydict[i['exchange']] = {}
    for j in mstlist:
        exchangecointtype = j["exchange"]+j["coin"]+"->"+i["exchange"]+i["coin"]
        if(i["exchange"]==j["exchange"]):
            num = -(np.inf)
        elif(i["coin"]==j["coin"]):
            num = -(np.inf)
        else:
            mydict[i['exchange']][j['exchange']] = [0,time]
            if(makecoinsort(j["coin"],i["coin"]) == 1):
                coin = i["coin"]+j["coin"]
                if(coin in loaddict.keys()):
                    if(loaddict[coin][j["exchange"]] and loaddict[coin][i["exchange"]]):
                        num = (1/loaddict[coin][i["exchange"]]["Ask"]*1.0025) - (1/loaddict[coin][j["exchange"]]["Bid"]*0.9975)
                    else:
                        num = -(np.inf)
                else:
                    num = -(np.inf)
            elif(makecoinsort(j["coin"],i["coin"]) == 0):
                coin = j["coin"]+i["coin"]
                if(coin in loaddict.keys()):
                    if(loaddict[coin][j["exchange"]] and loaddict[coin][i["exchange"]]):
                        num = loaddict[coin][i["exchange"]]["Bid"]*0.9975 - loaddict[coin][j["exchange"]]["Ask"]*1.0025
                    else:
                        num = -(np.inf)
                else:
                    num = -(np.inf)
        exchangecointnp.append(exchangecointtype)
        mstnp.append(num)
mst = np.array(mstnp)
exchangecointarr = np.array(exchangecointnp)
exchangecointarr.shape = (vertices,vertices)
mst.shape = (vertices,vertices)
mstt = mst.T
start = [2,8,14,20]
with open('record.csv', 'r') as infile:
    reader = csv.reader(infile)
    for rows in reader:
        k = rows[0]
        v = rows[1]
        p = rows[2]
        t = datetime.datetime.strptime(rows[3],"%Y-%m-%d %H:%M:%S.%f")
        if k in mydict:
            mydict[k][v] = [p,t]
for s in start:
    edge_list = []
    profit = []
    visited_vertices = [s]
    edge_list,profit,visited_vertices = minimum_spanning_tree(visited_vertices,mstt)
    print "#"*100
    for i,j in zip(edge_list,profit):
        name = Find(visited_vertices[visited_vertices.index(i[1])])
        earn = profit[visited_vertices.index(i[1])]
        print i[0],"(",profit[visited_vertices.index(i[0])],Find(visited_vertices[visited_vertices.index(i[0])]),")",i[1],"(",profit[visited_vertices.index(i[1])],Find(visited_vertices[visited_vertices.index(i[1])]),")"
        if (name[1] == 'USD' and earn > profit[0]*1.05):#destination is USD
            start,destination = GetPath(edge_list,visited_vertices[visited_vertices.index(i[1])],earn)
            infor = mydict[start][destination]
            if(float(infor[0]) > earn or ((time - infor[1]).total_seconds() < 3600 and (time - infor[1]).total_seconds()!=0)):
                continue
            SendMessage()
            mydict[start][destination] = [earn,time]
with open('record.csv', 'w') as csvfile:
    writer = csv.writer(csvfile)
    for keys,values in mydict.iteritems():
        for key,value in values.iteritems():
            writer.writerow([keys,key,value[0],value[1]])
print AllPath
#encoded_dict = urllib.urlencode(AllPath)
#r = requests.post('http://127.0.0.1:8000/bot/call1/', headers={'Content-type': 'application/json','Connection':'close'},json = AllPath,timeout=5)
#r.close()

# array:
#      BTC         ->        ETH
# X元ETH買1元BTC(ETHBTC_BID)        1元BTC買X元ETH(ETHBTC_ASK)

#      ETH         ->        BTC
# X元BTC買1元ETH(ETHBTC_BID)        1元ETH買X元BTC(ETHBTC_ASK)

#      USD         ->        BTC
# X元BTC買1元USD(ETHBTC_BID)        1元USD買X元BTC(ETHBTC_ASK)