import json

OPERATION_TO_BE_TRAINED = 'QX'
TRACE_SIZE =  5

traces = open('publication_data_300', 'rb')
data = json.load(traces)

request_types_list = data['request_types']
request_data_list = data['request_data']
response_data_list = data['response_data']

# print request_types_list[1][11]
# print request_data_list[1][11]
# print response_data_list[1][11]
# print request_types_list[1][12]
# print request_data_list[1][12]
# print response_data_list[1][12]
# print request_types_list[1][13]
# print request_data_list[1][13]
# print response_data_list[1][13]
# print request_types_list[1][14]
# print request_data_list[1][14]
# print response_data_list[1][14]

new_request_types_list= []
new_request_data_list = []
new_response_data_list= []

for request_types in request_types_list[:300]:
	upper_index = request_types_list.index(request_types)
	request_data = request_data_list[upper_index]
	response_data = response_data_list[upper_index]
	indices = [i for i, rtype in enumerate(request_types) if rtype == '5.. LDTP ']#OPERATION_TO_BE_TRAINED]
	for index in indices:
		print request_data[index]
# 		new_request_type = request_types[index-TRACE_SIZE+1:index+1]
# 		new_request_data = request_data[index-TRACE_SIZE+1:index+1]
# 		new_response_data = response_data[index-TRACE_SIZE+1:index+1]
	
# 	new_request_types_list.append(new_request_type)
# 	new_request_data_list.append(new_request_data)
# 	new_response_data_list.append(new_response_data)


# file = open(OPERATION_TO_BE_TRAINED + '_reformatted_300', 'w')
# file.write('{')
# file.write('\n\"request_types\" : ')
# file.write(str(new_request_types_list).replace("\'", "\"").replace('u',''))
# file.write(' ,')
# file.write('\n\"request_data\" : ')
# file.write(str(new_request_data_list).replace("\'", "\"").replace('u',''))
# file.write(' ,')
# file.write('\n\"response_data\" : ')
# file.write(str(new_response_data_list).replace("\'", "\"").replace("]\"","]").replace("\"[","[").replace('u',''))
# file.write('\n')
# file.write('}')
# file.close()
