from sklearn.multioutput import MultiOutputClassifier
from sklearn.ensemble import RandomForestClassifier
import json

'''
Response generation with machine learning. Data preperation.
'''


def get_unique_data(req_type, request_types_list, data_list):

    '''
    Get unique request or response data of a given request type.
    '''
    corresponding_data = []
    for i in range(len(request_types_list)):
        request_types = request_types_list[i]
        data = data_list[i]

        indices = [k for k, item in enumerate(
            request_types) if item == req_type]

        part_corresponding_data = [
            data[index] for index in indices]
        part_corresponding_data_flat = [
            item for sublist in part_corresponding_data for item in sublist]
        corresponding_data += part_corresponding_data_flat

    unique_corresponding_data = list(set(corresponding_data))

    return unique_corresponding_data



traces = open('ml_traces', 'rb')
data = json.load(traces)
request_types_list = data['request_types'][:-1]
request_data_list  = data['request_data'][:-1]
response_data_list = data['response_data'][:-1]

unique_req_types = list(set(
    [req_type for request_types in request_types_list for req_type in request_types]))

datapoints = []
outputs = []

for i in range(len(request_types_list)):
    datapoint = []
    output = []
    request_types = request_types_list[i]
    request_data  = request_data_list[i]
    response_data = response_data_list[i]
    for j in range(len(request_types)):
        req_type = request_types[j]
        req_data = request_data[j]
        res_data = response_data[j]

        part_datapoint = [0 for k in range(len(unique_req_types))]
        part_datapoint[unique_req_types.index(req_type)] = 1

        datapoint += part_datapoint

        unique_corresponding_req_data = get_unique_data(
            req_type, request_types_list, request_data_list)
        for data in req_data:
            part_datapoint = [0 for k in range(
                len(unique_corresponding_req_data))]
            part_datapoint[unique_corresponding_req_data.index(data)] = 1
            datapoint += part_datapoint

        unique_corresponding_res_data = get_unique_data(
            req_type, request_types_list, response_data_list)
        for data in res_data:
            part_datapoint = [0 for k in range(
                len(unique_corresponding_res_data))]
            part_datapoint[unique_corresponding_res_data.index(data)] = 1

            if j == len(request_types) - 1:
                output = part_datapoint
            else:
                datapoint += part_datapoint


    datapoints.append(datapoint)
    outputs.append(output)

forest = RandomForestClassifier(n_estimators=10)
multi_target_forest = MultiOutputClassifier(forest)
classifier = multi_target_forest.fit(datapoints, outputs)

traces = open('ml_traces', 'rb')
data = json.load(traces)
request_types_list = [data['request_types'][-1]]
request_data_list  = [data['request_data'][-1]]
response_data_list = [data['response_data'][-1]]

datapoints = []
outputs = []

for i in range(len(request_types_list)):
    datapoint = []
    output = []
    request_types = request_types_list[i]
    request_data  = request_data_list[i]
    response_data = response_data_list[i]
    for j in range(len(request_types)):
        req_type = request_types[j]
        req_data = request_data[j]
        res_data = response_data[j]

        part_datapoint = [0 for k in range(len(unique_req_types))]
        part_datapoint[unique_req_types.index(req_type)] = 1

        datapoint += part_datapoint

        unique_corresponding_req_data = get_unique_data(
            req_type, request_types_list, request_data_list)
        for data in req_data:
            part_datapoint = [0 for k in range(
                len(unique_corresponding_req_data))]
            part_datapoint[unique_corresponding_req_data.index(data)] = 1
            datapoint += part_datapoint

        unique_corresponding_res_data = get_unique_data(
            req_type, request_types_list, response_data_list)
        for data in res_data:
            part_datapoint = [0 for k in range(
                len(unique_corresponding_res_data))]
            part_datapoint[unique_corresponding_res_data.index(data)] = 1

            if j == len(request_types) - 1:
                output = part_datapoint
            else:
                datapoint += part_datapoint


    datapoints.append(datapoint)
    outputs.append(output)

print '------------------'
classifier.predict(datapoints)

