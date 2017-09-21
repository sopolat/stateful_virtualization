import xml.etree.ElementTree
import json
from collections import defaultdict
import string 
import re
def stuff():
    with open('getFares2.xml', 'w') as a:
        with open('publication_getFares.xml') as f:
            for line in f:
                a.writelines(unicode( line, errors='ignore'))
    return 


def dataCut(data,data2,maxLen=1000):
    reqs=[]
    ress=[]
    
    for reqs2, ress2 in zip(data,data2):
        if "*A" not in " ".join(reqs2):
            continue
        if "SINE IN"in " ".join(ress2):
            continue
        if "REQUESTED CLASS IS NOT AVAILABLE" in " ".join(ress2):
            continue
        if "INHIBITED FOR INTERNET" in " ".join(ress2):
            continue
        if "INVALID DATE" in " ".join(ress2):
            continue
        if(len(reqs2[-1])>maxLen or len(ress2[-1])>maxLen):
            continue
        for a,b in zip(reqs2, ress2):
            reqs.append(" ".join(a.split()))
            ress.append(" ".join(b.split()))
    return reqs , ress


def dataParse2(reqs,ress):
    reqs2=[]
    ress2=[]
    for req,res in zip(reqs, ress):
        data=[]
        data2=[]
        req2=[]
        res2=[]
        for a,b in zip(req,res):
            newData=[]
            if(a[0:3] =="0TK" or a[0:2]=="0O" ):
                for tk in a.split("|"):
                    index=3
                    while(tk[index] in string.digits):
                        index +=1
                    newData.append(tk[0:index]+" "+tk[index]+" "+tk[index+1:index+6]+" "+tk[index+6:index+12]+" "+tk[index+12:len(a)])
                data.append(" | ".join(newData))
                data2.append(b.split("*T R O Y A*")[0])
            else:
                data.append(a)
                data2.append(b.split("*T R O Y A*")[0])
            req2.append(" ".join(data))
            res2.append(" ".join(data2))
        reqs2.append(req2)
        ress2.append(res2)
    return reqs2 , ress2

def dataParse(traces):
    reqs=traces["requests"]
    ress=traces["responses"]
    reqs2=[]
    ress2=[]
    
    for req,res in zip(reqs, ress):
        req2=[]
        res2=[]
        count =0
        for a,b in zip(req,res):
            if(a == "QX"):
                count+=1
            if(count == 2):
                break
            req2.append(a)
            res2.append(b)
        reqs2.append(req2)
        ress2.append(res2)
    return reqs2,ress2

def dataParse3(traces):
    reqs=traces["requests"]
    ress=traces["responses"]
    newdata = {}
    newdata['request_types'] = []
    newdata['request_data'] = []
    newdata['response_data'] = []
    
    for req,res in zip(reqs, ress):
        type2=[]
        req2=[]
        res2=[]
        count =0
        for a,b in zip(req,res):
            b=b.split("*T R O Y A*")[0]
            if(a == "QX" or a == "I" or a == "BSX" or a == "UR" or a == "*ET-@I" or a == "*ET-/I" or a == "BMITT*IT/SU" or a == "BM/SC-R" or a == "E"):
                type2.append(a)
                req2.append("")
                res2.append(b)
                continue
            if(a == "BSIA5005BW/SU"):
                type2.append(a)
                req2.append("")
                res2.append(b)
                continue
            if((a[0] =="0")and a!="0A"):
                dumpa=[]
                for tk in a.split("|"):
                    index=3
                    while(tk[index] in string.digits):
                        index +=1
                    dumpa.append(tk[0:index])
                    dumpa.append(tk[index])
                    dumpa.append(tk[index+1:index+6])
                    dumpa.append(tk[index+6:index+12])
                    dumpa.append(tk[index+12:len(a)])
                type2.append("ticket")
                req2.append(dumpa)
                res2.append(b.split())
                continue
            if(a == "*R"):
                type2.append(a)
                req2.append("")
                res2.append(b.split())
                continue
            if(a[0] == "-"):
                type2.append("-")
                req2.append(a[1:])
                res2.append(b[1:].split())
                continue
            if(a == "*A"):
                type2.append(a)
                req2.append("")
                res2.append(b.split())
                continue
            if(a[0] == "*"):
                type2.append("*")
                req2.append(a.split('*'))
                res2.append(b.split())
                continue
            if(a[0:3] == "BMS"):
                type2.append(a[0:3])
                req2.append(a[3:])
                res2.append(b)
                continue
            if(a[0:3] == "FQP"):
                type2.append(a)
                req2.append(re.split("-[0-9]",a[3:]))
                res2.append(b)
                continue
            if(a[0:9]  == "5.. LDTP "):
                type2.append(a[0:9])
                req2.append(a[9:])
                res2.append(b)
                continue
            if(a[0:5] == "6ITT-"):
                type2.append("6ITT")
                req2.append(a[5:])
                res2.append(b.split('-'))
                continue
            if(a == "CX"):
                type2.append(a)
                req2.append("")
                res2.append(b)
                continue
            if(a.split("*")[0] == "SC"):
                type2.append(a.split("*")[0])
                req2.append(a.split("*")[1])
                res2.append(b)
                continue
            if(a == "4FGMIL"):
                type2.append(a)
                req2.append("")
                res2.append(b)
                continue
            if(a[0] == "4"):
                type2.append(a)
                req2.append("")
                res2.append(b)
                continue
            if(a[0:3] == "FZS"):
                type2.append("FZS")
                req2.append(a[3:-3])
                req2.append(a[-3:])
                res2.append(b)
                continue
            if(a == "SOF"):
                type2.append(a)
                req2.append("")
                res2.append(b)
                continue
            if(a == "0A"):
                type2.append(a)
                req2.append("")
                res2.append(b)
                continue
            print(a)
            print(b)
            eror()
        newdata['request_types'].append(type2)
        newdata['request_data'].append(req2)
        newdata['response_data'].append(res2)
    return newdata

def parse_thy():

    traces = {}
    traces['requests'] = []
    traces['responses'] = []
    print("ok")
    root = xml.etree.ElementTree.parse('publication_getFares.xml').getroot()
    oldkey = root[0][5].text
    requests = []
    responses = []
    print("ok2")
    for child in root:
        keyzo = child[5].text
        row = child[2].text
        request_splits = row.split('->')
        # print len(request_splits)
        if keyzo!=oldkey:
            traces['requests'].append(requests)
            traces['responses'].append(responses)
            requests = []
            responses = []
#            requests.append(str(keyzo))
#            responses.append(str(keyzo))
        for request_split in request_splits:
            if request_split=='':
                continue
            response_split = request_split.split('<-')
            request_data = response_split[0]
            if len(response_split)==1 :
                response_data = "NO DATA"
            else:
                response_data = response_split[1]
            request = request_data.split('\n')[1]
            response = ''.join(response_data.split('\n')[1:])

            requests.append(request)
            responses.append(response)
        oldkey = keyzo 
        
    traces['requests'].append(requests)
    traces['responses'].append(responses)


    return traces

traces = parse_thy()
newdata= dataParse3(traces)
with open('publication_data.txt', 'w') as outfile:
    json.dump(newdata, outfile)
#reqs,ress=dataParse(traces)
#data ,data2 = dataParse2(reqs,ress)
#datax,datax2 = dataCut(data,data2,500)
#with open("reqs.txt","w") as file1:
#    file1.writelines("\n".join(datax))
#with open("ress.txt","w") as file1:
#    file1.writelines("\n".join(datax2))