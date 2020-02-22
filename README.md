# Breath before speaking: a push protocol for rumor spreading with noise


## Synopsis
This repository contains the source code of an implementation for the Breath Before Speaking algorithm described in [https://doi.org/10.1007/s00446-015-0249-4](https://doi.org/10.1007/s00446-015-0249-4).



# Usage and code structure
## Usage
The code is powered by Flask [https://palletsprojects.com/p/flask/](https://palletsprojects.com/p/flask/).
The breathBeforeSpeaking.py file is stored on a "python web server" at this url: [http://artas.pythonanywhere.com](http://artas.pythonanywhere.com)

The server accept a GET request and it takes two request parameters, used for create the random graph : 

 - **n**: number of nodes
 - **p**: probability that there is an edge between two nodes

So for example, if you want simulate the protocol for a Gnp random graph with 100 nodes and edge probability of 0.5 you can make a GET request like: http://artas.pythonanywhere.com?n=100&p=0.5.

### Web response
The code executes the protocol and put the result on a json file. This json file is linked by an html page, created in the code and returned to the GET request. 
So when you make the GET, you get (pardon the pun!) an html page in wich there is the fundamental information: does the correct information win?
In each cases the json provides all the information about the outcome.

## Code structures

 1. As sayed before, the code is powered by Flask. The route-start-function, named **prepare_html**, take the request parameters and start the protocol with the function **prepare2breath** after creating the random graph with n and p passed.
 2. **prepare2breath(G)** takes a graph and, if it is connected, it sets the initial knowledge of nodes in G (a random source is the only informed node). Then it call the first stage of the protocol.
 3. **breath_stage1(G,source,info_source, info_other,N, P)** is the function that simulate the first stage of the breath before speaking algorithm (as explained in [https://doi.org/10.1007/s00446-015-0249-4](https://doi.org/10.1007/s00446-015-0249-4)) where source is the random source that know the information to spread, info_source and info_other are the "information" and the "un-information" values and P and N are the request parameters.
 4. After that the second stage is executed by the **breath_stage2** function.





# Android App
<a href="https://imgflip.com/gif/3powgj"><img src="https://i.imgflip.com/3powgj.gif" title="made at imgflip.com"/></a>

This is the implementation of an android app, to visualize the results of the protocol, and it was built using Flutter.
For the source code or for more information about the app contact us mpoliti08@gmail.com.














