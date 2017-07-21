
'''
Response generation with machine learning. Data preperation.
'''
import numpy as np
from sklearn.neural_network import MLPClassifier, MLPRegressor
from sklearn.neighbors import KNeighborsClassifier
from sklearn.svm import SVC
from sklearn.gaussian_process import GaussianProcessClassifier
from sklearn.gaussian_process.kernels import RBF
from sklearn.tree import DecisionTreeClassifier
from sklearn.ensemble import RandomForestClassifier, AdaBoostClassifier
from sklearn.naive_bayes import GaussianNB
from sklearn.discriminant_analysis import QuadraticDiscriminantAnalysis

import json
import sys
import os 

def pre_process_data(request_types_list, request_data_list, response_data_list):
    '''
    Mines needed information from the data
    '''
    unique_req_types = list(set(
        [req_type for request_types in request_types_list
         for req_type in request_types]))

    req_type_datapoint_dict = {}
    for req_type in unique_req_types:
        # part_datapoint = [0] * len(unique_req_types)
        # part_datapoint[unique_req_types.index(req_type)] = -1
        part_datapoint = [unique_req_types.index(req_type) + 1]
        req_type_datapoint_dict[req_type] = part_datapoint

    req_data_datapoint_dict = {}
    max_req_data_len = 0
    for req_type in unique_req_types:
        unique_corresponding_req_data = get_unique_data(
            req_type, request_types_list, request_data_list)
        if len(unique_corresponding_req_data) > max_req_data_len:
            max_req_data_len = len(unique_corresponding_req_data)
        for data in unique_corresponding_req_data:
            part_datapoint = [0] * len(unique_corresponding_req_data)
            part_datapoint[unique_corresponding_req_data.index(data)] = -1
            req_data_datapoint_dict[(req_type, str(data))] = part_datapoint

    for value in req_data_datapoint_dict.values():
        value += (max_req_data_len - len(value)) * [0]

    res_data_datapoint_dict = {}
    max_res_data_len = 0
    for req_type in unique_req_types:
        unique_corresponding_res_data = get_unique_data(
            req_type, request_types_list, response_data_list)
        unique_corresponding_res_data += [str([])]
        if len(unique_corresponding_res_data) > max_res_data_len:
            max_res_data_len = len(unique_corresponding_res_data)
        for data in unique_corresponding_res_data:
            part_datapoint = [0] * len(unique_corresponding_res_data)
            part_datapoint[unique_corresponding_res_data.index(data)] = -1
            res_data_datapoint_dict[(req_type, str(data))] = part_datapoint

    for value in res_data_datapoint_dict.values():

        value += (max_res_data_len - len(value)) * [0]

    # print req_type_datapoint_dict
    # print ''
    # print req_data_datapoint_dict
    # print ''
    # print res_data_datapoint_dict
    return req_type_datapoint_dict, req_data_datapoint_dict, res_data_datapoint_dict, max_req_data_len, max_res_data_len


fw = open('debug_datapoint', 'w')


def one_hot_encoder(req_type_datapoint_dict,
        req_data_datapoint_dict, res_data_datapoint_dict, max_req_data_len,
        max_res_data_len, request_types, request_data, response_data):
    '''
    one-hot encoding function 
    '''
    encoded_data = []
    # encoded_ouput = []
    for j in range(len(request_types)):
        req_type = request_types[j]
        req_data = request_data[j]
        res_data = response_data[j]

        part_datapoint = req_type_datapoint_dict[req_type]
        encoded_data += part_datapoint

        # print 'REQ TYPE ' + str(j) + ':'
        # print part_datapoint
        fw.write(req_type)
        fw.write(str(part_datapoint))
        fw.write(str(len(encoded_data)))
        fw.write('-')
        # for data in req_data:
        part_datapoint = req_data_datapoint_dict[(req_type, str(req_data))]
        encoded_data += part_datapoint
        # print 'REQ DATA ' + str(j)
        # print part_datapoint

        fw.write(str(part_datapoint))
        fw.write(str(len(encoded_data)))
        fw.write('-')

        # print res_data
        # for data in res_data:

        part_datapoint = res_data_datapoint_dict[(req_type, str(res_data))]
        if j == len(request_types) - 1:
            encoded_output = request_types.count('updateName')
            fw.write(str(encoded_output))
        else:
            encoded_data += part_datapoint

        # print 'RES DATA ' + str(j)
        # print part_datapoint

        # if res_data == []:
        #     encoded_data += part_datapoint
        #     part_datapoint = res_data_datapoint_dict[(req_type, str([]))]
            fw.write(str(part_datapoint))
        fw.write(str(len(encoded_data)))
        fw.write(' ')

    return encoded_data, encoded_output

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
        # part_corresponding_data_flat = [
        #     item for sublist in part_corresponding_data for item in sublist]
        corresponding_data += part_corresponding_data

    if isinstance(corresponding_data[0], list):
        # unique_corresponding_data = [list(x) for x in set(
        #     tuple(x) for x in corresponding_data)]
        # print corresponding_data
        unique_corresponding_data = []
        for x in corresponding_data:
            if x not in unique_corresponding_data:
                unique_corresponding_data.append(x)
        # print unique_corresponding_data
    else:
        unique_corresponding_data = list(set(corresponding_data))
    # print unique_corresponding_data
    return unique_corresponding_data


#######################################
############TRAINING PART##############
#######################################
cmd = 'python2 data_creator2.py ' + sys.argv[1] + ' ' + sys.argv[2]
os.system(cmd)

print 'data created'
print ''
traces = open('ml_traces', 'rb')
data = json.load(traces)

request_types_list = data['request_types']
request_data_list = data['request_data']
response_data_list = data['response_data']


req_type_datapoint_dict, req_data_datapoint_dict, \
res_data_datapoint_dict, max_req_data_len, max_res_data_len = \
pre_process_data(request_types_list, request_data_list, response_data_list)

# unique_req_types = list(set(
#     [req_type for request_types in request_types_list
#      for req_type in request_types]))

datapoints = []
outputs = []
total_length = len(request_types_list)

for i in range(total_length):
    request_types = request_types_list[i]
    request_data = request_data_list[i]
    response_data = response_data_list[i]

    datapoint, output = one_hot_encoder(req_type_datapoint_dict,
                            req_data_datapoint_dict, res_data_datapoint_dict, max_req_data_len,
                            max_res_data_len, request_types, request_data, response_data)


    fw.write('\n')
    datapoints.append(datapoint)
    outputs.append(output)
    print i

fw.close()  

names = ["Nearest Neighbors", "Linear SVM", "RBF SVM",  # "Neural Net",
         "Gaussian Process",
         "Decision Tree", "Random Forest", "AdaBoost",
         "Naive Bayes", "QDA"]
classifiers = [
    KNeighborsClassifier(5),
    SVC(kernel="linear", C=0.025),
    SVC(gamma=2, C=1),
    # MLPClassifier(alpha=1),
    GaussianProcessClassifier(1.0 * RBF(1.0), warm_start=True),
    DecisionTreeClassifier(max_depth=5),
    RandomForestClassifier(max_depth=5, n_estimators=10, max_features=1),
    AdaBoostClassifier(),
    GaussianNB(),
    QuadraticDiscriminantAnalysis()]

print 'train is over. test starts here.'

for name, clf in zip(names, classifiers):

    CROSS_VAL_SIZE = int(sys.argv[3])
    outfile = file('outfile_ml' + name, 'w')
    outfile.write('Out Predicted')
    outfile.write('\n')
    wrong_guess_counter = 0

    print name
    for k in range(total_length / CROSS_VAL_SIZE):
        clf.fit(datapoints[(k + 1) * CROSS_VAL_SIZE:] + datapoints[:k * CROSS_VAL_SIZE],
                outputs[(k + 1) * CROSS_VAL_SIZE:] + outputs[:k * CROSS_VAL_SIZE])
        print 'fitted'
        #######################################
        ##############TEST PART################
        #######################################

        for i in range((k * CROSS_VAL_SIZE), ((k + 1) * CROSS_VAL_SIZE)):
            datap = np.array(datapoints[i]).reshape(1, -1)
            predicted = clf.predict(datap)
            # print outputs[i]
            # print predicted
            if outputs[i] != predicted.tolist()[0] :
                wrong_guess_counter += 1

            outfile.write(str(outputs[i]) + ' ' + str(predicted))
            outfile.write('\n')
            # print str(outputs[i])  + ' ' + str(predicted)# true response vs
            # predicted

        outfile.write('\n')
        outfile.write(str(wrong_guess_counter))
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
