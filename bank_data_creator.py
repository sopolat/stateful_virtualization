fr = open('bank_data.xml', 'rb')
fw = open('bank_data_deposit.xml', 'wb')

while True:
    line = fr.readline()
    if not line:
        break  # EOF

    if 'depositMoney' not in line:
        continue

    fw.write(line)

from random import randint

for i in range(500):
    if i != 0:
        fw.write('\n')
    dep_req_1 = '<?xml?><S:Envelope xmlns:S=""><S:Body><ns2:depositMoney xmlns:ns2=""><accountId>'
    f = randint(10, 999)
    s = randint(10, 999)
    t = randint(10, 999)
    dep_req_2 = '</accountId><amount>'
    amnt = randint(10, 9999)
    dep_req_3 = '</amount></ns2:depositMoney></S:Body></S:Envelope>'
    fw.write(dep_req_1 + str(f) + '-' + str(s) + '-' +
             str(t) + dep_req_2 + str(amnt) + dep_req_3)
    fw.write('\n')

    dep_res_1 = '<?xml?><S:Envelope xmlns:S=""><S:Body><ns2:depositMoneyResponse xmlns:ns2=""><return>'
    amnt = randint(10, 99999)
    dep_res_2 = '</return></ns2:depositMoneyResponse></S:Body></S:Envelope>'
    fw.write(dep_res_1 + str(amnt) + dep_res_2)
