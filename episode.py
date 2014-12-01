'''
Created on 1 Dec 2014

@author: kehurley
'''

import tvdb_api
import tvdb_exceptions
import xml.etree.cElementTree as ET

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
        if self.episode_title_for_tvdb is None:
            return self.show_name_for_tvdb()
        elif not self.tvdb_ok:
            if self.episode_number != (None,None):
                return "%s;%s;s%02d.e%02d [tvdb=None]"%(self.show_name_for_tvdb(), self.episode_title_for_tvdb(),self.episode_number[0],self.episode_number[1])
            else:
                return "%s;%s"%(self.show_name_for_tvdb(), self.episode_title_for_tvdb())
        else:
            return "%s;%s;s%02d.e%02d [tvdb=%s]"%(self.show_name_for_tvdb(), self.episode_title_for_tvdb(), self.episode_number[0],self.episode_number[1],self.tvdb_ok)
        