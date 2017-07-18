
import random
import sys 

number_of_traces = int(sys.argv[1])
trace_size = int(sys.argv[2])
limit = 5
operation_to_be_trained = 'delete'
 
request_types_list = []
request_data_list = []
response_data_list = []
traces = {}
for i in range(number_of_traces):
    request_types = []
    request_data = []
    response_data = []

    id_counter = 1
    services = []
    for j in range(trace_size-1):
        rand_number = random.randint(0, 2)
        used_ids = []
        if rand_number == 0:
            request_types.append('service/add/')

            payload = []
            payload.append(id_counter)
            payload.append('service' + str(id_counter))
            payload.append('someurl' + str(id_counter))
            payload.append('SOAP')

            request_data.append([payload])

            if len(services) < limit:

                response_data.append(['OK'])

                serv_dict = {}
                serv_dict['id'] = id_counter
                serv_dict['serviceName'] = 'service' + str(id_counter)
                serv_dict['serviceUrl'] = 'someurl' + str(id_counter)
                serv_dict['protocol'] = 'SOAP'
                services.append(serv_dict)

                used_ids.append(id_counter)

                id_counter += 1

            else:
                response_data.append(['ERROR'])

        if rand_number == 1:
            request_types.append('service/delete/')

            if len(services) > 0:
                service_to_be_deleted = random.randint(0, 10)
                delete_id = services[service_to_be_deleted]['id']
                response_data.append(['OK'])
                services.remove(services[service_to_be_deleted])
            else:
                delete_id = random.randint(0, 5)
                response_data.append(['ERROR'])

            payload = []
            payload.append(delete_id)
            request_data.append(payload)

        if rand_number == 2:
            request_types.append('service/list/')

            payload = []
            payload.append("")

            request_data.append(payload)
            serv_list = []
            for serv in services:
                serv_list.append(serv.values())    
            response_data.append(serv_list)


    if operation_to_be_trained == 'add':

        request_types.append('service/add/')

        payload = []
        payload.append(id_counter)
        payload.append('service' + str(id_counter))
        payload.append('someurl' + str(id_counter))
        payload.append('SOAP')

        request_data.append(payload)

        if len(services) < limit:

            response_data.append(['OK'])

            serv_dict = {}
            serv_dict['id'] = id_counter
            serv_dict['serviceName'] = 'service' + str(id_counter)
            serv_dict['serviceUrl'] = 'someurl' + str(id_counter)
            serv_dict['protocol'] = 'SOAP'
            services.append([serv_dict])

            used_ids.append(id_counter)

            id_counter += 1

        else:
            response_data.append(['ERROR'])
    elif operation_to_be_trained == 'delete':
        request_types.append('service/delete/')

        if len(services) > 0:
            service_to_be_deleted = random.randint(0, len(services) - 1)
            delete_id = services[service_to_be_deleted]['id']
            response_data.append(['OK'])
            services.remove(services[service_to_be_deleted])
        else:
            delete_id = random.randint(0, 5)
            response_data.append(['ERROR'])

        payload = []
        payload.append(delete_id)
        request_data.append(payload)



    request_types_list.append(request_types)
    request_data_list.append(request_data)
    response_data_list.append(response_data)

file = open('ml_service_traces', 'w')
file.write('{')
file.write('\n\"request_types\" : ')
file.write(str(request_types_list).replace("\'", "\""))
file.write(' ,')
file.write('\n\"request_data\" : ')
file.write(str(request_data_list).replace("\'", "\""))
file.write(' ,')
file.write('\n\"response_data\" : ')
file.write(str(response_data_list).replace("\'", "\"").replace("]\"","]").replace("\"[","["))
file.write('\n')
file.write('}')
file.close()
