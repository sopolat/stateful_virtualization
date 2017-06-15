
'''
Response generation with machine learning. Data preperation.
'''

traces = open('traces', 'rb')
data = json.load(traces)
request_types_list = data['request_types']
request_data_list = data['request_data']
response_list = data['responses']

unique_req_types = list(set(
    [req_type for request_types in request_types_list for req_type in request_types]))

datapoints = []
outputs = []

for i in range(len(request_types_list)):
    datapoint = []
    output = []
    request_types = request_types_list[i]
    request_data = request_data_list[i]
    for j in range(len(request_types)):
        req_type = request_types[j]
        req_data = request_data[j]

        part_datapoint = [0 for k in range(len(unique_req_types))]
        part_datapoint[unique_req_types.index(req_type)] = 1

        datapoint += part_datapoint

        unique_corresponding_req_data = get_unique_data(
            req_type, request_types_list, request_data_list)
        for data in req_data:
            part_datapoint = [0 for k in range(
                len(unique_corresponding_req_data))]
            part_datapoint[unique_corresponding_req_data.index(data)] = 1
            if j == len(request_types) - 1:
                output += part_datapoint
            else:
                datapoint += part_datapoint

    datapoints.append(datapoint)
    outputs.append(output)


def get_unique_data(req_type, request_types_list, request_data_list):

	'''
	Get uniwue response data of a given request.
	'''
    corresponding_req_data = []
    for i in range(len(request_types_list)):
        request_types = request_types_list[i]
        request_data = request_data_list[i]

        indices = [k for k, item in enumerate(
            request_types) if item == req_type]

        part_corresponding_req_data = [
            request_data[index] for index in indices]
        part_corresponding_req_data_flat = [
            item for sublist in part_corresponding_req_data for item in sublist]
        corresponding_req_data += part_corresponding_req_data_flat

    unique_corresponding_req_data = list(set(corresponding_req_data))

    return unique_corresponding_req_data
