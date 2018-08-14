# -*- coding: UTF-8 -*-
import json
import numpy as np
from scipy.spatial.distance import pdist, squareform
import matplotlib.pyplot as plt
with open("Json.json","r") as loadfile:
    loaddict = json.load(loadfile)

# print loaddict["BTCUSD"]["Bittrex"]["Bid"]
coinList = ["BTC","ETH","USD"]
exchangeList = ["Bittrex","Cex","Bitfinex","Cryptopia"] #cex 每一行的4 5 6 (345) 中的 5(4) 是 cexeth
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
def minimum_spanning_tree(X, copy_X=True):
    """X are edge weights of fully connected graph"""
    #if copy_X:
    #    X = X.copy()
    if X.shape[0] != X.shape[1]:
        raise ValueError("X needs to be square matrix of edge weights")
    n_vertices = X.shape[0] #n*n return n
    spanning_edges = []
    # initialize with node 0:                                                                                         
    visited_vertices = [2]                                                                                            
    num_visited = 1
    # exclude self connections:
    diag_indices = np.arange(n_vertices)
    #X[diag_indices, diag_indices] = -(np.inf)#x[0,0] x[1,1] ....x[9,9]

    while num_visited != n_vertices:
        new_edge = np.argmax(X[visited_vertices], axis = None)#已經走過的最大的路徑
        if(X[new_edge] == (-np.inf)):
            num_visited+=1
            continue
        # 2d encoding of new_edge from flat, get correct indices
        new_edge = divmod(new_edge, n_vertices)
        print new_edge
        new_edge = [visited_vertices[new_edge[0]], new_edge[1]]#[0]商(列) [1]餘（行）                                                  
        # add edge to tree
        spanning_edges.append(new_edge)
        visited_vertices.append(new_edge[1])
        print visited_vertices
        # remove all edges inside current tree
        X[visited_vertices, new_edge[1]] = -(np.inf)
        X[new_edge[1], visited_vertices] = -(np.inf)                                                                     
        num_visited += 1
    print spanning_edges
    return np.vstack(spanning_edges)
# print mstlist
for i in mstlist:
    for j in mstlist:
        exchangecointtype = j["exchange"]+j["coin"]+"->"+i["exchange"]+i["coin"]
        if(i["exchange"]==j["exchange"]):
            num = -(np.inf)
        
        elif(i["coin"]==j["coin"]):
            num = -(np.inf)   
        else:
            if(makecoinsort(j["coin"],i["coin"]) == 0):
                coin = i["coin"]+j["coin"]
                num = (1/loaddict[coin][i["exchange"]]["Ask"])-(1/loaddict[coin][j["exchange"]]["Bid"])
                if(num<0):
                    num = -(np.inf)
            elif(makecoinsort(j["coin"],i["coin"]) == 1):
                coin = j["coin"]+i["coin"]
                num = loaddict[coin][i["exchange"]]["Ask"]-loaddict[coin][j["exchange"]]["Bid"]
                if(num<0):
                    num= -(np.inf)

        exchangecointnp.append(exchangecointtype)
        mstnp.append(num)

mst = np.array(mstnp)
exchangecointarr = np.array(exchangecointnp)
exchangecointarr.shape = (12,12)
mst.shape = (12,12)
mstt=mst.T
print exchangecointarr.T
print mstt
edge_list = minimum_spanning_tree(mstt)
""" 
for edge in edge_list:
    i, j = edge
    plt.plot([P[i, 0], P[j, 0]], [P[i, 1], P[j, 1]], c='r')"""
#plt.show()

# array:
#      BTC         ->        ETH
# X元ETH買1元BTC(ETHBTC_BID)        1元BTC買X元ETH(ETHBTC_ASK)

#      ETH         ->        BTC
# X元BTC買1元ETH(ETHBTC_BID)        1元ETH買X元BTC(ETHBTC_ASK)