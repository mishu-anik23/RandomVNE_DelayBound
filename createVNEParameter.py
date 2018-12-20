#! /usr/bin/env python2
# -*- coding: utf-8 -*-

import sys
import string
import os
import argparse
import xml.dom.minidom as dom
from xml.dom.minidom import getDOMImplementation
from xml.dom import minidom
from xml.dom.minidom import parse

def createVNEParam_fullMod_userDefined( outputFileName ):
    """ 
    Writes a xml file containing the fully modified VNE Parameter set by the 
    user to user given <outFileName> 
    """    
    print("\nAsking Parameters to create the Substrate Network...\n")
    minSubNode =  raw_input("\nEnter Minimum no of SubNode:\n") 
    maxSubNode =  raw_input("\nEnter Maximum no of SubNode:\n") 
    minSubNodeCapacity = raw_input("\nEnter Minimum SubNode Capacity:\n") 
    maxSubNodeCapacity = raw_input("\nEnter Maximum SubNode Capacity:\n") 
    minEmbCost = raw_input("\nEnter Minimum SubNode Embedding Cost:\n") 
    maxEmbCost = raw_input("\nEnter Maximum SubNode Embedding Cost:\n") 
    subEdgeProbability = raw_input("\nEnter Edge Probability:\n") 
    minSubEdgeCapacity = raw_input("\nEnter Minimum Edge Capacity:\n") 
    maxSubEdgeCapacity = raw_input("\nEnter Maximum Edge Capacity:\n") 
    
    print("\nAsking Parameters to create the Virtual Requests...\n")
    minReqNum = raw_input("\nEnter no of Request you wish to generate:\n") 
    minVirNode = raw_input("\nEnter Minimum no of Virtual Node:\n") 
    maxVirNode = raw_input("\nEnter Maximum no of Virtual Node:\n") 
    minVirNodeCapacity = raw_input("\nEnter Minimum Virtual Node Capacity:\n") 
    maxVirNodeCapacity = raw_input("\nEnter Maximum Virtual Node Capacity:\n") 
    virEdgeProbability =  raw_input("\nEnter Edge Probability:\n") 
    minVirEdgeCapacity = raw_input("\nEnter Minimum Virtual Edge Capacity:\n") 
    maxVirEdgeCapacity = raw_input("\nEnter Maximum Virtual Edge Capacity:\n") 
    minVirEdgeDelay = raw_input("\nEnter Minimum Virtual Edge Delay:\n") 
    maxVirEdgeDelay = raw_input("\nEnter Maximum Virtual Edge Delay:\n") 
    minSubCandidates = raw_input("\nEnter Minimum Substrate Candidates:\n") 
    maxSubCandidates = raw_input("\nEnter Maximum Substrate Candidates:\n") 
    minCustomer = raw_input("\nEnter Minimum Added Customer:\n") 
    maxCustomer = raw_input("\nEnter Maximum Added Customer:\n") 
 
    doc = minidom.Document()	
    root = doc.createElement("VNEParameter")
    root.setAttribute("version" , 0)
    root.setAttribute("schema" , "VNEParameterInstance_fullMod.xsd")
    
    doc.appendChild(root)
    
    randomNet_tag = doc.createElement("pureRandom")
    randomNet_tag.setAttribute('id', `1.1`)
    randomNet_tag.setAttribute('minNumberNodes', minSubNode)
    randomNet_tag.setAttribute('maxNumberNodes', maxSubNode)
    randomNet_tag.setAttribute('minNodeCost', minEmbCost)
    randomNet_tag.setAttribute('maxNodeCost', maxEmbCost)
    randomNet_tag.setAttribute('edgeProbability', subEdgeProbability)
    randomNet_tag.setAttribute('minNodeCapacity', minSubNodeCapacity)
    randomNet_tag.setAttribute('maxNodeCapacity', maxSubNodeCapacity)
    randomNet_tag.setAttribute('minEdgeCapacity', minSubEdgeCapacity)
    randomNet_tag.setAttribute('maxEdgeCapacity', maxSubEdgeCapacity)

    root.appendChild(randomNet_tag)

    request_tag = doc.createElement("requests")
    request_tag.setAttribute('id', `1.2`)
    request_tag.setAttribute('numberOfRequests', minReqNum)
    request_tag.setAttribute('minNumberNodes', minVirNode)
    request_tag.setAttribute('maxNumberNodes', maxVirNode)
    request_tag.setAttribute('edgeProbability', virEdgeProbability)
    request_tag.setAttribute('minNodeCapacity', minVirNodeCapacity)
    request_tag.setAttribute('maxNodeCapacity', maxVirNodeCapacity)
    request_tag.setAttribute('minEdgeCapacity', minVirEdgeCapacity)
    request_tag.setAttribute('maxEdgeCapacity', maxVirEdgeCapacity)
    request_tag.setAttribute('minEdgeDelay', minVirEdgeDelay)
    request_tag.setAttribute('maxEdgeDelay', maxVirEdgeDelay)
    request_tag.setAttribute('minNumberCandidates', minSubCandidates)
    request_tag.setAttribute('maxNumberCandidates', maxSubCandidates)
    request_tag.setAttribute('minNumberCustomers', minCustomer)
    request_tag.setAttribute('maxNumberCustomers', maxCustomer)
                    
    randomNet_tag.appendChild(request_tag)
    
    outFile = open(outputFileName +'.xml',"w")
    print("\nHere is your generated full modified VNE Parameter File ...\n")
    doc.writexml(sys.stdout, "   ", "\t", "\n", "utf-8")
    doc.writexml( outFile , "   ", "\t", "\n", "utf-8")
    print("\nYour fully Modified VNE Parameter File has written to {}".
    format(outputFileName + '.xml'))

def createVNEParam_netMod_userDefined( inputFileName , outputFileName  ):
    """ 
    Writes a xml file containing the modified Network Parameter set by the 
    user with default Request Parameter to user given <outFileName> """
    
    print("\nAsking Parameters to create the Substrate Network...\n")
    minSubNode =  raw_input("\nEnter Minimum no of SubNode:\n") 
    maxSubNode =  raw_input("\nEnter Maximum no of SubNode:\n") 
    minSubNodeCapacity = raw_input("\nEnter Minimum SubNode Capacity:\n") 
    maxSubNodeCapacity = raw_input("\nEnter Maximum SubNode Capacity:\n") 
    minEmbCost = raw_input("\nEnter Minimum SubNode Embedding Cost:\n") 
    maxEmbCost = raw_input("\nEnter Maximum SubNode Embedding Cost:\n") 
    subEdgeProbability = raw_input("\nEnter Edge Probability:\n") 
    minSubEdgeCapacity = raw_input("\nEnter Minimum Edge Capacity:\n") 
    maxSubEdgeCapacity = raw_input("\nEnter Maximum Edge Capacity:\n")
    
    docOut = minidom.Document()	
    root = docOut.createElement("VNEParameter")
    root.setAttribute("version" , 0)
    root.setAttribute("schema" , 
                      "VNEParameterInstance_networkMod_defaultRequest.xsd")    
    docOut.appendChild(root) 

    randomNet_tag = docOut.createElement("pureRandom")
    randomNet_tag.setAttribute('id', `1.1`)
    randomNet_tag.setAttribute('minNumberNodes', minSubNode)
    randomNet_tag.setAttribute('maxNumberNodes', maxSubNode)
    randomNet_tag.setAttribute('minNodeCost', minEmbCost)
    randomNet_tag.setAttribute('maxNodeCost', maxEmbCost)
    randomNet_tag.setAttribute('edgeProbability', subEdgeProbability)
    randomNet_tag.setAttribute('minNodeCapacity', minSubNodeCapacity)
    randomNet_tag.setAttribute('maxNodeCapacity', maxSubNodeCapacity)
    randomNet_tag.setAttribute('minEdgeCapacity', minSubEdgeCapacity)
    randomNet_tag.setAttribute('maxEdgeCapacity', maxSubEdgeCapacity)

    root.appendChild(randomNet_tag)

    docIn = parse(inputFileName)

    requestsTag_inputFile = docIn.getElementsByTagName("requests")
    for requestsTagAtts in requestsTag_inputFile:
        request_tag = docOut.createElement("requests")
        request_tag.setAttribute('id', requestsTagAtts.attributes['id'].value)
        request_tag.setAttribute('numberOfRequests', requestsTagAtts.
                                 attributes['numberOfRequests'].value)
        request_tag.setAttribute('minNumberNodes', requestsTagAtts.
                                 attributes['minNumberNodes'].value)
        request_tag.setAttribute('maxNumberNodes', requestsTagAtts.
                                 attributes['maxNumberNodes'].value)
        request_tag.setAttribute('edgeProbability', requestsTagAtts.
                                 attributes['edgeProbability'].value)
        request_tag.setAttribute('minNodeCapacity', requestsTagAtts.
                                 attributes['minNodeCapacity'].value)
        request_tag.setAttribute('maxNodeCapacity', requestsTagAtts.
                                 attributes['maxNodeCapacity'].value)
        request_tag.setAttribute('minEdgeCapacity', requestsTagAtts.
                                 attributes['minEdgeCapacity'].value)
        request_tag.setAttribute('maxEdgeCapacity', requestsTagAtts.
                                 attributes['maxEdgeCapacity'].value)
        request_tag.setAttribute('minEdgeDelay', requestsTagAtts.
                                 attributes['minEdgeDelay'].value)
        request_tag.setAttribute('maxEdgeDelay', requestsTagAtts.
                                 attributes['maxEdgeDelay'].value)
        request_tag.setAttribute('minNumberCandidates', requestsTagAtts.
                                 attributes['minNumberCandidates'].value)
        request_tag.setAttribute('maxNumberCandidates', requestsTagAtts.
                                 attributes['maxNumberCandidates'].value)
        request_tag.setAttribute('minNumberCustomers', requestsTagAtts.
                                 attributes['minNumberCustomers'].value)
        request_tag.setAttribute('maxNumberCustomers', requestsTagAtts.
                                 attributes['maxNumberCustomers'].value)                   
    randomNet_tag.appendChild(request_tag)
    outFile = open(outputFileName +'.xml',"w")
    print("\nHere is your generated Modified Network but Default Requests "
          "VNE Parameter File ...\n")
    docOut.writexml(sys.stdout, "   ", "\t", "\n", "utf-8")
    docOut.writexml( outFile , "   ", "\t", "\n", "utf-8")
    print("\nYour Modified Network but Default Requests VNE Parameter File "
          "has written to {}".format(outputFileName + '.xml'))

def createVNEParam_reqMod_userDefined(inputFileName, outputFileName):
    """ 
    Writes a xml file containing the modified Request Parameter set by the 
    user with default Network Parameter to user given <outFileName>
    """
    print("\nAsking Parameters to create the Virtual Requests...\n")
    minReqNum = raw_input("\nEnter no of Request you wish to generate:\n") 
    minVirNode = raw_input("\nEnter Minimum no of Virtual Node:\n") 
    maxVirNode = raw_input("\nEnter Maximum no of Virtual Node:\n") 
    minVirNodeCapacity = raw_input("\nEnter Minimum Virtual Node Capacity:\n") 
    maxVirNodeCapacity = raw_input("\nEnter Maximum Virtual Node Capacity:\n") 
    virEdgeProbability =  raw_input("\nEnter Edge Probability:\n") 
    minVirEdgeCapacity = raw_input("\nEnter Minimum Virtual Edge Capacity:\n") 
    maxVirEdgeCapacity = raw_input("\nEnter Maximum Virtual Edge Capacity:\n") 
    minVirEdgeDelay = raw_input("\nEnter Minimum Virtual Edge Delay:\n") 
    maxVirEdgeDelay = raw_input("\nEnter Maximum Virtual Edge Delay:\n") 
    minSubCandidates = raw_input("\nEnter Minimum Substrate Candidates:\n") 
    maxSubCandidates = raw_input("\nEnter Maximum Substrate Candidates:\n") 
    minCustomer = raw_input("\nEnter Minimum Added Customer:\n") 
    maxCustomer = raw_input( "\nEnter Maximum Added Customer:\n") 

    docOut = minidom.Document()	

    root = docOut.createElement("VNEParameter")
    root.setAttribute("version" , 0)
    root.setAttribute("schema" , 
                      "VNEParameterInstance_virReqMod_defaultNetwork.xsd")    
    docOut.appendChild( root ) 
    docIn = parse( inputFileName )    
    pureRandomTag_inputFile = docIn.getElementsByTagName("pureRandom")    
    for pureRandomTagAtts in pureRandomTag_inputFile:
        randomNet_tag = docOut.createElement("pureRandom")        
        randomNet_tag.setAttribute('id', pureRandomTagAtts.
                                   attributes['id'].value)
        randomNet_tag.setAttribute('minNumberNodes', pureRandomTagAtts.
                                   attributes['minNumberNodes'].value)
        randomNet_tag.setAttribute('maxNumberNodes', pureRandomTagAtts.
                                   attributes['maxNumberNodes'].value)
        randomNet_tag.setAttribute('minNodeCost', pureRandomTagAtts.
                                   attributes['minNodeCost'].value)
        randomNet_tag.setAttribute('maxNodeCost', pureRandomTagAtts.
                                   attributes['maxNodeCost'].value)
        randomNet_tag.setAttribute('edgeProbability', pureRandomTagAtts.
                                   attributes['edgeProbability'].value)
        randomNet_tag.setAttribute('minNodeCapacity', pureRandomTagAtts.
                                   attributes['minNodeCapacity'].value)
        randomNet_tag.setAttribute('maxNodeCapacity', pureRandomTagAtts.
                                   attributes['maxNodeCapacity'].value)
        randomNet_tag.setAttribute('minEdgeCapacity', pureRandomTagAtts.
                                   attributes['minEdgeCapacity'].value)
        randomNet_tag.setAttribute('maxEdgeCapacity', pureRandomTagAtts.
                                   attributes['maxEdgeCapacity'].value)
    root.appendChild(randomNet_tag)
    request_tag = docOut.createElement("requests")
    request_tag.setAttribute('id', `1.2`)
    request_tag.setAttribute('numberOfRequests', minReqNum)
    request_tag.setAttribute('minNumberNodes', minVirNode)
    request_tag.setAttribute('maxNumberNodes', maxVirNode)
    request_tag.setAttribute('edgeProbability', virEdgeProbability)
    request_tag.setAttribute('minNodeCapacity', minVirNodeCapacity)
    request_tag.setAttribute('maxNodeCapacity', maxVirNodeCapacity)
    request_tag.setAttribute('minEdgeCapacity', minVirEdgeCapacity)
    request_tag.setAttribute('maxEdgeCapacity', maxVirEdgeCapacity)
    request_tag.setAttribute('minEdgeDelay', minVirEdgeDelay)
    request_tag.setAttribute('maxEdgeDelay', maxVirEdgeDelay)
    request_tag.setAttribute('minNumberCandidates', minSubCandidates)
    request_tag.setAttribute('maxNumberCandidates', maxSubCandidates)
    request_tag.setAttribute('minNumberCustomers', minCustomer)
    request_tag.setAttribute('maxNumberCustomers', maxCustomer)
    randomNet_tag.appendChild( request_tag )

    outFile = open(outputFileName +'.xml',"w")
    print("\nHere is your generated Modified Virtual Request but Default "
          "Substrate Network VNE Parameter File ...\n")
    docOut.writexml(sys.stdout, "   ", "\t", "\n", "utf-8")
    docOut.writexml( outFile , "   ", "\t", "\n", "utf-8")
    print("\nYour Modified Virtual Request but Default Substrate Network VNE "
          "Parameter File has written to {}".format(outputFileName + '.xml'))


def main(argv): 
    parser = argparse.ArgumentParser()
    parser.add_argument('-o', action='store',
                        dest='userParamFile',
                        metavar='graphParameter',
                        default=None,
                        required=False,
                        help='Fully modifid Parameter file by user'
                             ' for graph construction')
    parser.add_argument('-i', action='store',
                        dest='defaultParamFile',
                        metavar='graphParameter',
                        default=None,
                        required=False,
                        help='Default VNE Parameter file' )
    parser.add_argument('-b', action='store_true',
                        dest='bothFlag',                                
                        default=None,
                        required=False,
                        help='Flag used for indicating both Parameter '
                             'is Modified by User')
    parser.add_argument('-n', action='store_true',
                        dest='netFlag',
                        default=None,
                        required=False,
                        help='Flag used for indicating only Network Parameter'
                             ' is Modified by User')
    parser.add_argument('-r', action='store_true',
                        dest='virReqFlag',
                        default=None,
                        required=False,
                        help='Flag used for indicating only Virtual Request '
                             'Parameter is Modified by User')
    global args
    args = parser.parse_args()
    if args.bothFlag:
        createVNEParam_fullMod_userDefined(args.userParamFile)
    if args.netFlag:
        createVNEParam_netMod_userDefined(args.defaultParamFile,
                                          args.userParamFile)
    if args.virReqFlag:
        createVNEParam_reqMod_userDefined(args.defaultParamFile,
                                          args.userParamFile)

if __name__ == "__main__":
  main(sys.argv[1:])