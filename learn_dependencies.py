from sklearn.neural_network import MLPClassifier
from Bio import pairwise2
import re

BACKWARD_BOUND = 3
GAP_OPENING    = -15;
GAP_EXTENSION  = -5;
MATCH          = 5
MISMATCH       = -1;

def extract_data_points():

    '''
    Learns the dependencies between the requests using machine learning
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

        if not request_type or not request_data or not response: break 
        
        # if request_type not in request_types:
        request_types.append(request_type)
        request_datas.append(request_data)
        requests.append([request_type, request_data])
        responses.append(response)

    used = []
    groups = []
    j = 0
    for request in requests:
        # print str(j) + ' -- ' + str(request)
        #Finds the indices of the each type of request
        indices = [i for i, x in enumerate(requests) if x == request and i not in used]

        if len(indices) > 1:
            groups.append(indices)
        used += indices
        j += 1 

    unique_request_types = list(set(request_types))
    n_request_types = len(unique_request_types)


    request_to_datapoints = {}
    request_to_class_tags = {}

    for group in groups:
        datapoints = []
        class_tags = []
        for i in range(len(group)):
            datapoint = [0 for j in range(n_request_types*BACKWARD_BOUND)]
            if group[i] < 3:
                continue
            datapoint[unique_request_types.index(request_types[group[i]-3])] = 1
            datapoint[unique_request_types.index(request_types[group[i]-2]) +   n_request_types] = 1
            datapoint[unique_request_types.index(request_types[group[i]-1]) + 2*n_request_types] = 1 
            datapoints.append(datapoint)

            if i == 0:
                class_tags.append(0)
            elif not responses[group[i]] == responses[group[i-1]]:
                class_tags.append(1)
                alignment = pairwise2.align.globalms(responses[group[i]][20500:], responses[group[i-1]][20500:], MATCH, MISMATCH, GAP_OPENING, GAP_EXTENSION)[159]
                
                match_gap = r'(\-+)'
                match_iter = re.finditer(match_gap, alignment[0])
                print alignment[0]
                print alignment[1]
                print ""
                for matchObj in match_iter:
                    print alignment[0][matchObj.start():matchObj.end()]
                
                match_iter = re.finditer(match_gap, alignment[1])
                
                for matchObj in match_iter:
                    print alignment[1][matchObj.start():matchObj.end()]
                return
            else:
                class_tags.append(0)
            

        request_to_datapoints[request_types[group[0]]] = datapoints
        request_to_class_tags[request_types[group[0]]] = class_tags

    print '***********************'
    for key in request_to_datapoints:
        print key + ' --- ' + str(request_to_datapoints[key]) + ' --- ' + str(request_to_class_tags[key])


def learn_dependency_nn(X, y):
    # X = [[0, 1, 0, 0, 0, 0, 0, 0, 0, 1, 0, 0, 0, 1, 0, 0, 0, 0], [0, 1, 0, 0, 0, 0, 0, 0, 0, 1, 0, 0, 0, 1, 0, 0, 0, 0], [0, 1, 0, 0, 0, 0, 0, 0, 0, 1, 0, 0, 0, 1, 0, 0, 0, 0], [0, 1, 0, 0, 0, 0, 0, 0, 0, 1, 0, 0, 1, 0, 0, 0, 0, 0], [1, 0, 0, 0, 0, 0, 0, 0, 0, 1, 0, 0, 1, 0, 0, 0, 0, 0], [1, 0, 0, 0, 0, 0, 0, 0, 0, 1, 0, 0, 1, 0, 0, 0, 0, 0], [0, 0, 0, 1, 0, 0, 1, 0, 0, 0, 0, 0, 0, 0, 0, 1, 0, 0], [0, 0, 0, 1, 0, 0, 0, 0, 0, 0, 0, 1, 0, 0, 1, 0, 0, 0], [0, 0, 1, 0, 0, 0, 0, 0, 0, 0, 0, 1, 0, 0, 1, 0, 0, 0], [0, 0, 1, 0, 0, 0, 0, 0, 0, 0, 0, 1, 0, 0, 1, 0, 0, 0], [0, 0, 1, 0, 0, 0, 0, 0, 0, 0, 0, 1, 0, 0, 0, 0, 1, 0], [0, 0, 0, 0, 1, 0, 0, 0, 0, 0, 0, 1, 0, 0, 0, 0, 1, 0], [0, 0, 0, 0, 1, 0, 0, 0, 0, 0, 0, 1, 0, 0, 0, 0, 1, 0]]
    # y = [1, 1, 0, 1, 1, 1, 0, 0, 0, 0, 0, 0, 0]
    clf = MLPClassifier(solver='lbfgs', alpha=1e-5, hidden_layer_sizes=(2, 2), random_state=1)
    clf.fit(X, y)
    # clf.predict([0, 0, 0, 1, 0, 0, 0, 0, 0, 0, 1, 0, 0, 0, 0, 0, 0, 1])
    return clf

if __name__ == "__main__":
    extract_data_points()
