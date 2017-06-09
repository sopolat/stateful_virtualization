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
for k in range(5):
    data = {}
    data["name"] = names.get_first_name()
    data["surname"] = names.get_last_name()
    data["tel"] = "054" + \
        "".join(secure_random.choice(string.digits) for _ in range(8))
    loginTokens["".join(secure_random.choice(
        string.ascii_uppercase + string.digits) for _ in range(5))] = data
reqList = []
resList = []
for i in range(1):
    requests = []
    responses = []
    loginId = "bos"
    # loginAs
    idOf = "".join(secure_random.choice(loginTokens.keys()))
    requests.append("loginAs:" + idOf)
    responses.append("OK")
    loginId = idOf
    for j in range(100):
        func = secure_random.randint(1, 140)
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
        elif func in range(1, 21):
            # update name
            updateData = names.get_first_name()
            request = "updateName:" + updateData
            if func % 4 == 0:
                response = "error"
            else:
                data = loginTokens[loginId]
                data["name"] = updateData
                loginTokens[loginId] = data
                response = "OK"
        elif func in range(21, 41):
            # updateSurname
            updateData = names.get_last_name()
            request = "updateSurname:" + updateData
            if func % 4 == 0:
                response = "error"
            else:
                data = loginTokens[loginId]
                data["surname"] = updateData
                loginTokens[loginId] = data
                response = "OK"
        elif func in range(41, 61):
            # updateTel
            updateData = "054" + \
                "".join(secure_random.choice(string.digits) for _ in range(8))
            request = "updateTel:" + updateData
            if func % 4 == 0:
                response = "error"
            else:
                data = loginTokens[loginId]
                data["tel"] = updateData
                loginTokens[loginId] = data
                response = "OK"
        elif func in range(61, 81):
            # Who
            request = "who"
            if False:
                response = "error"
            else:
                response = str(loginTokens[loginId]).replace('\'', '')
        elif func in range(81, 101):
            # MyName
            request = "myName"
            if False:
                response = "error"
            else:
                response = str(loginTokens[loginId]["name"])
        elif func in range(101, 121):
            # MyTel
            request = "myTel"
            if False:
                response = "error"
            else:
                response = str(loginTokens[loginId]["tel"])
        elif func in range(121, 141):
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
    reqList.append(requests)
    resList.append(responses)

file = open('template_approach_traces', 'w')
file.write('{')
file.write('\n')
file.write(str(reqList))
file.write('\n')
file.write(str(resList))
file.write('\n')
file.write('}')
file.close()
