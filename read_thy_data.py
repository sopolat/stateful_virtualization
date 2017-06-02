
import xml.etree.ElementTree
import json
from collections import defaultdict

def parse_thy():

    traces = {}
    traces['requests'] = []
    traces['responses'] = []
    
    root = xml.etree.ElementTree.parse('createProfile_30_seasion_getFlightDetails_17_trace.xml').getroot()

    for child in root[:1000]:
        row = child[2].text
        request_splits = row.split('->')
        # print len(request_splits)
        requests = []
        responses = []
        for request_split in request_splits:
            if request_split=='':
                continue
            response_split = request_split.split('<-')
            request_data = response_split[0]
            if(len(response_split)==1):
                response_data = "No Response"
            else:
                response_data = response_split[1]
            request = request_data.split('\n')[1]
            response = ''.join(response_data.split('\n')[1:])

            requests.append(request)
            responses.append(response)

        traces['requests'].append(requests)
        traces['responses'].append(responses)

    # for response in traces['responses']:
    #     for r in responses:
    #         print r

    trace_file = open('thy_traces','w')
    trace_file.write(str(traces).replace('\'','\"'))
    trace_file.close()

    return

def find_differences():
    f = open('thy_traces','rb')
    traces = json.load(f)
    requests_list = traces['requests']
    responses_list = traces['responses']

    req_to_res = defaultdict(list)
    for i in range(len(requests_list)):
        requests = requests_list[i]
        for j in range(len(requests)):
            request = requests[j]
            if responses_list[i][j].strip() not in req_to_res[request]:
                req_to_res[request.strip()].append(responses_list[i][j].strip())


    print (len(req_to_res))

    i = 0
    for key in req_to_res:
        if len(req_to_res[key]) > 3: 
            print (key + ' --- ' + str(req_to_res[key]))
            i += 1

        if i == 10:
            break


if __name__ == "__main__":
    parse_thy()
