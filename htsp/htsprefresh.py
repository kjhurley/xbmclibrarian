""" demonstrate grab of tvhead database

grab tvhead data base, identify recordings, match against TVDB entry
and report how recorded file should be renamed

"""
import htsp, unittest
import tvdb_api, tvdb_exceptions
import re

import logging


def refresh(server, port=9982, user="hts", password="hts"):
    c=htsp.HTSPClient((server,port))
    c.hello()
    c.authenticate(user=user,passwd=password)
    c.enableAsyncMetadata({'epg':1})

    # Process messages
    count=0
    MAX_COUNT=20000

    recorded={}
    import sys

    while count<MAX_COUNT:
        count+=1
        if count%400==0: 
            sys.stdout.write(".")
            sys.stdout.flush()
        msg = c.recv()
        if 'method' in msg:
            method=msg['method']
            
            if method == "dvrEntryAdd" and msg["state"]=="completed":
                recorded[msg["id"]]=msg
            elif method == "initialSyncCompleted":
                print
                break

    return recorded

if __name__ == '__main__':
    import sys
    recs= refresh(sys.argv[1])
    for r in recs:
        print r, recs[r]
