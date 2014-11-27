""" demonstrate grab of tvhead database

grab tvhead data base, identify recordings, match against TVDB entry
and report how recorded file should be renamed

"""
import htsp, unittest
import tvdb_api, tvdb_exceptions
import re

import logging

class TVDBShowFromEPG:
    """ find a show in the tv db from epg info """
    def __init__(self, tvdb):
        self.tvdb=tvdb
    def find(self, epg_data):
        self.show= self.tvdb[epg_data.show]
        return self.show

class Channel:
    def __init__(self,msg):
        self.lcn=msg["channelNumber"]
        self.name=msg["channelName"]
        self.id=msg["channelId"]

class Channels:
    def __init__(self):
        self.by_lcn={}
        self.id_to_number={}
        self.now_and_next=[]

    def __str__(self):
        s=""
        lcns=self.by_lcn.keys()
        lcns.sort()
        for c in lcns:
            s+="%d: %s\n"%(c, self.by_lcn[c].name)
        return s

    def add(self, msg):
        new_chan=Channel(msg)
        self.by_lcn[new_chan.lcn]=new_chan
        self.id_to_number[new_chan.id]=new_chan.lcn
        #self.now_and_next+=[msg["eventId"],msg["nextEventId"]]

    def find(self, name=None, lcn=None, chan_id=None):
        if name is not None:
            for l in self.by_lcn:
                if name == self.by_lcn[l].name:
                    return self.by_lcn[l]
        elif lcn is not None:
            return self.by_lcn[lcn]
        elif chan_id is not None:
            return self.by_lcn[self.id_to_number[chan_id]]
        else:
            raise RuntimeError("missing keyword")
        raise KeyError("Could not find channel using name=%s,lcn=%s,chan_id=%s"%(name, lcn,chan_id))
        

def recorded_on_channel(dvr_entry, channels):
    channels.find(chan_id=dvr_episode["channel"]).name.startswith(channel_name)

class TVDBShowFromEpgForNewE4(TVDBShowFromEPG):
    """ find an entry in tvdb for a 'brand new series' show 

    E4 insert 'NEW' into the title of shows!
    """
    def relevant(self, epg_data):
        epg_data.show.startswith("New:")

    def find(self, epg_data):
        show_without_new=epg_data.show

class IdentifyEpisodeFromEPG:
    def find(self, epg_data, tvdb):
        return None

class IdentifyEpisodeUsingEpisodeNumberInDescription(IdentifyEpisodeFromEPG):
    """ assume single season series """
    def find(self, epg_data, tvdb):
        """ epg text start with something like 2/5 

        episode id is the first number
        second number is the total number of episodes in the series

        assume single series
        """
        text=epg_data["description"]
        title=epg_data["title"]
        re_ep_id=re.compile('^(\d+)\/\d+\.\s+').search(text)
        if re_ep_id:
            episode_id=int(re_ep_id.groups()[0])
            return tvdb[title][1][episode_id]
        return None

class IdentifyEpisodeUsingEpisodeTitleInDescription(IdentifyEpisodeFromEPG):
    """ need to find the season as well using the description """

    def find(self, epg,tvdb):
        """ epg text like 'The Funny One: We all laugh ...'

        episode name is the first section of text

        assume single series
        """
        ep_name_search=re.compile("^([^:]+):\s+\w").search(epg.text)
        if ep_name_search:
            self.episode_name=ep_name_search.groups()[0]
            return tvdb[epg.title].search(epg_ep_name,key='episodename')
        return None

class EPGEntry:
    def __init__(self, epg):
        self.show=epg["title"]
        self.text=epg["description"]



def process_initial_sync():
    pass

def main():
    c=htsp.HTSPClient(("127.0.0.1",9982))
    rsp=c.hello()
    #print rsp
    c.authenticate(user='hts',passwd='hts')

    c.enableAsyncMetadata({'epg':1})

    # Process messages
    count=0
    MAX_COUNT=20000
    methods=[]
    channels=Channels()

    recorded={}
    samples=[]
    import sys

    while count<MAX_COUNT:
        count+=1
        if count%400==0: 
            sys.stdout.write(".")
            sys.stdout.flush()
        msg = c.recv()
        if 'method' in msg:
            method=msg['method']
            if method not in methods:
                methods+=[method]
                samples+=[msg]
            if method == "channelAdd":
                channels.add(msg)

            elif method == "dvrEntryAdd" and msg["state"]=="completed":
                recorded[msg["id"]]=msg
            elif method == "initialSyncCompleted":
                print
                break
    if count == MAX_COUNT: print "max messages received"

    tvdb=tvdb_api.Tvdb()

    for r in recorded:
        dvr_episode=recorded[r]
        try:
            epg=EPGEntry(dvr_episode)
            try:
                show=tvdb[epg.show]
            except tvdb_exceptions.tvdb_shownotfound, e:
                # might be mangled with 'new series' crap at the start - thanks E4!
                # 
                new_str="New:"
                if epg.show.startswith(new_str) and channels.find(chan_id=dvr_episode["channel"]).name.startswith("E4"):
                    epg.show=epg.show[len(new_str):].strip()
                    show=tvdb[epg.show]
            epg_text=dvr_episode["description"]
            re_ep_id=re.compile('^(\d+)\/\d+\.\s+').search(epg_text)
            re_ep_name=re.compile("^([^:]+):\s+\w").search(epg_text)
            if re_ep_id:
                epg_ep=int(re_ep_id.groups()[0])
                print "%s -> %s_%02dx%02d.mkv"%(dvr_episode["path"],epg.show, 1, epg_ep)
                continue
            elif re_ep_name:
                epg_ep_name=re_ep_name.groups()[0]
                if dvr_episode["title"].startswith("New:") and epg_ep_name.startswith("Brand new series - "):
                    epg_ep_name=epg_ep_name[len("Brand new series -"):].strip()
                e=show.search(epg_ep_name,key='episodename')
                if len(e)==1:
                    seas_num=int(e[0]['seasonnumber'])
                    ep_num= int(e[0]['episodenumber'])
                    print "%s -> %s_%dx%02d.mkv"%(dvr_episode["path"],epg.show, seas_num, ep_num)

                    continue
            # fall through to here if no matches
            print "[[ not possible to match : %s ]]"%dvr_episode

        except tvdb_exceptions.tvdb_shownotfound, e:
            print "[[ not possible to match : %s ]]"%dvr_episode


if __name__ == '__main__':
    main()
