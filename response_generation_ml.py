
'''
Response generation with machine learning. Data preperation.
'''
import numpy as np
from sklearn.neural_network import MLPClassifier, MLPRegressor
# from sklearn.ensemble import AdaBoostClassifier
import json
import sys

def one_hot_encoder(type, request_types_list, request_data_list, response_data_list,
                    request_types, request_data, response_data, unique_req_types):
    '''
    one-hot encoding function 
    '''

    request_type_encoding_dict = {}
    request_data_encoding_dict = {}
    response_data_encoding_dict = {}

    encoded_data = []
    # encoded_ouput = []
    for j in range(len(request_types)):
        req_type = request_types[j]
        req_data = request_data[j]
        res_data = response_data[j]

        part_datapoint = [0] * len(unique_req_types)
        part_datapoint[unique_req_types.index(req_type)] = 1

        # request_type_encoding_dict[req_data] = part_datapoint
        encoded_data += part_datapoint

        unique_corresponding_req_data = get_unique_data(
            req_type, request_types_list, request_data_list)
        if req_type == 'updateName':
            encoded_data += [unique_corresponding_req_data.index(req_data[0])]
        else:    
            for data in req_data:
                part_datapoint = [0] * len(unique_corresponding_req_data)
                part_datapoint[unique_corresponding_req_data.index(data)] = 1
                encoded_data += part_datapoint

        unique_corresponding_res_data = get_unique_data(
            req_type, request_types_list, response_data_list)
        for data in res_data:
            part_datapoint = [0] * len(unique_corresponding_res_data)
            part_datapoint[unique_corresponding_res_data.index(data)] = 1

            if j == len(request_types) - 1 and res_data.index(data) == 0:
                unique_corresponding_req_data = get_unique_data(
                    "updateName", request_types_list, request_data_list)
                # unique_corresponding_req_data.sort()
                # print data
                # print res_data
                # print unique_corresponding_req_data
                encoded_ouput = output_encoder(unique_corresponding_req_data, request_data, data)
            else:
                encoded_data += part_datapoint

    return encoded_data, encoded_ouput

def output_encoder(unique_corresponding_req_data, request_data, data):
    flat_request_data = [item for sublist in request_data for item in sublist]
    # encoded_output = []
    # test for only the first name. ignore phone number and surname
    # data = res_data[0]
    # for data in res_data[0]:
    # print data
    # print flat_request_data
    # print unique_corresponding_req_data
    if data in flat_request_data:
        # part_datapoint = [0] * len(unique_corresponding_req_data)
        # if data in unique_corresponding_req_data:
        #     part_datapoint[unique_corresponding_req_data.index(data)] = 1
        encoded_output = unique_corresponding_req_data.index(data)
        # encoded_output = [0] * len(flat_request_data)
        # encoded_output[flat_request_data.index(data)] = 1

    return encoded_output

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
    # print corresponding_data
    unique_corresponding_data = list(set(corresponding_data))

    return unique_corresponding_data


#######################################
############TRAINING PART##############
#######################################

traces = open('ml_traces', 'rb')
data = json.load(traces)

request_types_list = data['request_types']
request_data_list = data['request_data']
response_data_list = data['response_data']

unique_req_types = list(set(
    [req_type for request_types in request_types_list
     for req_type in request_types]))

datapoints = []
outputs = []
total_length = len(request_types_list)
max_len = 0
for i in range(total_length):
    request_types = request_types_list[i]
    request_data = request_data_list[i]
    response_data = response_data_list[i]

    # num_elem_in_list = 0
    # for k in range(len(request_types)):
    #     if request_types[k] == "service/add/" and response_data[k] == ["OK"]:
    #         num_elem_in_list += 1
    #     elif request_types[k] == "service/delete/" and response_data[k] == ["OK"]:
    #         num_elem_in_list -= 1

    # print num_elem_in_list

    datapoint, output = one_hot_encoder('train',
                                        request_types_list, request_data_list,  response_data_list,
                                        request_types, request_data, response_data, unique_req_types)
    print datapoint
    print output 
    datapoints.append(datapoint)
    outputs.append(output)
    print i

    if len(datapoint) > max_len:
        max_len = len(datapoint)

for i in range(len(datapoints)):
    datapoint_resized = datapoints[i] + [0] * (max_len - len(datapoints[i]))
    datapoints[i] = datapoint_resized

mlp = MLPRegressor(solver='lbfgs', alpha=1e-5, hidden_layer_sizes=(100, ),
                    random_state=1, activation='logistic', max_iter=1000)

# multi_target_forest = MultiOutputRegressor(mlp)
# classifier = multi_target_forest.fit(datapoints, outputs)

# print len(datapoints)
# print len(outputs)
print 'train is over. test starts here.'

outfile = file('outfile_ml', 'w')
outfile.write('Out Predicted')
outfile.write('\n')
wrong_guess_counter = 0
CROSS_VAL_SIZE = 20
for k in range(10):
    mlp.fit(datapoints[(k + 1) * CROSS_VAL_SIZE:] + datapoints[:k * CROSS_VAL_SIZE],
            outputs[(k + 1) * CROSS_VAL_SIZE:] + outputs[:k * CROSS_VAL_SIZE])
    print 'fitted'
    #######################################
    ##############TEST PART################
    #######################################

    for i in range((k * CROSS_VAL_SIZE), ((k + 1) * CROSS_VAL_SIZE)):
        datap = np.array(datapoints[i]).reshape(1, -1)
        predicted = mlp.predict(datap)
        # print outputs[i]
        # print predicted
        if outputs[i] != predicted.tolist()[0] :
            wrong_guess_counter += 1

        outfile.write(str(outputs[i]) + ' ' + str(predicted))
        outfile.write('\n')
        # print str(outputs[i])  + ' ' + str(predicted)# true response vs
        # predicted

print wrong_guess_counter
# real_out = []
# for p in predicted[0]:
#     if p > 0.08:
#         real_out.append(1)
#     else:
#         real_out.append(0)
# print '----------------'
# print outputs[-1]
# print real_out

# print predicted
