from xmlrpc.server import SimpleXMLRPCServer
from xmlrpc.client import ServerProxy
import sys
import json

workers = {
    'worker-1': ServerProxy("http://localhost:23001/"),
    'worker-2': ServerProxy("http://localhost:23002/")
}


def getbylocation(location):
    amGroupArray = workers['worker-1'].getbylocation(location)
    nzGroupArray = workers['worker-2'].getbylocation(location)
    return {
            'error': False,
            'result': amGroupArray + nzGroupArray
    }


def getbyname(name):
    #here we check whether the name is in given range or not
     if name[0] in getCharRange("a","m"):
        result = workers['worker-1'].getbyname(name)
    else:
        result = workers['worker-2'].getbyname(name)

    return {
            'error': False,
            'result': result
    }


def getbyyear(location, year):
    amGroupResult = workers['worker-1'].getbyyear(location,year)
    nzGroupResult = workers['worker-2'].getbyyear(location,year)
    return {
            'error': False,
            'result': amGroupResult + nzGroupResult
    }

     
def getCharRange(start, stop):
    return (chr(n) for n in range(ord(start), ord(stop) + 1))


def main():
    port = int(sys.argv[1])
    server = SimpleXMLRPCServer(("localhost", port))
    print(f"Listening on port {port}...")

    #: register RPC functions
    server.register_function(getbyname,"getbyname")
    server.register_function(getbylocation,"getbylocation")
    server.register_function(getbyyear,"getbyyear")
    server.serve_forever()


if __name__ == '__main__':
    main()