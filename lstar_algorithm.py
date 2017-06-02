
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
        if e.source == 'init':
            continue
        if edge.name == e.name and edge.source == e.source and \
           edge.dest != e.dest:
            print edge.name + ' ' + e.name
            print edge.source + ' ' + e.source
            print edge.dest + ' ' + e.dest
            print str(edges[edge.previous].name) + ' ' + str(edges[e.previous].name)
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

            return edge.id

    return -1


def progressive_learn(requests_list, responses_list):
    '''
    Implements progressive learning algorithm.
    '''


    traces = zip(requests_list[:30], responses_list[:30])

    id = 0
    skipId = -1
    edges = []
    for requests, responses in traces:
        for i in range(len(requests)):

            previous = id - 1

            if skipId != -1:
                previous = skipId
                skipId = -1

            if i != 0:
                e = Edge(
                    id, requests[i], responses[i], responses[i-1], previous)
            else:
                e = Edge(id, requests[i], responses[i])

            while check_nondeterminisim(edges, e):
                all_destinations = []
                for edge in edges:
                    if e.previous == edge.id:
                        previous_edge = edge

                    all_destinations.append(edge.dest)

                new_dest_node = previous_edge.dest + '\''

                while new_dest_node in all_destinations:
                    new_dest_node += '\''

                id += 1
                e.source = new_dest_node
                e.previous = id

                new_edge = Edge(id , previous_edge.name, new_dest_node, 
                         previous_edge.source, previous_edge.previous)

                edges.append(e)

                e = new_edge

            if graph_contains(edges, e) != -1:
                skipId = graph_contains(edges, e)
                continue


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

    traces = open('thy_31_traces','rb')
    data = json.load(traces)
    requests_list  = data['requests']
    responses_list = data['responses']

    # requests_list, responses_list = parse_service_traces()

    responses_list = response_enumeration(responses_list)

    edges = progressive_learn(requests_list, responses_list)

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

def parse_service_traces():
    service_traces = open('clear_service_traces', 'r')

    request_types = []
    request_datas = []
    requests = []
    responses = []

    cnt = 1
    response_enum_dict = {}
    while True:
        request_type = service_traces.readline()
        request_data = service_traces.readline()
        response = service_traces.readline()

        if not request_type or not request_data or not response: break 
        
        # if request_type not in request_types:
        request_types.append(request_type)
        request_datas.append(request_data)
        requests.append(request_type)

        if response_enum_dict.get(response,0) == 0:
            response_enum_dict[response] = cnt 
            cnt += 1

        responses.append(str(response_enum_dict[response]))

        print responses

    return [requests], [responses]

def response_enumeration(responses_list):

    cnt = 1
    response_enum_dict = {}
    enumerated_responses_list = []
    for responses in responses_list:

        enumerated_responses = []

        for response in responses:
            if response_enum_dict.get(response,0) == 0:
                response_enum_dict[response] = cnt 
                cnt += 1

            enumerated_responses.append(str(response_enum_dict[response]))

        enumerated_responses_list.append(enumerated_responses)
    
    return enumerated_responses_list


if __name__ == "__main__":
    lstar_main()