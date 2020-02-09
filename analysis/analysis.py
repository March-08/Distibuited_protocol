import requests
import urllib.request, json
import random
import json
from datetime import datetime
from statistics import mean,variance


NOT_CONNECTED=1

class ResponseData:
  def __init__(self, diameter, edgeProbability,numberEdges,numberNodes,sourceDegree,outcome,stage1,stage2):
    self.diameter = diameter
    self.edgeProbability = edgeProbability
    self.numberEdges = numberEdges
    self.numberNodes = numberNodes
    self.sourceDegree = sourceDegree
    self.outcome = outcome
    self.stage1 = stage1
    self.stage2 = stage2

  def toString(self):
       print("diameter: " + str(self.diameter) + "\n" +
             "edgeProbability: " + str(self.edgeProbability) + "\n" +
             "numberEdges: " + str(self.numberEdges) + "\n" +
             "numberNodes: " + str(self.numberNodes) + "\n" +
             "sourceDegree: " + str(self.sourceDegree) + "\n" +
             "outcome: " + str(self.outcome) + "\n" +
             "stage1: " + str(self.stage1) + "\n" +
             "stage2: " + str(self.stage2)
             )

  def to_json(self):
      return json.dumps(self.__dict__)

  @classmethod
  def from_json(cls, json_str):
    json_dict = json.loads(json_str)
    return cls(**json_dict)



def get_data(n,p):
    url="http://artas.pythonanywhere.com/?n={}&p={}".format(n,p)
    url2="http://artas.pythonanywhere.com/return_json"

    start = datetime.now()
    try:
        response1=urllib.request.urlopen(url)
        if(response1.read().decode()=="graph is not connected!"):
            print("graph is not connected!")
            return None
    except:
        return None
    end= datetime.now()
    time_taken_to_generate_key = end - start
    response2=urllib.request.urlopen(url2)
    data = json.loads(response2.read().decode())

    diameter=data["Diameter"]
    edgeProbability=data["Edge probability"]
    numberEdges=data["Number of edges"]
    numberNodes=data["Number of nodes"]
    sourceDegree=data["Source degree"]
    outcome=data["outcome"]
    stage1=data["stage1"]
    stage2=data["stage2"]

    responseData=ResponseData(diameter, edgeProbability,numberEdges,numberNodes,sourceDegree,outcome,stage1,stage2)

    return responseData,time_taken_to_generate_key.total_seconds()

def get_n_requests(n):
    responses=[]
    times=[]
    not_connected_times=0

    for i in range(n):
        nodes = random.randint(2, 100)
        edgeProb = random.random()
        data=get_data(nodes,edgeProb)
        if (data != None):
            response,time=data
            times.append(time)
            responses.append(response)

    #print(times)
    return responses,times

def get_n_fixed_requests(n,nodes,p):
    responses = []
    times = []
    not_connected_times = 0

    for i in range(n):
        data=get_data(nodes, p)
        if(data!=None):
            response,time = data
            times.append(time)
            responses.append(response)

    # print(responses)
    return responses,times

def isClique(responseData):
    n=responseData.numberNodes
    if (responseData.numberEdges==(n*(n-1)/2)):
        return True
    else:
        return False

def  countClique(responses):
    count=0
    for responseData in responses:
        if(isClique(responseData)):
            count+=1
    return count

def min_max_avg_var_edges(responses):
    numberEdges=[]
    for responseData in responses:
        numberEdges.append(responseData.numberEdges)

    min_edges=min(numberEdges)
    max_edges=max(numberEdges)
    avg_edges=mean(numberEdges)
    var_edges=variance(numberEdges)
    return min_edges,max_edges,avg_edges,var_edges

def min_max_avg_var_degree(responses):
    numberDegrees = []
    for responseData in responses:
        numberDegrees.append(responseData.sourceDegree)
    min_degree = min(numberDegrees)
    max_degree = max(numberDegrees)
    avg_degree = mean(numberDegrees)
    var_degree = variance(numberDegrees)
    return min_degree, max_degree, avg_degree, var_degree

def min_max_avg_var_informed_nodes(responses):
    informesNodes = []
    for responseData in responses:
        informesNodes.append(responseData.outcome["# correctly informed"])
    min_informed = min(informesNodes)
    max_informed = max(informesNodes)
    avg_informed = mean(informesNodes)
    var_informed = variance(informesNodes)
    return min_informed, max_informed, avg_informed, var_informed

def all_correctly_informed(responses):
    all=0
    for responseData in responses:
        if responseData.numberNodes==responseData.outcome["# correctly informed"]:
            all+=1
    return all

def majority_informed(responses):   #numero di volte che la maggior parte sono stati inf correttamente
    majority_correctly=0
    majority_incorrectly=0
    for responseData in responses:
        if responseData.numberNodes/2<responseData.outcome["# correctly informed"]:
            majority_correctly+=1
        else:
            majority_incorrectly+=1
    return majority_correctly,majority_incorrectly


def write_statistics(throws,n,p,file_name):
    responses, times = get_n_fixed_requests(throws, n, p)
    min_time = min(times)
    max_time = max(times)
    mean_time = mean(times)
    variance_time = variance(times)
    # total time
    totaltime = 0
    for time in times: totaltime += time
    times_disconnected = throws - len(responses)
    times_connected = len(responses)
    number_of_clique = countClique(responses)

    min_edges, max_edges, avg_edges, var_edges = min_max_avg_var_edges(responses)
    min_degree, max_degree, avg_degree, var_degree = min_max_avg_var_degree(responses)  # e cosa e' successo un qst casi (degree sorgente)
    min_informed, max_informed, avg_informed, var_informed = min_max_avg_var_informed_nodes(responses)

    all_correctly_inf = all_correctly_informed(responses)
    majority_correctly_informed, majority_uncorrectly_informed = majority_informed(responses)

    f=open("../reports/"+file_name+".txt","w+")
    f.write("throws: {}\nnumber_nodes: {}\nedge_probability: {}\n".format(throws,n,p))
    f.write("min_time : {}\nmax_time: {}\navg_time: {}\nvar_time: {}\ntotal_time: {}\n".format(min_time,max_time,mean_time,variance_time,totaltime))
    f.write("times_disconnected : {}\ntimes_connected: {}\nnumber_of_clique: {}\n".format(times_connected,times_disconnected,number_of_clique,))
    f.write("min_edges : {}\nmax_edges: {}\navg_edges: {}\nvar_edges: {}\n".format(min_edges,max_edges,avg_edges,var_edges))
    f.write("min_source_degree : {}\nmax_source_degree: {}\navg_source_degree: {}\nvar_source_degree: {}\n".format(min_degree,max_degree,avg_degree,var_degree))
    f.write("min_correctly_informed : {}\nmax_correctly_informed: {}\navg_correctly_informed: {}\nvar_correctly_informed: {}\n".format(min_informed,max_informed,avg_informed,var_informed))
    f.write("times_all_correctly_informed : {}\ntimes_majority_correctly_informed: {}\ntimes_majority_uncorrectly_informed: {}\n".format(all_correctly_inf,majority_correctly_informed,majority_uncorrectly_informed,))

    f.close()


write_statistics(10,10,1,"stats")






