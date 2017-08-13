import json

traces = open('ml_traces', 'rb')
data = json.load(traces)

request_types_list = data['request_types']
request_data_list = data['request_data']
response_data_list = data['response_data']

lstm_format_data_file = open('lstm_format_data_file', 'w')
 
for request_types, request_data, response_data in zip(request_types_list, request_data_list, response_data_list):
	input_trace = ''
	output_trace = '' 
	for req_type, req_data, res_data in zip(request_types, request_data, response_data):
		input_trace += req_type
		input_trace += req_data[0]
		output_trace += res_data[0]
		lstm_format_data_file.write(input_trace)
		lstm_format_data_file.write('\n')
		lstm_format_data_file.write(output_trace)
		lstm_format_data_file.write('\n')
		input_trace += output_trace
		output_trace = '' 