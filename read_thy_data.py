
import xml.etree.ElementTree

def parse_thy():

    traces = {}
    traces['requests'] = []
    traces['responses'] = []
    
    root = xml.etree.ElementTree.parse('thy_data.xml').getroot()

    for child in root[:100]:
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

if __name__ == "__main__":
    parse_thy()