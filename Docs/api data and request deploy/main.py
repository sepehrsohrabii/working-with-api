import requests
from pathlib import Path
from mahan_functions import source_table, write_on_xml
Agent_id = 'MOW07603'

Operation, Request_Schema, Response_Schema, Resource = source_table()

for index,oper in enumerate(Operation, 1):
    print(str(index) + '-' +oper)
selected_operation_number = int(input('Select related operation number:'))
selected_Response_Schema = Response_Schema[selected_operation_number - 1]
selected_Resource = Resource[selected_operation_number - 1]





headers = {'Accept':'application/xml',
           'Content-Type':'application/xml',
           'Authorization': 'y00Lm/iuKNN6X8xU/p5FyJYVjXBCOh/JEQdcwPyGtJg='}
endpoint = 'https://staging.homares.ir/wsbe/rest'

url = endpoint + selected_Resource


xmlfile = write_on_xml(selected_operation_number)

response = requests.post(url = url, data=xmlfile, headers=headers)
respath = './HomaRes OTA API Sample for IR v1.1/1. {}_edited.xml'.format(selected_Response_Schema[:-4])


with open(respath, 'w') as f:
    f.write(response.text)
f.close()

