
'''
Response generation with machine learning. Data preperation.
'''
import numpy as np
# from sklearn.neural_network import MLPClassifier, MLPRegressor
from sklearn.neighbors import KNeighborsClassifier
from sklearn.svm import SVC
from sklearn.gaussian_process import GaussianProcessClassifier
from sklearn.gaussian_process.kernels import RBF
from sklearn.tree import DecisionTreeClassifier
from sklearn.ensemble import RandomForestClassifier, AdaBoostClassifier
from sklearn.naive_bayes import GaussianNB
from sklearn.discriminant_analysis import QuadraticDiscriminantAnalysis
from sklearn.decomposition import PCA

import json
import sys
import os
from bs4 import BeautifulSoup
from collections import defaultdict


#global variables
operation_to_be_trained = sys.argv[1]
trace_size = int(sys.argv[2])


req_data_dict = defaultdict(list)
res_data_dict = defaultdict(list)


bank_file = open('bank_data.xml', 'rb')
reformetted_file = open('reformetted_bank_data', 'w')

bank_lines = bank_file.readlines()
flag = 'req'
account_dict = {}
for line in bank_lines:
    line = line.strip()
    y=BeautifulSoup(line, 'lxml')
    if flag == 'req':
        if 'getAccount ' in line:
            reformetted_file.write('getaccount ')
            acc_id = y.accountid.text
            reformetted_file.write(acc_id + ' / ')
            if [acc_id] not in req_data_dict['getaccount']:
                req_data_dict['getaccount'].append([acc_id])
        if 'getNewToken ' in line:
            reformetted_file.write('getnewtoken ')
            reformetted_file.write('empty / ')  
            if ['empty'] not in  req_data_dict['getnewtoken']:
                req_data_dict['getnewtoken'].append(['empty'])
        if 'depositMoney ' in line:
            reformetted_file.write('deposit ')
            reformetted_file.write(y.accountid.text + ' ' + y.amount.text + ' / ')   
            if [y.accountid.text, y.amount.text] not in req_data_dict['deposit']:
                req_data_dict['deposit'].append([y.accountid.text, y.amount.text])
        if 'withdrawMoney ' in line:
            reformetted_file.write('withdraw ')
            reformetted_file.write(y.accountid.text + ' ' + y.amount.text + ' / ')  
            if [y.accountid.text, y.amount.text] not in req_data_dict['withdraw']:
                req_data_dict['withdraw'].append([y.accountid.text, y.amount.text])
        if 'getTransactions ' in line:
            reformetted_file.write('gettransactions ')
            reformetted_file.write(y.accountid.text + ' / ') 
            if [y.accountid.text] not in req_data_dict['gettransactions']:
                req_data_dict['gettransactions'].append([y.accountid.text])

        flag = 'res'
    else:
        if 'getAccountResponse' in line:
            try:
                reformetted_file.write(account_dict[acc_id][0] + ' ' + account_dict[acc_id][1] + '\n')
            except:
                reformetted_file.write(y.fname.text + ' ' + y.lname.text + '\n')
                account_dict[acc_id] = (y.fname.text, y.lname.text)
            if acc_id not in res_data_dict['getaccount']:
                res_data_dict['getaccount'].append([y.fname.text, y.lname.text])
        if 'getNewTokenResponse' in line:
            reformetted_file.write(y.returns.text + '\n')
            if [y.returns.text] not in res_data_dict['getnewtoken']:
                res_data_dict['getnewtoken'].append([y.returns.text])
        if 'depositMoneyResponse' in line:
            reformetted_file.write(y.returns.text + '\n')
            if [y.returns.text] not in res_data_dict['deposit']:
                res_data_dict['deposit'].append([y.returns.text])
        if 'withdrawMoneyResponse' in line:
            reformetted_file.write(y.returns.text + '\n')
            if [y.returns.text] not in res_data_dict['withdraw']:
                res_data_dict['withdraw'].append([y.returns.text])
        if 'getTransactionsResponse' in line:
            reformetted_file.write(y.transid.text + ' ' + y.fromaccount.text + ' ' + y.toaccount.text + '\n')
            if [y.transid.text, y.fromaccount.text, y.toaccount.text] not in res_data_dict['gettransactions']:
                res_data_dict['gettransactions'].append([y.transid.text, y.fromaccount.text, y.toaccount.text])


        flag = 'req'

def arrange_trace_window(event_list, param_list, resp_list, event, params, resp):
    
    event_list.append(event)
    param_list.append(params)
    resp_list.append(resp)

    if len(event_list) > trace_size:
        del event_list[0]

    if len(param_list) > trace_size:
        del param_list[0]

    if len(resp_list) > trace_size:
        del resp_list[0]

    return event_list, param_list, resp_list


fw = open('debug_datapoint', 'w')

req_types = [
        'getaccount',
        'getnewtoken',
        'deposit',
        'withdraw',
        'gettransactions']

most_diverse_req = 0
most_diverse_res = 0

for req in req_types:
    if len(res_data_dict[req]) > most_diverse_res:
        most_diverse_res = len(res_data_dict[req])

    if len(req_data_dict[req]) > most_diverse_req:
        most_diverse_req = len(req_data_dict[req])


reformetted_file = open('reformetted_bank_data', 'rb')

datapoints = []
outputs    = []
event_list = []
param_list = []
resp_list  = []
datapoints = []
outputs = []
next_event_flag = False
while True:
    line = reformetted_file.readline()
    if not line: break  # EOF
    # if 'trace' in line:
    #     #remove last datapoint. becaues there is no next event
    #     if next_event_flag:
    #         del datapoints[-1]
    #         next_event_flag = False
    #     event_list = []
    #     param_list = []
    #     continue
    line = line.strip()
    line_splitted = line.split(' / ')
    request_parts = line_splitted[0].split(' ')
    op_type = request_parts[0]
    params = request_parts[1:]
    resp = line_splitted[1].split(' ')


    event_list, param_list, resp_list = arrange_trace_window(event_list, param_list, resp_list, op_type, params, resp)

    if op_type == operation_to_be_trained and len(event_list)== trace_size:
        datapoint = []
        i = 0
        for event, params, resp in zip(event_list, param_list, resp_list):
            i += 1
            event_encoded = [0] * len(req_types)
            event_encoded[req_types.index(event)] = -1
            datapoint += event_encoded
            
            part_datapoint = [0] * most_diverse_req #len(req_data_dict[event])
            part_datapoint[req_data_dict[event].index(params)] = -1
            datapoint += part_datapoint
            print event
            if i == trace_size:
                output = [0] * len(res_data_dict[event])
                output[res_data_dict[event].index(resp)] = -1
            else:
                part_datapoint = [0] * most_diverse_res #len(res_data_dict[event])
                part_datapoint[res_data_dict[event].index(resp)] = -1
                datapoint += part_datapoint

        fw.write(str(datapoint))
        fw.write('---')
        fw.write(str(output))
        fw.write('\n')

        outputs.append(output)
        datapoints.append(datapoint)

total_length = len(datapoints)

#######################################
############TRAINING PART##############
#######################################


# datapoints = list(PCA(n_components=100).fit_transform(datapoints))
# print 'data reduced (PCA)'

names = [
        "Decision Tree", 
         # "Linear SVM",   
         # "Neural Net", #"Nearest Neighbors", 
         # "RBF SVM", 
         # "Random Forest", #"Naive Bayes", "QDA"
         # "AdaBoost",
         # "Gaussian Process"
         ]
classifiers = [
    # KNeighborsClassifier(3),
    DecisionTreeClassifier(max_depth=50),
    # SVC(kernel="linear", C=0.025),
    # SVC(gamma=2, C=1),
    # MLPClassifier(alpha=1),
    # GaussianProcessClassifier(1.0 * RBF(1.0), warm_start=True),
    # RandomForestClassifier(max_depth=5, n_estimators=10, max_features=1),
    # AdaBoostClassifier(),
    # GaussianNB(),
    # QuadraticDiscriminantAnalysis()
    ]


print 'train is over. test starts here.'
for name, clf in zip(names, classifiers):
    # clf = MLPClassifier(solver='lbfgs', alpha=1e-5, hidden_layer_sizes=(100, ),
    #                     random_state=1, activation='logistic', max_iter=1000)

    # clf = AdaBoostClassifier()
    # multi_target_forest = MultiOutputRegressor(mlp)
    # classifier = multi_target_forest.fit(datapoints, outputs)

    print name
    # Read cross val size from the user input
    CROSS_VAL_SIZE = int(sys.argv[3])
    outfile = file('outfile_ml' + name, 'w')
    outfile.write('Out Predicted')
    outfile.write('\n')
    wrong_guess_counter = 0
    # try:
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
            if outputs[i] != predicted.tolist()[0]:
                wrong_guess_counter += 1

            outfile.write(str(outputs[i]) + ' ' + str(predicted))
            outfile.write('\n')
            # print str(outputs[i])  + ' ' + str(predicted)# true response vs
            # predicted

    outfile.write('\n')
    outfile.write(str(wrong_guess_counter))
    print wrong_guess_counter

    # except:
    #     outfile.write('Error Happened.')
    outfile.close()