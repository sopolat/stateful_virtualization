import json

fr = open('ml_traces', 'rb')
fw = open('ml_traces_lstm', 'wb')

data = json.load(fr)

request_types = data['request_types']
request_data = data['request_data']
response_data = data['response_data']

for i in range(len(request_types)):
    req_type_trace = request_types[i]
    req_data_trace = request_data[i]
    res_data_trace = response_data[i]
    question = ""
    answer = ""
    for j in range(1, len(req_type_trace)):
        question += req_type_trace[j]
        question += req_data_trace[j][0]
        if j == len(req_type_trace)-1:
            answer = res_data_trace[j][0]
        else:
            question += res_data_trace[j][0]

    fw.write(question.upper())
    fw.write('\n')
    fw.write(answer.upper())
    fw.write('\n')