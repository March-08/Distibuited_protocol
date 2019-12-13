# -*- coding: utf-8 -*-
"""
Created on Wed Dec  4 09:48:47 2019

@author: utente
"""
import matplotlib.pyplot as plt
import random
import networkx as nx

#Return dictionary that represent initial knowledge value of the node in the Graph
def createAttrDict(s,n,info_source,info_other):
    d ={}
    for i in range(0,n):
        d[i]=info_other
    d[s]=info_source
    return d


def colorAll(G,color):
    color_map=[] 
    for v in G.nodes():
        color_map.append(color)
    nx.draw_random(G,node_color = color_map,with_labels=True)
    plt.show()

#Return number of informed nodes at round t and print an image of the info-situation at that round
def countInformedNode(G,t,info_source,info_other,N):
    states= nx.get_node_attributes(G,'state')
    count = 0
    color_map=[]
    if(N<500):
        for x in states:
            if(states[x]==info_source):
                count=count+1
                color_map.append("red")
            else:
                color_map.append("blue")
        plt.figure(t)
        nx.draw_random(G,node_color = color_map,with_labels=True)
        plt.show()
        
    if(count==N):
        print("all nodes are informed after "+str(t)+" rounds")
        return True
    print("At the end of round  "+str(t)+" there are "+str(count)+" informed node")
    return False

def countInformedNode2(G,t,info_source,info_other,N):
    states= nx.get_node_attributes(G,'state')
    count = 0
    color_map=[]
    if(N<500):
        for x in states:
            if(states[x]==info_source):
                count=count+1
                #informed
                color_map.append("red")
            elif(states[x]==(info_source+1%2)):
                #bad information
                color_map.append("blue")
            else:
                #uninformed
                color_map.append("green")
        plt.figure(t)
        nx.draw_random(G,node_color = color_map,with_labels=True)
        plt.show()
        
    if(count==N):
        print("all nodes are informed after "+str(t)+" rounds")
        return True
    print("At the end of round  "+str(t)+" there are "+str(count)+" informed node")
    return False


#Return random neighboor of node v in graph G
def random_nb(G,v):
    nb = nx.all_neighbors(G,v)
    if(nb):
        return random.choice(list(nb))
    else:
        print("Graph is not connected")
        exit;

