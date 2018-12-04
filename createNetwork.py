#! /usr/bin/env python2
# -*- coding: utf-8 -*-

## importing the regular python module
import argparse
import math
import os
import random
import string
import sys
from xml.dom import minidom
from xml.dom.minidom import parse
## importing module from project directory
from createVNEInstance import *


# Function to create random substrate network
def create_random_network(graph, tag, prefix, connected):
    """ Creates a random substrate network based on the range of node numbers
    selected by the user and the <edgeProbability> value for connecting two
    substrate nodes.
    Additional Substrate Network Attributes:
    	Substrate Node : Longitude and Latitude, Capacity, Node Emedding Cost.
	Substrate Edge : Bandwidhth Capacity, Link Embedding Cost, Edge Probability."""
    
    numberNodes = random.randint(int(tag.getAttribute("minNumberNodes")), 
                                 int(tag.getAttribute("maxNumberNodes")))
    alpha = float(tag.getAttribute("edgeProbability"))
    min_n_cap = float(tag.getAttribute("minNodeCapacity"))
    n_cap_range = float(tag.getAttribute("maxNodeCapacity")) - min_n_cap
    min_node_cost = float(tag.getAttribute("minNodeCost"))
    max_node_cost = float(tag.getAttribute("maxNodeCost"))
    min_e_cap = float(tag.getAttribute("minEdgeCapacity"))
    e_cap_range = float(tag.getAttribute("maxEdgeCapacity")) - min_e_cap

    ### Creating nodes ###
    for i in range(numberNodes):
        capacity = round(random.random() * n_cap_range + min_n_cap, 1) 
        longitude = random.randint(0, 180)
        latitude = random.randint(0, 90)
        costs = round(random.uniform(min_node_cost, max_node_cost), 1)
        graph.addNode(SubstrateNode(len(graph.nodes), prefix + `i`, capacity,
                                    costs, longitude, latitude))

        ### add edges to ensure connectivity ###
        if connected and i > 0:
            j = random.randint(graph.nodes[-1].id - i, graph.nodes[-1].id -1)
            capacity = round(random.random() * e_cap_range + min_e_cap, 1)
            costs = round((((graph.nodes[-1].longitude-graph.nodes[j].longitude)
                            **2) + ((graph.nodes[-1].latitude-graph.nodes[j].
                                   latitude)**2))**0.5, 1)
            latitudeDifference = math.radians(graph.nodes[-1].latitude - 
                                              graph.nodes[j].latitude)
            longitudeDifference = math.radians(graph.nodes[-1].longitude - 
                                               graph.nodes[j].longitude)
            ### variable needed to calculate distance using Haversine formula
            a = ((math.sin(latitudeDifference/2))**2 +
                 (math.cos(math.radians(graph.nodes[-1].latitude))) *
                 (math.cos(math.radians(graph.nodes[j].latitude))) *
                 ((math.sin(longitudeDifference/2))**2))
            c = 2 * math.atan2(math.sqrt(abs(a)), math.sqrt(abs(1-a)))
            distance = round(6371 * c,1)
            maxDelay = round((distance / 204.357),1)
            graph.addEdge(SubstrateEdge(len(graph.edges),j, graph.nodes[-1].id,
                                        capacity, costs, distance, maxDelay))
    ### Creating edges ###
    for i in range(len(graph.nodes) - numberNodes, len(graph.nodes)):
        for j in range(i+1, len(graph.nodes)):
            if random.random() <= alpha and graph.hasEdge(i,j) == False: 
                capacity = round(random.random() * e_cap_range + min_e_cap, 1)
                costs = round((((graph.nodes[i].longitude - graph.nodes[j].
                                longitude)**2) + ((graph.nodes[i].latitude 
                                - graph.nodes[j].latitude))**2)**0.5, 1)
                latitudeDifference = math.radians(graph.nodes[j].latitude - 
                                                  graph.nodes[i].latitude)
                longitudeDifference = math.radians(graph.nodes[j].longitude - 
                                                   graph.nodes[i].longitude)
                a = ((math.sin(latitudeDifference/2))**2 +
                     (math.cos(math.radians(graph.nodes[-1].latitude))) * 
                     (math.cos(math.radians(graph.nodes[j].latitude))) *
                     ((math.sin(longitudeDifference/2))**2))
                c = 2 * math.atan2(math.sqrt(abs(a)), math.sqrt(abs(1-a)))
                distance = round(6371 * c,1)
                maxDelay = round((distance / 204.357),1)
                graph.addEdge(SubstrateEdge(len(graph.edges), i, j, capacity,
                                             costs, distance, maxDelay))


# Function to create Random Service Request
def create_random_request(substrate, graph, tag, prefix, connected):    
    """ Creates a random service request based on the range of virtual node numbers
    selected by the user and the <edgeProbability> value for connecting two
    virtual nodes.
    Additional Service Request Attributes:
    	Virtual Node : Node Number Range, Capacity Demand, Suitable Substrate Candidate Range,
		       Customer Node Number Range
	Virtual Edge : Bandwidhth Demand, Bounde Tx-delay Range, Edge Probability."""
    
    numberNodes = random.randint(int(tag.getAttribute("minNumberNodes")), 
                                 int(tag.getAttribute("maxNumberNodes")))
    alpha = float(tag.getAttribute("edgeProbability"))
    min_n_cap = float(tag.getAttribute("minNodeCapacity"))
    n_cap_range = float(tag.getAttribute("maxNodeCapacity")) - min_n_cap
    min_e_cap = float(tag.getAttribute("minEdgeCapacity"))
    e_cap_range = float(tag.getAttribute("maxEdgeCapacity")) - min_e_cap
    min_candidates = int(tag.getAttribute("minNumberCandidates"))
    max_candidates = int(tag.getAttribute("maxNumberCandidates"))
    min_customers = int(tag.getAttribute("minNumberCustomers"))
    max_customers = int(tag.getAttribute("maxNumberCustomers"))
    
    ### Creating nodes ###
    for i in range(numberNodes):
        capacity = round(random.random() * n_cap_range + min_n_cap, 1) 
        candidates = []
        num_candidates = random.randint(min_candidates, max_candidates)
        if num_candidates >= len(substrate.nodes):
            candidates =  "all"
        else:
            candidates = range(len(substrate.nodes))
            random.shuffle(candidates)            
            candidates =  candidates[:num_candidates]
        graph.addNode(VirtualNode(len(graph.nodes), prefix + `i`, candidates, 
                                  capacity))
	### add edges to ensure connectivity 
        if connected and i > 0:
            j = random.randint(graph.nodes[-1].id - i, graph.nodes[-1].id -1)
            capacity = round(random.random() * e_cap_range + min_e_cap, 1)
            graph.addEdge(VirtualEdge(len(graph.edges), j, graph.nodes[-1].id, 
                                      capacity, 
                                      random.randint(
                                        int(tag.getAttribute("minEdgeDelay")),
                                        int(tag.getAttribute("maxEdgeDelay")))))
    
    ### Creating edges ###
    for i in range(len(graph.nodes) - numberNodes, len(graph.nodes)):
        for j in range(i+1, len(graph.nodes)):
            if random.random() <= alpha and graph.hasEdge(i,j) == False: 
                capacity = round(random.random() * e_cap_range + min_e_cap, 1)                
                graph.addEdge(VirtualEdge(len(graph.edges), i, j, capacity, 
                                          random.randint(
                                            int(tag.getAttribute(
                                                "minEdgeDelay")),
                                            int(tag.getAttribute(
                                                    "maxEdgeDelay")))))

    ### Adding customers ###
    for c in range(random.randint(min_customers, max_customers)):
        candidates_cNodes = []
        num_candidates_cNodes = random.randint(min_candidates, max_candidates)
        if num_candidates_cNodes >= len(substrate.nodes):
            candidates_cNodes =  "all"
        else:
            candidates_cNodes = range(len(substrate.nodes))
            random.shuffle(candidates_cNodes)            
            candidates_cNodes = candidates_cNodes[:num_candidates_cNodes]
        graph.addNode(VirtualNode(len(graph.nodes),prefix + "c_"+str(c),
                                  candidates_cNodes,round(random.uniform(1.0,
                                                                         5.0))))
        graph.addEdge(VirtualEdge(len(graph.edges), graph.nodes[-1].id, 
                                  random.randint(0, len(graph.nodes) - c - 2), 
                                  round(random.random() * 
                                        e_cap_range + min_e_cap, 1), 
                                  random.randint(
                                    int(tag.getAttribute("minEdgeDelay")),
                                    int(tag.getAttribute("maxEdgeDelay")))))


# Function to write a Random VNE Instance in XML format
def create_randomnet_vne(graph, requests, outFileName):
    """Generates a XML file containing the random substrate nework and random service requests
    based on the user-seleceted parameter file and saves in the current working directory."""

    doc = minidom.Document()	
    root = doc.createElement("VNEInstance")
    root.setAttribute("version" , 0)
    root.setAttribute("schema","VNEInstance.xsd")
    doc.appendChild(root)
    substrate_tag = doc.createElement("substrate")
    root.appendChild(substrate_tag)    
    nodes_tag = doc.createElement("nodes")
    substrate_tag.appendChild(nodes_tag)
    
    for node in graph.nodes:
        node_tag = doc.createElement("node")
        node_tag.setAttribute('id',`node.id`)
        node_tag.setAttribute('nodeName',node.name)
        node_tag.setAttribute('capacity',`node.capacity`)
        node_tag.setAttribute('costs',`node.costs`)		
        node_tag.setAttribute('longitude',`node.longitude`)
        node_tag.setAttribute('latitude',`node.latitude`)
        nodes_tag.appendChild(node_tag)
    edges_tag = doc.createElement("edges")
    substrate_tag.appendChild(edges_tag)

    for edge in graph.edges:
        edge_tag = doc.createElement("edge")
        edge_tag.setAttribute('id',`edge.id`)
        edge_tag.setAttribute('sourceNodeId',`edge.sourceNodeId`)
        edge_tag.setAttribute('destinationNodeId',`edge.destinationNodeId`)
        edge_tag.setAttribute('capacity',`edge.capacity`)
        edge_tag.setAttribute('costs',`edge.costs`)
        edge_tag.setAttribute('edgeDistance',`edge.edgeDistance`)
        edge_tag.setAttribute('edgeDelay',`edge.edgeDelay`)	
        edges_tag.appendChild(edge_tag)
    requests_tag = doc.createElement("requests")
    root.appendChild(requests_tag)

    for req in requests:
        req_tag = doc.createElement("request")
        requests_tag.appendChild(req_tag)
        req_tag.setAttribute('id', `req.id`)
        req_tag.setAttribute('profit',"-10000")
        req_tag.setAttribute('startTime',"0")
        req_tag.setAttribute('revalTime',"0")		
        req_tag.setAttribute('endTime',"100")
        nodes_tag = doc.createElement("virtualNodes")
        req_tag.appendChild(nodes_tag)

        for node in req.nodes:
            node_tag = doc.createElement("virtualNode")
            node_tag.setAttribute('id',`node.id`)
            node_tag.setAttribute('nodeName',node.name)
            node_tag.setAttribute('capacity',`node.capacity`)
            if not node.nodeCandidates == "all":
                candidates = doc.createElement("nodeCandidateIds")
                for c in node.nodeCandidates:
                    c_tag = doc.createElement("nodeId")
                    c_tag.setAttribute('id',`c`)
                    candidates.appendChild(c_tag)			
                node_tag.appendChild(candidates) 
            nodes_tag.appendChild(node_tag)
        edges_tag = doc.createElement("virtualEdges")
        req_tag.appendChild(edges_tag)

        for edge in req.edges:
            edge_tag = doc.createElement("virtualEdge")
            edge_tag.setAttribute('id',`edge.id`)
            edge_tag.setAttribute('sourceNodeId',`edge.sourceNodeId`)
            edge_tag.setAttribute('destinationNodeId',`edge.destinationNodeId`)
            edge_tag.setAttribute('capacity',`edge.capacity`)
            edge_tag.setAttribute('delay',`edge.delay`)
            edges_tag.appendChild(edge_tag)
    outFile=open(outFileName + '.xml',"w")
    print("\nRandom Network VNE Problem Instance is written to {}".
          format(outFileName + '.xml'))
    doc.writexml(outFile, "   ", "\t", "\n", "utf-8")


# Function to create a Fixed Substrate Network and Random Service Requests
def create_fixednet_vne(networkFileName, requests, outputFileName):
    """Generates a XML file containing the Fixed substrate nework based on the user-selected
    any previously generated VNE instance and random service requests based on the user-seleceted
    parameter file,which saves in the current working directory."""

    readData_substrateNetwork = parse(networkFileName)
    substrateNodes = readData_substrateNetwork.getElementsByTagName("node")
    substrateEdges = readData_substrateNetwork.getElementsByTagName("edge")   
    doc = minidom.Document()
    root = doc.createElement("VNEInstance")
    root.setAttribute("version",0)
    root.setAttribute("schema","VNEInstance.xsd")
    doc.appendChild(root)
    substrate_tag = doc.createElement("substrate")
    root.appendChild(substrate_tag)
    nodes_tag = doc.createElement("nodes")
    substrate_tag.appendChild(nodes_tag)

    for node in substrateNodes:
        node_tag = doc.createElement("node")
        node_tag.setAttribute('id',node.attributes['id'].value)
        node_tag.setAttribute('nodeName',node.attributes['nodeName'].value)
        node_tag.setAttribute('capacity',node.attributes['capacity'].value)
        node_tag.setAttribute('costs',node.attributes['costs'].value) 		
        node_tag.setAttribute('longitude',node.attributes['longitude'].value)
        node_tag.setAttribute('latitude',node.attributes['latitude'].value)
        nodes_tag.appendChild(node_tag)
    edges_tag = doc.createElement("edges")
    substrate_tag.appendChild(edges_tag)

    for edge in substrateEdges:
        edge_tag = doc.createElement("edge")
        edge_tag.setAttribute('id',edge.attributes['id'].value)
        edge_tag.setAttribute('sourceNodeId',edge.
                              attributes['sourceNodeId'].value)
        edge_tag.setAttribute('destinationNodeId',edge.
                              attributes['destinationNodeId'].value)
        edge_tag.setAttribute('capacity',edge.attributes['capacity'].value)
        edge_tag.setAttribute('costs',edge.attributes['costs'].value)
        edge_tag.setAttribute('edgeDistance',edge.
                              attributes['edgeDistance'].value)
        edge_tag.setAttribute('edgeDelay',edge.attributes['edgeDelay'].value)
        edges_tag.appendChild(edge_tag)
    requests_tag = doc.createElement("requests")
    root.appendChild(requests_tag)
    for req in requests:
        req_tag = doc.createElement("request")
        requests_tag.appendChild(req_tag)
        req_tag.setAttribute('id',`req.id`)
        req_tag.setAttribute('profit',"-10000")
        req_tag.setAttribute('startTime',"0")
        req_tag.setAttribute('revalTime',"0")		
        req_tag.setAttribute('endTime',"100")
        nodes_tag = doc.createElement("virtualNodes")
        req_tag.appendChild(nodes_tag)

        for node in req.nodes:
            node_tag = doc.createElement("virtualNode")
            node_tag.setAttribute('id',`node.id`)
            node_tag.setAttribute('nodeName',node.name)
            node_tag.setAttribute('capacity' ,`node.capacity`)
            if not node.nodeCandidates == "all":
                candidates = doc.createElement("nodeCandidateIds")
                for c in node.nodeCandidates:
                    c_tag = doc.createElement("nodeId")
                    c_tag.setAttribute('id',`c`)
                    candidates.appendChild(c_tag)			
                node_tag.appendChild(candidates)  
            nodes_tag.appendChild(node_tag)
        edges_tag = doc.createElement("virtualEdges")
        req_tag.appendChild(edges_tag)

        for edge in req.edges:
            edge_tag = doc.createElement("virtualEdge")
            edge_tag.setAttribute('id',`edge.id`)
            edge_tag.setAttribute('sourceNodeId',`edge.sourceNodeId`)
            edge_tag.setAttribute('destinationNodeId',`edge.destinationNodeId`)
            edge_tag.setAttribute('capacity',`edge.capacity`)
            edge_tag.setAttribute('delay',`edge.delay`)
            edges_tag.appendChild(edge_tag)
    outFile=open(outputFileName +'.xml',"w")
    print("\nFixed Network VNE Problem Instance is written to {}".
          format(outputFileName + '.xml'))
    doc.writexml(outFile, "   ", "\t", "\n", "utf-8")


# Function to determine the number of generated service requests based on user-set number
def generate_requests(substrate,tag):
    """Determines the number of service requests generation according to the value
    given in the requests tag."""
    requests = []
    for i in range( int(tag.getAttribute("numberOfRequests"))):
	requests.append(VirtualGraph(i, [], [], {} ))
	create_random_request(substrate, requests[-1], tag, "", True  )
	return requests

# Definie the main function
def main(argv):
    description='Random and Fixed Network VNE Instance Creator'    
    parser = argparse.ArgumentParser(description=description)    
    parser.add_argument('-i','--info',
			action='store_true',
			dest='infoFlag',
			default=False,
			required=False,
			help='show transformation information')      
    parser.add_argument('-o','--outputFile',
			action='store',
			dest='output',
			metavar='outputVNEProblemFile',
			default="",
			help='Output file name of generated VNE Problem')    
    parser.add_argument('--input','--inputSNFile',
			dest='inputNetworkInstance',
			metavar='inputNetworkInstanceFile',
			default="",
			help='input Substrate Network Instance file name') 
    parser.add_argument('--xml',
			action='store',
			dest='paramFile',
			metavar='graphParameter',
			default=None,
			required=True,
			help='Parameter file for graph construction')
    global args
    args = parser.parse_args()
    doc = parse(args.paramFile)
    if args.inputNetworkInstance:
        doc1 = parse(args.inputNetworkInstance)
        substrateNodes = doc1.getElementsByTagName("node")
        f_substrate = SubstrateGraph(1, substrateNodes, [], {})
        for tag in doc.getElementsByTagName( "requests" ):
            req_fix = generate_requests(f_substrate, tag)
            create_fixednet_vne(args.inputNetworkInstance,
                                req_fix, args.output)
    else:
        for pureRandom in doc.getElementsByTagName("pureRandom"):
            substrate = SubstrateGraph(pureRandom.
                                       getAttribute("id"), [], [], {})
            create_random_network(substrate, pureRandom, "", True)
            for tag in pureRandom.getElementsByTagName("requests"):
                requests = generate_requests(substrate, tag)
                create_randomnet_vne(substrate, requests, args.output)

if __name__ == "__main__":
  main(sys.argv[1:])

