# -*- coding: utf-8 -*-
"""
Created on Sat Nov 23 16:07:32 2019

@author: Lorenzo
"""
from flask import Flask
from flask import request
app = Flask(__name__)

#perchè 1 è spesso non informato?

#Breath before speaking protocol for rumor spreading with noisy comunication
import networkx as nx
import protocol
import math
import random
import biasing as bs
import json
#noisy probability is 0.5-E
E = 0.3
# #nodes
#N = 50
#Erdos-renyi probability
#P=0.5
#costant for number of phases
C1=1
#costant for number of rounds
C2=1


def is_flipped(a):
    count=0
    for x in a:
        count=count+x
    if(count>=(len(a)/2)):
        return 1
    return 0

def prepare_json(nedge,diam,sdegree,N,P):
    data = {}
    data["Number of nodes"] = N
    data["Edge probability"] = P
    data["Number of edges"] = nedge
    data["Diameter"] = diam
    data["Source degree"] = sdegree
    data["stage1"] = []
    return data

def breathe_stage1(G,s,info_source,info_other,N,P):
    print("\n\n\n HELLO IN NEW EXECUTION: \n\n\n")
    #1/E^2*logn round solo la sorgente

    data = prepare_json(G.number_of_edges(),nx.diameter(G),G.degree[s],N,P)
    _,uninf,data=protocol.countInformedNode2(G,0,info_source,N,data)
    round=1

    for phase in range(0,C1*math.floor(math.log(N,2))):

       for _ in range(0,math.floor(C2*1/math.pow(E,2))):

            w=protocol.random_nb(G,s)
            if(G.nodes[w]['state']==info_other):
                msg_arrive = bs.biasing1(1/2+E)
                if(msg_arrive==1):
                    G.nodes[w]['state']=G.nodes[s]['state']
                else:
                    #message is flipping
                    G.nodes[w]['state']=G.nodes[s]['state']+1%2
            _,uninf,data=protocol.countInformedNode2(G,round,info_source,N,data)
            round = round+1

    for phase in range(0,C1*math.floor(math.log(N,2))-1):
        #informed list take account of nodes speak to who at phase i
        informed=[]
        if(uninf==0):
                break
        for _ in range(0,math.floor(C2*1/math.pow(E,2))):

            #BREATHE
            for v in list(G.nodes()):
                if(G.nodes[v]['state']== 0 or G.nodes[v]['state']== 1):
                    #sceglie un nodo a caso e lo informa
                    w=protocol.random_nb(G,v)
                    informed.append([v,w]);

            #SPEAKING
            for [v,w] in informed:
                #If w is not informed yet
                if(G.nodes[w]['state']==info_other):
                    #print("il nodo "+str(w)+" sta per cambiare idea")
                    no_error=bs.biasing1(1/2+E)
                    if(no_error==1):
                        G.nodes[w]['state']=G.nodes[v]['state']
                    else:
                        #message is flipping
                        G.nodes[w]['state']=G.nodes[v]['state']+1%2
            _,uninf,data=protocol.countInformedNode2(G,round,info_source,N,data)
            round=round+1
            if(uninf==0):
                break

    with open('/home/artas/mysite/data.json', 'w') as f:
        json.dump(data, f, ensure_ascii=False, indent=4)
    return G,data





def breathe_stage2(G,s,info_source,info_other,N,data):
    data["stage2"]=[]
    for v in G.nodes():
        #red is correct info
        red=0
        #blu is flipped info
        blu=0
        sampling_value = 0
        for sample in range(0,math.floor(C2*1/math.pow(E,2))):
            w=protocol.random_nb(G,v)
            if(G.nodes[w]['state']==0 or G.nodes[w]['state']==1):
                if(G.nodes[w]['state']==info_source):
                    red=red+1
                else:
                    blu=blu+1

        if(red>blu):
            G.nodes[v]['state']=info_source
        elif(blu>red):
            G.nodes[v]['state']=info_source+1%2
        else:
            G.nodes[v]['state']=bs.biasing1(1/2)

        sampling_value = "correct info" if G.nodes[v]['state']==info_source else "uncorrect info"
        sampling = {"sampling value node "+str(v): sampling_value}
        data["stage2"].append(sampling)



    info,badinfo = protocol.countInformation(G,info_source)
    data["outcome"]={"# correctly informed":info,"# uncorrectly informed": badinfo}
    with open('/home/artas/mysite/data.json', 'w') as f:
        json.dump(data, f, ensure_ascii=False, indent=4)




@app.after_request
def apply_caching(response):
    response.headers['Cache-Control'] = 'no-cache, no-store, must-revalidate'
    return response


@app.route('/return_json')
def ret_json():
    f = open('/home/artas/mysite/data.json','rb')
    data = f.read()
    return json.loads(data)


@app.route('/', methods=['GET'])
def prepare_html():
        N= request.args.get('n')
        P= request.args.get('p')

        ret = prepare2breathe(nx.fast_gnp_random_graph(int(N),float(P)),random.randrange(0,int(N)),int(N),float(P))
        if(ret == -1):
            return "graph is not connected!"
        maj = 0
        f = open('/home/artas/mysite/data.json','rb')
        data = f.read()
        data = json.loads(data)
        if(data["outcome"]["# correctly informed"]>data["outcome"]["# uncorrectly informed"]):
            maj="Ants correctly understand that there is a cricket!"
        else:
            maj="Ants understand that there is a bear outside! all ants are running now!"
        s = """
        <html>
            <head>
                <title>BBS</title>
            </head>
            <body>
                <h1>Welcome to the arena</h1>
                <p>"""+maj+"""</p>
                <a href="/return_json"> See why ants behave like that! download json </a>
            </body>
        </html>
        """
        return s

'''
@app.route('/', methods=['GET'])
def ret_json():
        N= request.args.get('n')
        P= request.args.get('p')

        ret = prepare2breathe(nx.fast_gnp_random_graph(int(N),float(P)),random.randrange(0,int(N)),int(N),float(P))
        if(ret == -1):
            return "graph is not connected!"
        f = open('/home/artas/mysite/data.json','rb')
        data = f.read()
        return json.loads(data)
'''



def  breathe(G,s,info_source,info_other,N,P):
    G,data = breathe_stage1(G,s,info_source,info_other,N,P)
    breathe_stage2(G,s,info_source,info_other,N,data)


def prepare2breathe(G,s,N,P):
    if(nx.is_connected(G)==False):
        print("don't play with unconnected graph please")
        return -1
    d = protocol.createAttrDict(s,N,0,"uninformed")
    nx.set_node_attributes(G,d,'state')
    print("the process is about to start")
    breathe(G,s,0,"uninformed",N,P)
    return 1


if __name__=='__main__':
    app.run()


