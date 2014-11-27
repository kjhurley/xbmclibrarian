'''
Created on 14 Aug 2014

@author: khurley



'''
import re
import tvdb_api
import tvdb_exceptions
import htsp
import xml.etree.cElementTree as ET
import logging

#logging.getLogger().setLevel(logging.DEBUG)
class Episode(object):
    @staticmethod
    def match_info(info_dict):
        """ test if info fields are a match for this Episode class """
        return True
    
    def __init__(self, show_name, episode_title, season_number, episode_number):
        self.show_name=show_name
        self.episode_title=episode_title
        self.episode_number=(season_number,episode_number)
        self.tvdb_ok=None # None if not checked, True if show and episode titles match
    
    def cross_check_with_tvdb(self):
        self.tvdb_ok=False  
        try:
            tv=tvdb_api.Tvdb()
        except tvdb_exceptions.tvdb_exception:
            self.tvdb_ok=None
            return
        try:
            the_show=tv[self.show_name_for_tvdb()]
        except tvdb_exceptions.tvdb_exception:
            print "tvdb show lookup failed!"
            return
        try:
            search_result=the_show.search(self.episode_title_for_tvdb())
        except tvdb_exceptions.tvdb_exception:
            print "tvdb episode lookup failed!"
            return
        assert len(search_result)>0, "no matches for %s"%(self)
        
        if len(search_result)==1:
            matched_episode=search_result[0]
        elif len(search_result)>1:
            # try using season/episode
            try:
                matched_episode=the_show[self.episode_number[0]][self.episode_number[1]]
            except tvdb_exceptions.tvdb_exception:
                raise RuntimeError("could not resolve multiple matches for %s"%self)
        
        # update episode number using tvdb data
        self.episode_number=(int(matched_episode.get(u'seasonnumber')),int(matched_episode.get(u'episodenumber')))
        self.tvdb_ok=True
            
    def convert_to_nfo(self):
        top=ET.Element('episodedetails')
        ET.SubElement(top,"title")
            
    def show_name_for_tvdb(self):
        """ base class is a null op
        needed for special cases where name needs mangling before it can be used in tvdb lookup!
        """ 
        return self.show_name
    
    def episode_title_for_tvdb(self):
        """ base class method is a null op 
        
        this is only needed in derived classes that do special handling
        """
        return self.episode_title
    
    def __repr__(self):
        return "%s;%s;s%02d.e%02d [tvdb=%s]"%(self.show_name_for_tvdb(), self.episode_title_for_tvdb(), self.episode_number[0],self.episode_number[1],self.tvdb_ok)
       
class HTSPInfoParser(object):
    '''
    Reads the htsp epg dump and build objects representing individual shows
    '''


    def __init__(self, htsp_server):
        '''
        Constructor
        '''
        self._server = htsp_server
        self.shows=[]
        
    def read_log(self):
        """ read through the whole stream building the list of shows 
        
        Initially populate dictionaries built from the fields in the info stream
        
        """
        
        
        htsp_client=htsp.HTSPClient(self._server)
        htsp_client.authenticate(user='hts',passwd='hts')
        htsp_client.enableAsyncMetadata({'epg':1})
        
        
        fields={'name': "nameshort:\s+(?P<name>\S[\s\S]+)$",
                "title": "episodeshort:\s+(?P<title>\S[\s\S]+)$",
                "full title": "title:\s+(?P<full_title>\S[\s\S]+)$",
                "description":"desc:\s+(?P<description>\S+.*)$",
                "episode name":"episodeshort:\s+(?P<episode_name>\S+.*)$"}
        optional_fields={
                "senum": "senum:\s+(?P<senum>s\d+e\d+)$",}
        fields_re={}
        [fields_re.update({key: re.compile(fields[key])}) for key in fields]
        [fields_re.update({key: re.compile(optional_fields[key])}) for key in optional_fields]
        
        blank_re=re.compile("^\s+$")
        show_info=[]
        current_show={}
        for line in info_stream:
            for key in fields_re:
                a_match=fields_re[key].match(line)
                if a_match:
                    matched_field=a_match.groupdict()
                    # insert field with leading and trailing whitespace removed
                    [current_show.update({k:matched_field[k].strip()}) for k in matched_field]
                    
            # end when all optional and mandatory fields are read *or* when all mandatory fields have been read and a blank line is found:
            if  ( len(current_show.keys())==(len(fields.keys())+len(optional_fields)))  or blank_re.match(line) and len(current_show.keys())== len(fields.keys()):
                show_info+=[current_show]
                #self.shows+=[episode_factory(current_show)]
                current_show={}
        return show_info
    
    def parse(self, info_stream):
        file_info_list=self.read_log(info_stream)
        for file_info in file_info_list:    
            self.shows+=[episode_factory(file_info)]
        
        
if __name__ == '__main__':
    import sys
    p=IPlayerInfoParser()
    p.read_log(sys.stdin)
    for s in p.shows:
        s.cross_check_with_tvdb()
        print s
        
            
        