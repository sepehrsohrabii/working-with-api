from mahan_functions import source_table
selected_operation_number = 3
Agent_id = 'MOW07603'
Operation, Request_Schema, Response_Schema, Resource = source_table()
selected_operation = Operation[selected_operation_number - 1]
selected_Request_Schema = Request_Schema[selected_operation_number - 1]

path = './HomaRes OTA API Sample for IR v1.1/1. {}.xml'.format(selected_Request_Schema[:-4])
newpath = './HomaRes OTA API Sample for IR v1.1/1. {}_edited.xml'.format(selected_Request_Schema[:-4])
import xml.etree.ElementTree as ET

tree = ET.parse(path)
root = tree.getroot()

for el in tree.iter():
    print(el.attrib)
    for key in el.attrib.keys():
        if key == 'FlightNumber':
            print(el.attrib[key])