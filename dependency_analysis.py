
import json
from Bio import pairwise2

def parse_traces():
    '''
    Parses the trace file.
    '''
    trace_file = open('service_traces', 'r')
    clear_trace_file = open('clear_service_traces', 'w')

    lines = trace_file.readlines()

    for line in lines:
        if not (line.startswith('POST') or line.startswith('{')):
            continue
        else:
            clear_trace_file.write(line)


def find_dependencies():
    '''
    Finds the dependencies between request types.
    '''
    # service_traces = open('clear_service_traces', 'r')

    # request_types = []
    # request_data = []
    # requests = []
    # responses = []
    # while True:
    #     request_type = service_traces.readline()
    #     request_data = service_traces.readline()
    #     response = service_traces.readline()

    #     if not request_type or not request_data or not response:
    #         break  # EOF

    #     request_types.append(request_type)
    #     request_data.append(request_data)
    #     requests.append([request_type, request_data])
    #     responses.append(response)


    traces = open('template_approach_traces','rb')
    data = json.load(traces)
    requests  = data['requests']
    responses = data['responses']
    request_types = []
    request_data  = []

    for request in requests:
        request_types.append(request.split(':')[0])
        try:
            request_data.append(request.split(':')[1])
        except:
            request_data.append('{}')
                

    print request_types
    print len(request_data)
    print len(responses)

    used = []
    groups = []
    j = 0
    for request in request_types:
        print str(j) + ' -- ' + str(request)
        indices = [i for i, x in enumerate(request_types)
                   if x == request and i not in used]
        if len(indices) > 1:
            groups.append(indices)
        used += indices
        j += 1

    print groups

    dependancy_mapping = {}
    for group in groups:
        dep_list = []
        for i in range(len(group) - 1):
            is_changed = 0
            if not responses[group[i]] == responses[group[i + 1]]:
                is_changed = 1
            start = group[i] + 1
            end = group[i + 1]
            dep_list.append(tuple(request_types[start:end], is_changed))

        dependancy_mapping[request_types[group[0]]] = dep_list

    # print dependancy[0]+ ' affects ' + dependancy[1]

    return dependancy_mapping

def difference_function():

    pairwise2.align.localxx('','')

    return True
if __name__ == "__main__":
    find_dependencies()
