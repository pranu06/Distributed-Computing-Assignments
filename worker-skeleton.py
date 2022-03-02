import json
import sys
from xmlrpc.server import SimpleXMLRPCServer

# Storage of data

# Opening JSON file
amJson = open('data-am.json')
nzJson = open('data-nz.json')

# returns JSON object as
amJsonData = json.load(amJson)
nzJsonData = json.load(nzJson)

#create an empty list to store location and year values
foundLocValues = []
foundLocYearValues = []

amValues = list(amData.values())
nzValues = list(nzData.values())
data_table = []

def load_data(group):
    # load data based which portion it handles (am or nz)
    if group == 'am': 
        data_table.append(amData)
    else:
        data_table.append(nzData) 
    pass


def getbyname(name):
    #here we need to check whether given name is present in data_table or not 
    if name in data_table[0]:
        return data_table[0][name]
        
    else:
        return f"Sorry record not found with {name}"


def getbylocation(location):
    #convert dict to list of objects so that we can iterate
    groupValues = list(data_table[0].values()) 
    for value in groupValues:
        if location == value['location']:
            foundLocValues.append(value)
    
    return foundLocValues
        

def getbyyear(location, year):
    #convert dict to list of objects so that we can iterate
    groupValues = list(data_table[0].values())
    for value in groupValues:
        if location == value['location'] and year == value['year']:
            foundLocYearValues.append(value)
    
    return foundLocYearValues
 
        

def main():
    if len(sys.argv) < 3:
        print('Usage: worker.py <port> <group: am or nz>')
        sys.exit(0)

    port = int(sys.argv[1])
    group = sys.argv[2]
    server = SimpleXMLRPCServer(("localhost", port))
    print(f"Listening on port {port}...")
  
    #register RPC functions
    load_data(group) 
    server.register_function(getbyname,"getbyname")
    server.register_function(getbylocation,"getbylocation")
    server.register_function(getbyyear,"getbyyear")
    server.serve_forever()

if __name__ == '__main__':
    main()
