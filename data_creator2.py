# -*- coding: utf-8 -*-
"""
Created on Fri Jun 09 10:52:54 2017

@author: sopolat
"""

import names
import random
import string
import sys

funs=[15,10,28,44,50,3,30,33]
loginTokens = {}
secure_random = random.SystemRandom()
#for k in range(5):
#    data = {}
#    data["name"] = names.get_first_name()
#    data["surname"] = names.get_last_name()
#    data["tel"] = "054" + \
#        "".join(secure_random.choice(string.digits) for _ in range(8))
#    loginTokens["".join(secure_random.choice(
#        string.ascii_uppercase + string.digits) for _ in range(5))] = data
    
typeList = []
reqList = []
resList = []
for i in range(int(sys.argv[1])):
    requestTypes = []
    requests = []
    responses = []
    loginId = "bos"
    # loginAs
#    idOf = "".join(secure_random.choice(loginTokens.keys()))
#    requests.append("loginAs:" + idOf)
#    responses.append("OK")
#    loginId = idOf
#    
    # create user
    idOf = "".join(secure_random.choice(
    string.ascii_uppercase + string.digits) for _ in range(5))
    request =[]
    request.append("")
    response = []
    response.append("OK")
    data = {}
    data["name"] = ""
    data["surname"] = ""
    data["tel"] = ""
    loginTokens[idOf] = data
    loginId = idOf
    requestTypes.insert(0, "createUser")
    requests.insert(0, request)
    responses.insert(0, response)

    for j in range(int(sys.argv[2])):
        func = secure_random.randint(1, 60)
        if func not in range(1, 21) and "updateName" not in requestTypes and j == int(sys.argv[2])-1:
            func = 10
        while func in range(1, 21) and requestTypes.count("updateName") == 3 and i < (int(sys.argv[1]) / 3):
            func = secure_random.randint(1, 60)
        while func in range(1, 21) and requestTypes.count("updateName") == 2 and i > int(sys.argv[1]) / 3 and i < 2*int(sys.argv[1]) / 3 :
            func = secure_random.randint(1, 60)        
        while func in range(1, 21) and requestTypes.count("updateName") == 1 and i > 2*int(sys.argv[1]) / 3 :
            func = secure_random.randint(1, 60)
        # func = funs[j]
        request =[]
        response = []
        if func in range(0, 0):
            # create user
            idOf = "".join(secure_random.choice(
                string.ascii_uppercase + string.digits) for _ in range(5))
            request = "createUser"
            data = {}
            data["name"] = ""
            data["surname"] = ""
            data["tel"] = ""
            loginTokens[idOf] = data
            response = idOf
            loginId = idOf
        elif func in range(1, 21):
            # update name
            updateData = names.get_first_name()
            # print updateData
            requestTypes.append("updateName")
            
            request.append(updateData)
            if 1==0:#func%10 == 0:
                response.append("error")
            else:
                data = loginTokens[loginId]
                data["name"] = updateData
                loginTokens[loginId] = data
                response.append("OK")
        elif func in range(21, 41):
            # updateSurname
            requestTypes.append("updateSurname")
            updateData = names.get_last_name()
            request.append(updateData)
            if 1==0:#func%10 == 0:
                response.append( "error")
            else:
                data = loginTokens[loginId]
                data["surname"] = updateData
                loginTokens[loginId] = data
                response.append("OK")
        elif func in range(41, 61):
            # updateTel
            requestTypes.append("updateTel")
            updateData = "054" + \
                "".join(secure_random.choice(string.digits) for _ in range(8))
            request.append( updateData)
            if 1==0:#func%10 == 0:
                response.append("error")
            else:
                data = loginTokens[loginId]
                data["tel"] = updateData
                loginTokens[loginId] = data
                response.append("OK")
        elif func in range(0, 0):
            # Who
            request = "who"
            if False:
                response = "error"
            else:
                response = str(loginTokens[loginId]).replace('\'', '')
        elif func in range(0, 0):
            # MyName
            request = "myName"
            if False:
                response = "error"
            else:
                response = str(loginTokens[loginId]["name"])
        elif func in range(0, 0):
            # MyTel
            request = "myTel"
            if False:
                response = "error"
            else:
                response = str(loginTokens[loginId]["tel"])
        elif func in range(0, 0):
            # MySurname
            request = "mySurname"
            if False:
                response = "error"
            else:
                response = str(loginTokens[loginId]["surname"])
        elif func in range(0, 0):
            # loginAs
            idOf = "".join(secure_random.choice(loginTokens.keys()))
            request = "loginAs:" + idOf
            response = "OK"
            loginId = idOf
        requests.append(request)
        responses.append(response)

    # from sklearn.utils import shuffle
    # requestTypes_s, requests_s, responses_s = shuffle(requestTypes[1:], requests[1:], responses[1:])
    # requestTypes_s.insert(0,requestTypes[0])
    # requests_s.insert(0,requests[0])
    # responses_s.insert(0,responses[0])
    # requestTypes = requestTypes_s
    # requests = requests_s
    # responses = responses_s

    request =[]
    response = []
    requestTypes.append("who")
    request.append("")
    response.append(loginTokens[loginId]["name"])
    response.append(loginTokens[loginId]["surname"])
    response.append(loginTokens[loginId]["tel"])
    requests.append(request)
    responses.append(response)
    typeList.append(requestTypes)
    reqList.append(requests)
    resList.append(responses)

file = open('ml_traces', 'w')
file.write('{')
file.write('\n\"request_types\" : ')
file.write(str(typeList).replace("\'","\""))
file.write(' ,')
file.write('\n\"request_data\" : ')
file.write(str(reqList).replace("\'","\""))
file.write(' ,')
file.write('\n\"response_data\" : ')
file.write(str(resList).replace("\'","\""))
file.write('\n')
file.write('}')
file.close()
