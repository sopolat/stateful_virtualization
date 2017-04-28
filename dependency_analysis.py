
def parse_traces():

    '''
    Parses the trace file.
    '''
    trace_file = open('service_traces','r')
    clear_trace_file = open('clear_service_traces','w')

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
    service_traces = open('clear_service_traces', 'r')

    request_types = []
    request_datas = []
    requests = []
    responses = []
    while True:
        request_type = service_traces.readline()
        request_data = service_traces.readline()
        response = service_traces.readline()

        if not request_type or not request_data or not response: break  # EOF

        request_types.append(request_type)
        request_datas.append(request_data)
        requests.append([request_type, request_data])
        responses.append(response)

    print len(request_types)
    print len(request_datas)
    print len(responses)

    used = []
    groups = []
    j = 0
    for request in requests:
        print str(j) + ' -- ' + str(request)
        indices = [i for i, x in enumerate(requests) 
                    if x == request and i not in used]
        if len(indices) > 1:
            groups.append(indices)
        used += indices
        j += 1 

    print groups
    print request_types[18]
    print request_types[19:20]
    dependancy_mapping = {}
    for group in groups:
        for i in range(len(group)-1):
            if not responses[group[i]] == responses[group[i+1]]:
                start = group[i]+1
                end   = group[i+1]
                print group
                print str(start) + ' ' + str(end)
                print tuple(request_types[start:end])
                print request_types[group[i]]
                dependancy_mapping[tuple(request_types[start:end])] = request_types[group[i]]

    for key in dependancy_mapping:
        print str(key) + ' affects ' + str(dependancy_mapping[key])