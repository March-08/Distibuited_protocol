# -*- coding: utf-8 -*-
"""
Created on Wed Dec  4 09:48:47 2019

@author: utente
"""

import json

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


def countInformation(G,info_source):
    states= nx.get_node_attributes(G,'state')
    info = 0
    badinf = 0
    for x in states:
        if(states[x]==info_source):
            info=info+1
        elif(states[x]==(info_source+1%2)):
            badinf=badinf+1
    return info,badinf


#Return number of informed nodes at round t and print an image of the info-situation at that round
def countInformedNode2(G,t,info_source,N,data):

    round = {}

    info,badinf = countInformation(G,info_source)
    if(info+badinf==N):

        round={"round"+str(t):"all nodes are informed"}
        data["stage1"].append(round)

        uninf=N-(info+badinf)
        return info,uninf,data

    uninf=N-(info+badinf)
    round = {"round":t,"informed":info,"bad_informed":badinf,"uninformed":uninf}
    data["stage1"].append(round)

    return info,uninf,data

'''

#Return number of informed nodes at round t and print an image of the info-situation at that round
def countInformedNode2(G,t,info_source,info_other,N):
    f = open('/home/artas/mysite/data.json','rb')
    data = f.read()
    data = json.loads(data)
    f.close()
    f=open('/home/artas/mysite/data.json',"w",encoding="utf-8")
    round = {}
    states= nx.get_node_attributes(G,'state')
    info = 0
    badinf = 0
    #color_map=[]
    #if(N<500):
    for x in states:
        if(states[x]==info_source):
            info=info+1
            #informed
    #         color_map.append("red")
        elif(states[x]==(info_source+1%2)):
                #bad information
                #color_map.append("blue")
            badinf=badinf+1
           # else:
                #uninformed
    #            uninf=uninf+1
    #            color_map.append("green")
    # plt.figure(t)
     #   nx.draw_random(G,node_color = color_map,with_labels=True)
      #  plt.show()

    if(info+badinf==N):
    #    print("all nodes are informed after "+str(t)+" rounds")
        round["round "+str(t)]="all nodes are informed"
        data["stage1"].append(round)
        json.dump(data, f, ensure_ascii=False, indent=4)
        uninf=N-(info+badinf)
        return info,uninf
    #print("At the end of round  "+str(t)+" there are "+str(info)+" correctly informed node")
    uninf=N-(info+badinf)
    round["round "+str(t)]={"informed":info,"bad_informed":badinf,"uninformed":uninf}
    data["stage1"].append(round)
    json.dump(data, f, ensure_ascii=False, indent=4)
    f.close()
    return info,uninf

'''


#Usato da mobile per salvataggio
def countInformedNode3(G,t,info_source,info_other,N):
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
        plt.savefig('static/foo'+str(t)+'.png')

    if(count==N):
        #print("all nodes are informed after "+str(t)+" rounds")
        return True
   # print("At the end of round  "+str(t)+" there are "+str(count)+" informed node")
    return False


#Return random neighboor of node v in graph G
def random_nb(G,v):
    nb = nx.all_neighbors(G,v)
    if(nb):
        return random.sample(list(nb),1)[0]
    else:
        print("Graph is not connected")
        exit;

