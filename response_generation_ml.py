
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
from sklearn.decomposition import PCA

import json
import sys
import os

######################
#Sample command
#python critical 5 100
######################


#global variables
operation_to_be_trained = sys.argv[1]
trace_size = int(sys.argv[2])




def arrange_trace_window(event_list, param_list, event, water_level, methane_level, is_pump):
    
    event_list.append(event)
    param_list.append([water_level, methane_level, is_pump])
    if len(event_list) > trace_size:
        del event_list[0]

    if len(param_list) > trace_size:
        del param_list[0]

    return event_list, param_list

#######################################
############TRAINING PART##############
#######################################

#Data is ready. Taken from Walkinshaw
mine_pump_data = open('mine_pump', 'rb')


fw = open('debug_datapoint', 'w')

event_types = ['highwater',
'switch_pump_on',
'turn_on',
'critical',
'switch_pump_off',
'turn_off',
'not_critical',
'low_water']

event_list = []
param_list = []
datapoints = []
outputs = []
next_event_flag = False
while True:
    line = mine_pump_data.readline()
    if not line: break  # EOF
    if 'trace' in line:
        #remove last datapoint. becaues there is no next event
        if next_event_flag:
            del datapoints[-1]
            next_event_flag = False
        event_list = []
        param_list = []
        continue
    line = line.strip()
    line_splitted = line.split(' ')
    event = line_splitted[0]
    water_level = float(line_splitted[1])
    methane_level = float(line_splitted[2])
    
    if line_splitted[3] == 'true':
        is_pump = 1 
    else:
        is_pump = 0

    if next_event_flag:
        # output_encoded = [0] * len(event_types)
        # output_encoded[event_types.index(event)] = -1
        # outputs.append(output_encoded)
        outputs.append(event_types.index(event))
        fw.write(str(outputs))
        fw.write('\n')
        next_event_flag = False

    event_list, param_list = arrange_trace_window(event_list, param_list, event, water_level, methane_level, is_pump)

    if event == operation_to_be_trained and len(event_list)== trace_size:
        datapoint = []
        next_event_flag = True
        for event, params in zip(event_list, param_list):
            event_encoded = [0] * len(event_types)
            event_encoded[event_types.index(event)] = -1
            datapoint += event_encoded
            for param in params:
                datapoint += [param]
        fw.write(str(datapoint))
        datapoints.append(datapoint)

# exit()      


fw.close()

# Dimensionality reduction
# datapoints = list(PCA(n_components=100).fit_transform(datapoints))
# print 'data reduced (PCA)'

names = [
        "Decision Tree", 
         "Linear SVM",  # 
         # "Neural Net", #"Nearest Neighbors", 
         # "RBF SVM", 
         # "Random Forest", #"Naive Bayes", "QDA"
         "AdaBoost",
         # "Gaussian Process"
         ]
classifiers = [
    # KNeighborsClassifier(3),
    DecisionTreeClassifier(max_depth=18),
    SVC(kernel="linear", C=0.005),
    # SVC(gamma=2, C=1),
    # MLPClassifier(alpha=1),
    # GaussianProcessClassifier(1.0 * RBF(1.0), warm_start=True),
    # RandomForestClassifier(max_depth=5, n_estimators=10, max_features=1),
    AdaBoostClassifier(),
    # GaussianNB(),
    # QuadraticDiscriminantAnalysis()
    ]

total_length = len(datapoints)
kfold = int(sys.argv[3])
CROSS_VAL_SIZE = int(total_length / kfold)

print len(datapoints)
print len(outputs)
print CROSS_VAL_SIZE

print 'train is over. test starts here.'
for name, clf in zip(names, classifiers):

    print name
    # Read cross val size from the user input
    outfile = file('outfile_ml' + name, 'w')
    outfile.write('Out Predicted')
    outfile.write('\n')
    wrong_guess_counter = 0
    # try:
    for k in range(kfold):
        clf.fit(datapoints[(k + 1) * CROSS_VAL_SIZE:] + datapoints[:k * CROSS_VAL_SIZE],
                outputs[(k + 1) * CROSS_VAL_SIZE:] + outputs[:k * CROSS_VAL_SIZE])
        print 'fitted'

        #######################################
        ##############TEST PART################
        #######################################

        for i in range((k * CROSS_VAL_SIZE), ((k + 1) * CROSS_VAL_SIZE)):
            datap = np.array(datapoints[i]).reshape(1, -1)
            predicted = clf.predict(datap)

            if outputs[i] != predicted.tolist()[0]:
                wrong_guess_counter += 1

            outfile.write(str(outputs[i]) + ' ' + str(predicted))
            outfile.write('\n')

    outfile.write('\n')
    outfile.write(str(wrong_guess_counter))
    print wrong_guess_counter

    # except:
    #     outfile.write('Error Happened.')
    outfile.close()