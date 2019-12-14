# -*- coding: utf-8 -*-
"""
Created on Sat Nov 23 16:07:32 2019

@author: Lorenzo
"""

#Breath before speaking protocol for rumor spreading with noisy comunication
import networkx as nx
import protocol
from numpy.random import choice
import math
import random
import biasing as bs

#noisy probability is 0.5-E
E = 0.3
# #nodes
N = 5
#Erdos-renyi probability
P=0.5
#costant for number of phases
C1=5
#costant for number of rounds
C2=5

#Stage 1 of breath before speaking protocol: for O(logn) phases and for O(1/E^2) round for each phases each
#   informed agent send its opinion and each uninformed agent listen incoming opinion and at the end of the phase 
#       become informed with the first opinion has recived

def breathe_stage1(G,info_source,info_other):
     round = 1
     #print initial state of envirorment
     allInformed=protocol.countInformedNode2(G,0,info_source,info_other,N)
     allInformed=False
     
     #Phases
     for i in range(0,C1 * math.floor(math.log(N,2))):
          inform=[]
          print("\n\nROUND "+str(round)+":\n")
          #BREATHE
          for v in list(G.nodes()):
            if(G.node[v]['state']== 0 or G.node[v]['state']== 1):
                #sceglie un nodo a caso e lo informa
                w=protocol.random_nb(G,v)
                inform.append([v,w]);

          #SPEAKING
          for [v,w] in inform:
               #If w isn't informed yet
               if(G.node[w]['state']==info_other):  
                   #Sending simulate for O(1/e^2) times(ROUND)
                   for i in range(0,math.floor(C2*1/math.pow(E,2))):
                        spread_info = bs.biasing1(0.5-E)
                   
                   #If spread_info==1 it means that after ROUND sending the message was flipped
                   if(spread_info==1):
                       #Flipping the message and sending it
                       G.node[w]['state']=G.node[v]['state']+1% 2
                       if(G.node[w]['state']!=info_source):
                           print("The node "+str(v)+" push BAD information to "+str(w)+" for flip!")
                       else:
                           print("The node "+str(v)+" push information to "+str(w)+" even if flipped")
                             
                   else:
                       #Send message witouth flip
                       print("The node "+str(v)+" push information to "+str(w))
                       G.node[w]['state']=G.node[v]['state']
               else:
                   print("il nodo "+str(v)+"ha provato a informare nuovamente "+str(w)+" ma "+str(w)+" è furbo e non cambia idea")
          allInformed=protocol.countInformedNode2(G,round,info_source,info_other,N)
          round=round+1   
     return G
   
        

def breathe_stage2(G,s,o):
    red=0
    blue=0
    for v in G.nodes():
        if(G.node[v]['state']==0):
            red=red+1
        elif(G.node[v]['state']==1):
            blue=blue+1
    maj=0
    if(blue > red ):
        protocol.colorAll(G,"blue")
    else:
        protocol.colorAll(G,"red")


        
               
            
            

def  breathe(G,info_source,info_other):
    G = breathe_stage1(G,info_source,info_other)
    breathe_stage2(G,info_source,info_other)
   
def prepare2breathe(G,s):
    if(nx.is_connected(G)==False):
        print("don't play with unconnected graph please")
        return
    d = protocol.createAttrDict(s,N,0,"uninformed")
    nx.set_node_attributes(G,d,'state')
    print("the process is about to start")
    breathe(G,0,"uninformed")
    
 

prepare2breathe(nx.fast_gnp_random_graph(N,P),random.randrange(0,N))

