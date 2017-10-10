import json

traces = open('5.. LDTP _reformatted_1000', 'rb')
data = json.load(traces)

request_types_list = data['request_types']
request_data_list = data['request_data']
response_data_list = data['response_data']

fw = open('LDTP_lstm_format', 'w')
for request_types in request_types_list:
	upper_index = request_types_list.index(request_types)
	request_data = request_data_list[upper_index]
	response_data = response_data_list[upper_index]
	question = ''
	answer   = ''
	for i in range(len(request_types)):
		question += request_types[i]
		if isinstance(request_data[i], list):
			temp_var = ''
			for req_data in request_data[i]:
				temp_var += req_data
			if len(temp_var) > 100:
			    temp_var = temp_var[:100]
			question += temp_var
		else:
			if len(request_data[i]) > 100:
			    question += request_data[i][:100]
			else:
			    question += request_data[i]	
		if isinstance(response_data[i], list):
			for res_data in response_data[i]:
				answer += res_data
		else:
			answer    = response_data[i]
		if len(answer) > 100:
		    answer = answer[:100]
		
		fw.write(question)
		fw.write('\n')
		fw.write(answer)
		fw.write('\n')
		
