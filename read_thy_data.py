
import xml.etree.ElementTree
import json
from collections import defaultdict

def parse_thy():

    traces = {}
    traces['requests'] = []
    traces['responses'] = []
    
    root = xml.etree.ElementTree.parse('thy_data.xml').getroot()

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
    trace_file.write(str(traces))
    trace_file.close()

    return

def parse_thy_operation_type_based():

    traces = {}
    traces['requests'] = []
    traces['responses'] = []
    
    root = xml.etree.ElementTree.parse('thy_data.xml').getroot()

    operation_file = open('operation_to_requests', 'w')

    for child in root[:1000]:

        operation_type = child[1].text

        operation_file.write('-----' + operation_type + '-----')
        operation_file.write('\n')

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
            response_data = response_split[1]
            request = request_data.split('\n')[1]
            response = ''.join(response_data.split('\n')[1:])

            requests.append(request)
            responses.append(response)
        
        operation_file.write(str(requests))
        operation_file.write('\n')
        operation_file.write(str(responses))
        operation_file.write('\n')
        operation_file.write('\n')

    operation_file.close()

    return


def find_differences():
    f = open('thy_traces','rb')
    traces = json.load(f)
    requests_list = traces['requests']
    responses_list = traces['responses']

    unique_requests = []

    req_to_res = defaultdict(list)
    for i in range(len(requests_list)):
        requests = requests_list[i]
        for j in range(len(requests)):
            request = requests[j]
            if request not in unique_requests:
                unique_requests.append(request)        
            if responses_list[i][j].strip() not in req_to_res[request]:
                req_to_res[request.strip()].append(responses_list[i][j].strip())


    print len(unique_requests)
    print len(req_to_res)

    f = open('unique_requests','w')
    for ureq in unique_requests:
        f.write(ureq)
        f.write('\n')
    f.close()

    i = 0
    for key in req_to_res:
        if len(req_to_res[key]) > 3: 
            print key + ' --- ' + str(req_to_res[key])
            i += 1

        if i == 15:
            break


def find_differences_operation_type_based():
    
    root = xml.etree.ElementTree.parse('thy_data.xml').getroot()

    req_list = []
    for child in root[:1000]:

        operation_type = child[1].text

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
            response_data = response_split[1]
            request = request_data.split('\n')[1]
            response = ''.join(response_data.split('\n')[1:])

        requests.append(request)
        if requests not in req_list:
            req_list.append(requests)
        else:
            print str(requests)
        responses.append(response)

if __name__ == "__main__":
    find_differences_operation_type_based()
