'''
Created on 14 Aug 2014

@author: khurley

'''
import re
import tvdb_api
import tvdb_exceptions
import htsp.htsprefresh
import xml.etree.cElementTree as ET
import logging

#logging.getLogger().setLevel(logging.DEBUG)
class Episode(object):
    @staticmethod
    def match_info(info_dict):
        """ test if info fields are a match for this Episode class """
        return True
    
    def __init__(self, show_name, episode_title=None, season_number=None, episode_number=None):
        self.show_name=show_name
        self.episode_title=episode_title
        self.episode_number=(season_number,episode_number)
        self.tvdb_ok=None # None if not checked, True if show and episode titles match
    
    def cross_check_with_tvdb(self):
        self.tvdb_ok=False  
        try:
            tv=tvdb_api.Tvdb()
        except tvdb_exceptions.tvdb_exception:
            logging.error("couldn't initialise tvdb!")
            self.tvdb_ok=None
            return
        try:
            show_name=self.show_name_for_tvdb()
            the_show=tv[show_name]
        except tvdb_exceptions.tvdb_exception:
            logging.warn("tvdb show lookup failed - %s!"%show_name)
            return
        try:
            ep_title=self.episode_title_for_tvdb()
            search_result=the_show.search(ep_title)
        except tvdb_exceptions.tvdb_exception:
            logging.warn( "tvdb episode lookup failed: %s / %s!"%(show_name, ep_title))
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
        if self.episode_title_for_tvdb is None:
            return self.show_name_for_tvdb()
        elif not self.tvdb_ok:
            return "%s;%s"%(self.show_name_for_tvdb(), self.episode_title_for_tvdb())
        else:
            return "%s;%s;s%02d.e%02d [tvdb=%s]"%(self.show_name_for_tvdb(), self.episode_title_for_tvdb(), self.episode_number[0],self.episode_number[1],self.tvdb_ok)

def episode_factory(recording_info):
    """ use dict representing recording_info to choose episode class and
    create an instance of Episode
    """
    if 'episode_title' in recording_info:
        return Episode(recording_info['title'], recording_info['episode_title'])
    else: 
        return Episode(recording_info['title'])

class DescriptionParser(object):
    def __init__(self, description):
        self.details=description

    def description_starts_with_episode_title(self):
        title_and_details_regex=re.compile("^(?P<title>([A-Z]\S+\s*)+): (?P<details>.*)$")
        self.match=title_and_details_regex.search(self.details)
        return self.match is not None
    
    def extract_episode_title_from_description(self):
        assert self.match is not None
        return self.match.group('title')
    
    def extract_details_from_description(self):
        """ if title matched at start then return the rest else return all of it """
        if self.match is not None:
            return self.match.group('details')
        else:
            return self.details
       
class HTSPInfoParser(object):
    '''
    Reads the htsp epg dump and build objects representing individual shows
    '''


    def __init__(self):
        '''
        Constructor
        '''
        self.shows=[]
        
    def read_log(self, recordings):
        """ read through the whole stream building the list of shows 
        
        Initially populate dictionaries built from the fields in the info stream
        
        """
        
        show_info=[]
        current_show={}
        for recording in recordings:
            if recording['state']=='completed':
                current_show={
                    'title': recording['title']
                    }
                parser=DescriptionParser(recording['description'])
                if parser.description_starts_with_episode_title():
                    current_show['episode_title']=parser.extract_episode_title_from_description()
                    current_show['details']=parser.extract_details_from_description()
                else:
                    current_show['details']=recording['description']
                    current_show['episode_title']=None
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
    p=HTSPInfoParser()
    recordings=htsp.htsprefresh.refresh("192.168.1.78")
    p.parse(recordings)
    print p.shows
    if False:
        for s in p.shows:
            s.cross_check_with_tvdb()
            print s
        
            
        