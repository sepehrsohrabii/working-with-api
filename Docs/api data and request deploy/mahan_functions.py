import re
from datetime import datetime


def source_table():
    Operation = []
    Request_Schema = []
    Response_Schema = []
    Resource = []

    with open('table source.txt') as file:
        for row in file:
            row = row.strip()
            op = row[:row.index(',')]
            Operation.append(op)
            RQ = re.findall(', (.*RQ.xsd)', row)

            Request_Schema.append(RQ[0])
            RS = re.findall('xsd (.*RS.xsd)', row)
            Response_Schema.append(RS[0])
            resource = re.findall('/.*', row)
            Resource.append(resource[0])
    return Operation, Request_Schema, Response_Schema, Resource




def write_on_xml(selected_operation_number):
    Agent_id = 'MOW07603'
    Operation, Request_Schema, Response_Schema, Resource = source_table()
    selected_operation = Operation[selected_operation_number - 1]
    print('you select %s' % selected_operation)
    selected_Request_Schema = Request_Schema[selected_operation_number - 1]

    path = './HomaRes OTA API Sample for IR v1.1/1. {}.xml'.format(selected_Request_Schema[:-4])
    newpath = './HomaRes OTA API Sample for IR v1.1/1. {}_edited.xml'.format(selected_Request_Schema[:-4])
    import xml.etree.ElementTree as ET
    tree = ET.parse(path)
    root = tree.getroot()
    root[0][0][0].attrib['ID'] = Agent_id
    root[0][0].attrib['ISOCurrency'] = 'RUB'
    root.attrib['Target'] = 'Test'  # Test or Production
    root.attrib['TimeStamp'] = datetime.utcnow().strftime('%Y-%m-%dT%H:%M:%S')
    root.attrib['EchoToken'] = '0001'
    if selected_operation_number==1:
        root[1].text = 'Hi sepehr'
    elif selected_operation_number==2:
        root[1][0].text = '2022-05-15'



    elif selected_operation_number==3:
        root[1][0].text = '2022-05-10'


    elif selected_operation_number==4:
        # print(Request_Schema[2])
        search_path = './HomaRes OTA API Sample for IR v1.1/1. {}_edited.xml'.format(Response_Schema[1][:-4])
        import xml.etree.ElementTree as ET
        search_tree = ET.parse(search_path)
        search_root = search_tree.getroot()
        for el in search_tree.iter():
            for key in el.attrib.keys():
                if key == 'FlightNumber':
                    # print(el.attrib[key])
                    root[1][0][0][0].attrib['FlightNumber'] = el.attrib[key]
                if key == 'DepartureDateTime':
                    # print(el.attrib[key])
                    root[1][0][0][0].attrib['DepartureDateTime'] = el.attrib[key]
                if key == 'ArrivalDateTime':
                    # print(el.attrib[key])
                    root[1][0][0][0].attrib['ArrivalDateTime'] = el.attrib[key]
                if key == 'Duration':
                    # print(el.attrib[key])
                    root[1][0][0][0].attrib['Duration'] = el.attrib[key]
                if key == 'StopQuantity':
                    # print(el.attrib[key])
                    root[1][0][0][0].attrib['StopQuantity'] = el.attrib[key]
                if key == 'RPH':
                    # print(el.attrib[key])
                    root[1][0][0][0].attrib['RPH'] = el.attrib[key]
                if key == 'AirEquipType':
                    # print(el.attrib[key])
                    root[1][0][0][0].attrib['AirEquipType'] = el.attrib[key]
                if key == 'RPH':
                    # print(el.attrib[key])
                    root[1][0][0][0].attrib['RPH'] = el.attrib[key]
                if key == 'RPH':
                    # print(el.attrib[key])
                    root[1][0][0][0].attrib['RPH'] = el.attrib[key]
                if key == 'RPH':
                    # print(el.attrib[key])
                    root[1][0][0][0].attrib['RPH'] = el.attrib[key]
                if key == 'RPH':
                    # print(el.attrib[key])
                    root[1][0][0][0].attrib['RPH'] = el.attrib[key]

        # print(search_root[1][0][1][0][0].attrib['Amount'])
        # print(search_root[1][0][1][0][1].attrib['Amount'])

        root[2][0][0].attrib['Amount'] = search_root[1][0][1][0][0].attrib['Amount']
        root[2][0][1].attrib['Amount'] = search_root[1][0][1][0][1].attrib['Amount']
        root[2][0][0].attrib['CurrencyCode'] = search_root[1][0][1][0][0].attrib['CurrencyCode']
        root[2][0][1].attrib['CurrencyCode'] = search_root[1][0][1][0][1].attrib['CurrencyCode']
        root[5][0][0][1].attrib['Amount'] = search_root[1][0][1][0][1].attrib['Amount']
        root[5][0][0][1].attrib['CurrencyCode'] = search_root[1][0][1][0][1].attrib['CurrencyCode']
    elif selected_operation_number == 5:
        root[1].attrib['ID'] = 'VPTF21'

    tree.write(newpath)
    with open(newpath) as file:
        xmlfile = file.read()
    return xmlfile
