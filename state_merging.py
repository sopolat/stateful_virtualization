#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Thu Apr 27 10:27:15 2017

@author: suleyman
"""

import graphviz as gv

import json

import functools





def add_nodes(graph, nodes):

    for n in nodes:

        if isinstance(n, tuple):

            graph.node(n[0], **n[1])

        else:

            graph.node(n)

    return graph



def add_edges(graph, edges):

    for e in edges:

        if isinstance(e[0], tuple):

            graph.edge(*e[0], **e[1])

        else:

            graph.edge(*e)

    return graph



def create_edge_list(requestsList, responses):

    edge_list = []
    j =0
    for requests in requestsList:
        source_dest = (responses[0],responses[j+1])
        label = {'label':requests[0]}
        edge_list.append((source_dest,label))
        j+=1
        for i in range(1,len(requests)):
    
            source_dest = (responses[j],responses[j+1])
    
            label = {'label':requests[i]}
    
            edge_list.append((source_dest,label))
            j+=1

    return edge_list



def create_node_list(responseList,response_list):

    node_list = []
    node_list.append('Init-0')
    i = 0
    for responses in responseList:
        for resp in responses:
    
            node_list.append(str(i))
            response_list.append(resp)
            i += 1

    return node_list

def check_path(node,edge_list):
    path=[]
    for i in range(len(edge_list)):
        for edge in edge_list:
            if(edge[0][1]==node):
                path.append(edge[1]['label'])
                node=edge[0][0]
                if(node=='Init_0'):
                    break
        if(node=='Init_0'):
            break
                
    
    return path

def merge_nodes(merge_list,node_list,edge_list,delete_node_list,delete_edge_list):
    nodeI=node_list[merge_list[0]]
    for J in merge_list:
        nodeJ=node_list[J]
        if(nodeI==nodeJ):
            continue
        for i in range(len(edge_list)):
            edge=edge_list[i]
            if(edge[0][0]==nodeJ):
                edge_list[i]=((nodeI,edge[0][1]),edge[1])
            if(edge[0][1]==nodeJ):
                delete_edge_list.append(edge)
        delete_node_list.append(nodeJ)
    return edge_list

f = open('thy_traces','rb')

data = json.load(f)



requests = data['requests']

responses = data['responses']


digraph = functools.partial(gv.Digraph, format='png')

response_list=[]

node_list = create_node_list(responses,response_list)

edge_list = create_edge_list(requests,node_list)

pta_list=[]
response_list=[]
for node in node_list:
    pta_list.append(check_path(node,edge_list))
   
delete_node_list=[]   
delete_edge_list=[]  
for i in range(len(pta_list)):
    if(node_list[i] in delete_node_list):
        continue
    merge_list=[]
    merge_list.append(i)
    for j in range(len(pta_list)):
        if(i==j):
            continue
        if(pta_list[i]==pta_list[j]):
            merge_list.append(j)
    if(len(merge_list)>1):
        merge_nodes(merge_list,node_list,edge_list,delete_node_list,delete_edge_list)
        
        
        
for i in delete_node_list:
    node_list.remove(i)
    
for i in delete_edge_list:
    edge_list.remove(i)


graph = add_edges(

    add_nodes(digraph(), node_list),

    edge_list

)
graph.render('img/traces')