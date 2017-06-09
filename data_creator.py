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
    data["name"]=names.get_first_name()
    data["surname"] = names.get_last_name()
    data["tel"] = "054" + "".join(secure_random.choice(string.digits) for _ in range(8))
    loginTokens["".join(secure_random.choice(string.ascii_uppercase + string.digits) for _ in range(5))] = data
reqList = []
resList = []
for i in range( 50):
    requests=[]
    responses=[]
    loginId="bos"
    #loginAs
    idOf="".join(secure_random.choice(loginTokens.keys()))
    requests.append( "loginAs:" + idOf)
    responses.append("OK")
    loginId=idOf
    for j in range(10):
        func = secure_random.randint(1,101)
        if func in range(1,6):
            #create user
            idOf="".join(secure_random.choice(string.ascii_uppercase + string.digits) for _ in range(5))
            request = "createUser"
            data = {}
            data["name"]=""
            data["surname"] = ""
            data["tel"] = ""
            loginTokens[idOf]=data
            response=idOf
        elif func in range(6,26):
            #update name
            updateData=names.get_first_name()
            request = "updateName:" + updateData
            if loginId=="bos":
                response="error"
            else:
                data=loginTokens[loginId]
                data["name"]=updateData
                loginTokens[loginId]=data
                response="OK"
        elif func in range(26,46):
            #updateSurname
            updateData= names.get_last_name()
            request = "updateSurname:" + updateData
            if loginId=="bos":
                response="error"
            else:
                data=loginTokens[loginId]
                data["surname"]=updateData
                loginTokens[loginId]=data
                response="OK"
        elif func in range(46,66):
            #updateTel
            updateData="054" + "".join(secure_random.choice(string.digits) for _ in range(8))
            request = "updateTel:" + updateData
            if loginId=="bos":
                response="error"
            else:
                data=loginTokens[loginId]
                data["tel"]=updateData
                loginTokens[loginId]=data
                response="OK"
        elif func in range(66,96):
            #Who
            request = "who"
            if loginId=="bos":
                response="error"
            else:
                response=str(loginTokens[loginId]).replace('\'','')
        elif func in range(96,102):
            #loginAs
            idOf="".join(secure_random.choice(loginTokens.keys()))
            request = "loginAs:" + idOf
            response="OK"
            loginId=idOf
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