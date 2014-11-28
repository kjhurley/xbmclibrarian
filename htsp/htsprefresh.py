""" demonstrate grab of tvhead database

grab tvhead data base, identify recordings, match against TVDB entry
and report how recorded file should be renamed

"""
import htsp, unittest
import tvdb_api, tvdb_exceptions
import re

import logging

class Refresh(object):
    def __init__(self, server, port=9982, user="hts", password="hts"):
        self.server_and_port=(server,port)
        self.user_name=user
        self.password=password
        
    def connect(self):
        self.client=htsp.HTSPClient(self.server_and_port)
        self.client.hello()
        self.client.authenticate(user=self.user_name,passwd=self.password)
        self.count=0
        self.client.enableAsyncMetadata({'epg':1})
        
    def read_some_data(self):
        """ read some data from the epg dump
        
        use a generator to allow non-blocking reading
        """ 
        while True:
            msg=self.client.recv()
            if 'method' in msg:
                self.count+=1
                method=msg['method']
                if method!='initialSyncCompleted':
                    yield msg
                else:
                    break
        # the end
        
import sys
def refresh(server):
    recorded={}
    ref=Refresh(server)
    ref.connect()
    for msg in ref.read_some_data():
        if ref.count%400==0: 
            sys.stdout.write(".")
            sys.stdout.flush()
        if msg['method'] == "dvrEntryAdd" and msg["state"]=="completed":
            recorded[msg["id"]]=msg
    print
    return recorded

if __name__ == '__main__':
    import sys
    recs= refresh(sys.argv[1])
    for r in recs:
        print r, recs[r]
