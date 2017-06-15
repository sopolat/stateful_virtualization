# -*- coding: utf-8 -*-
"""
Created on Fri Jun 09 10:52:54 2017

@author: sopolat
"""

import names
import random
import string

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
for i in range(20):
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
    requestTypes.append("createUser")
    requests.append(request)
    responses.append(response)
    
    for j in range(8):
        func = secure_random.randint(1, 60)
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
            requestTypes.append("updateName")
            
            request.append(updateData)
            if func%10 == 0:
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
            if func%10 == 0:
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
            if func%10 == 0:
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
