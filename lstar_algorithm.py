
import graphviz as gv
import json
import functools

class Edge(object):

    def __init__(self, id, name, dest, source="init", previous=-1):
        self.id = id
        self.name = name
        self.source = source
        self.dest = dest
        self.previous = previous

#CHECK THIS previousun destinationu da eklenecek conditiona
def check_nondeterminisim(edges, e):
    '''
    Checks if this edge applies nondeterminism.
    '''
    for edge in edges:
        if edge.name == e.name and edge.source == e.source and \
           edge.dest != e.dest:
            print edge.name + ' ' + e.name
            print edge.source + ' ' + e.source
            print edge.dest + ' ' + e.dest
            print str(edge.previous) + ' ' + str(e.previous)
            print '---------' 
            return True

    return False


#CHECK THIS. ONE CONDITION IS MISSING
def graph_contains(edges, e):
    '''
    Checks if this edge already there.
    '''
    for edge in edges:
        if edge.name == e.name and edge.source == e.source and \
            edge.dest == e.dest:
            return True

    return False


def progressive_learn(data):
    '''
    Implements progressive learning algorithm.
    '''
    requests_list  = data['requests']
    responses_list = data['responses']

    traces = zip(requests_list, responses_list)

    id = 0
    edges = []
    for requests, responses in traces:
        for i in range(len(requests)):

            previous = id-1

            if i != 0:
                e = Edge(
                    id, requests[i], responses[i], responses[i-1], previous)
            else:
                e = Edge(id, requests[i], responses[i])

            if graph_contains(edges, e):
                continue

            while check_nondeterminisim(edges, e):
                for edge in edges:
                    if e.previous == edge.id:
                        previous_edge = edge
                        break

                new_dest_node = previous_edge.dest + '\''
                e.source = new_dest_node
                previous_edge.dest = new_dest_node
                edges.append(e)
                e = previous_edge
                # e = Edge(id+1, previous_edge.name, new_dest_node, 
                #          previous_edge.source, previous_edge.previous)

            id += 1
            edges.append(e)

    return edges

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


def lstar_main():
    
    digraph = functools.partial(gv.Digraph, format='png')

    traces = open('traces','rb')
    data = json.load(traces)

    edges = progressive_learn(data)

    edge_list = []
    node_list = []    
    for edge in edges:
        source = edge.source
        dest = edge.dest
        label = edge.name
        if source not in node_list:
            node_list.append(source)
        if dest not in node_list:
            node_list.append(dest)
            
        source_dest = (source, dest)
        label = {'label':label}
        edge_list.append((source_dest, label))
    
    graph = add_edges(
        add_nodes(digraph(), node_list),
        edge_list
    )
    graph.render('img/lstar') 


    return True

if __name__ == "__main__":
    lstar_main()