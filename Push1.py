# -*- coding: utf-8 -*-
"""
Created on Fri Nov 22 16:53:28 2019
"""

#Ultra-Simple push protocol on Gnp graph for information spreading
#Please don't play with unconnected graph
import matplotlib.pyplot as plt
from random import randrange
import networkx as nx
import random
import math

#nodes
N= 20
#edge probability
P = 0.2




#Return random neighboor of node v in graph G
def random_nb(G,v):
    nb = nx.all_neighbors(G,v)
    try:
        return random.choice(list(nb))
    except:
        raise Exception("Sorry, the graph is not connected")    #stops the program


#Return dictionary that represent initial knowledge value of the node in the Graph
def createAttrDict(s,n):
    d ={}
    informed_index=randrange(n)

    #random initiator
    for i in range(0,n):
        d[i]='uninformed'
        if (informed_index==i):
            d[i]="informed"

    return d

#Return number of informed nodes at round t
def countInformedNode(G,t):
    states= nx.get_node_attributes(G,'state')
    count = 0
    color_map=[]
    for x in states:
        if(states[x]=='informed'):
            count=count+1
            color_map.append("red")
        else:
            color_map.append("blue")
        plt.figure(t)
        nx.draw_shell(G,node_color = color_map,with_labels=True)
        plt.show()
    if(count==N):
        print("all nodes are informed after "+str(t)+" rounds")
        return True
    print("At the end of round  "+str(t)+" there are "+str(count)+" informed node")
    return False

#Until all nodes are informed, every informed node choose one neighboor at random and push information to it.
def push(G):
        countInformedNode(G,0)
        allInformed=False
        round=1
        while(allInformed==False):
            print("\n\nROUND: "+str(round))
            for v in list(G.nodes()):

                if(G.nodes[v]['state']=='informed'):
                    #sceglie un nodo a caso e lo informa
                    w=random_nb(G,v)
                    print("The node "+str(v)+" push information to "+str(w))
                    G.nodes[w]['state']='informed'
            allInformed=countInformedNode(G,round)
            round=round+1
        #log(n)
        print("\n"+str(math.log(N,2)))

#Take graph G and source s, create dictionary with wich set the initial knowledge of nodes in G. Then start the push protocol  
def prepare2push(G,s):
    if(nx.is_connected(G)==False):
        print("don't play with unconnected graph please")
        return
    d = createAttrDict(s,N)
    nx.set_node_attributes(G,d,'state')
    print("the process is about to start")
    push(G)
    
    

prepare2push(nx.fast_gnp_random_graph(N,P),0)
