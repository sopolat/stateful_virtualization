import json

OPERATION_TO_BE_TRAINED = '5.. LDTP '
TRACE_SIZE =  5

traces = open('publication_data.txt', 'rb')
data = json.load(traces)

request_types_list = data['request_types']
request_data_list = data['request_data']
response_data_list = data['response_data']

new_request_types_list= []
new_request_data_list = []
new_response_data_list= []

# fw = open('debug_file', 'w')
for request_types in request_types_list[:1000]:
	upper_index = request_types_list.index(request_types)
	request_data = request_data_list[upper_index]
	response_data = response_data_list[upper_index]
	indices = [i for i, rtype in enumerate(request_types) if rtype == OPERATION_TO_BE_TRAINED]
	for index in indices:
		# fw.write(str(request_types))
		# fw.write('\n')
		# fw.write(str(request_data))
		# fw.write('\n')
		print response_data[index]
		new_request_type = request_types[index-TRACE_SIZE+1:index+1]
		new_request_data = request_data[index-TRACE_SIZE+1:index+1]
		new_response_data = response_data[index-TRACE_SIZE+1:index+1]
		if len(new_request_type) == 0:
			continue
		new_request_types_list.append(new_request_type)
		new_request_data_list.append(new_request_data)
		new_response_data_list.append(new_response_data)

OPERATION_TO_BE_TRAINED = OPERATION_TO_BE_TRAINED.replace('/', '?')
file = open(OPERATION_TO_BE_TRAINED + '_reformatted_1000', 'w')
file.write('{')
file.write('\n\"request_types\" : ')
file.write(str(new_request_types_list).replace("\'", "\"").replace('u',''))
file.write(' ,')
file.write('\n\"request_data\" : ')
file.write(str(new_request_data_list).replace("\'", "\"").replace('u',''))
file.write(' ,')
file.write('\n\"response_data\" : ')
file.write(str(new_response_data_list).replace("\'", "\"").replace("]\"","]").replace("\"[","[").replace('u',''))
file.write('\n')
file.write('}')
file.close()
