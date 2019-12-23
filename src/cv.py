import os, sys, datetime

def dec(hexStr):
    return str(int(hexStr, base=16))

def binLong(hexStr):
    return bin(int(hexStr, 16))[2:].zfill(8)
    
def json(key, value):
    timestamp = datetime.datetime.now().isoformat()
    return "{'timestamp':'%s','%s':'%s'}" % (str(timestamp), str(key), str(value))