'''
Created on 1 Dec 2014

@author: kehurley
'''

import tvdb_exceptions
import xml.etree.cElementTree as ET
import logging
from pygments.lexers import other

class NoMatchingShowsError(Exception):
    pass

class NoMatchingEpisodesError(Exception):
    pass

class MultipleMatchingEpisodesError(Exception):
    def __init__(self, msg, matches):
        super(MultipleMatchingEpisodesError,self).__init__(msg)
        self.matches=matches

class Episode(object):
    """ base class - tv show without episode title, or season/episode number
    """
    @staticmethod
    def match_info(info_dict):
        """ test if info fields are a match for this Episode class 
        
        this is used by factory function when looking for best matching episode subclass
        """
        return True
    

    
    def __init__(self, show_name, episode_title=None, season_number=None, episode_number=None, details=None):
        self.show_name=show_name
        self.episode_title=episode_title
        self.episode_number=(season_number,episode_number)
        self.details=details
    
    def __eq__(self, other):
        """ compare by converting to string using __repr__ """
        return str(other) == str(self)
    
    def cross_check_with_tvdb(self, tvdb):
        try:
            the_show=tvdb[self.show_name_for_tvdb()]
        except tvdb_exceptions.tvdb_exception:
            raise NoMatchingShowsError("tvdb show lookup failed - %s"%self.show_name_for_tvdb())
        try:
            search_result=the_show.search(self.episode_title_for_tvdb())
            logging.debug("search returned %s"%search_result)
        except tvdb_exceptions.tvdb_exception:
            raise NoMatchingEpisodesError("tvdb episode lookup failed - %s:%s"%(self.show_name_for_tvdb(),self.episode_title_for_tvdb() ))

        if len(search_result)==0:
            raise NoMatchingEpisodesError("tvdb lookup for %s returned no matches"%self)
        
        if len(search_result)==1:
            matched_episode=search_result[0]
        elif len(search_result)>1:
            # try using season/episode to disambiguate
            if self.episode_number != (None,None):
                try:
                    matched_episode=the_show[self.episode_number[0]][self.episode_number[1]]
                except tvdb_exceptions.tvdb_exception:
                    raise MultipleMatchingEpisodesError("could not resolve multiple matches for %s"%self,search_result)
            else:
                raise MultipleMatchingEpisodesError("no episode numbers available to try resolving multiple matches for %s"%self,search_result)
        
        # update episode number using tvdb data
        self.episode_number=(int(matched_episode.get(u'seasonnumber')),int(matched_episode.get(u'episodenumber')))
            
    def convert_to_nfo(self):
        top=ET.Element('episodedetails')
        if self.episode_title is not None:
            title=ET.SubElement(top,"title")
            title.text=self.episode_title
            
        if self.details is not None:
            plot=ET.SubElement(top,"plot")
            plot.text=self.details
        
        return ET.tostring(top,"UTF-8")
            
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
        """ present string that shows maximum info - may include results of TVDB lookup """
        if self.episode_title_for_tvdb is None:
            return self.show_name_for_tvdb()
        elif self.episode_number == (None,None):
            return "%s;%s"%(self.show_name_for_tvdb(), self.episode_title_for_tvdb())
        else:
            return "%s;%s;s%02d.e%02d"%(self.show_name_for_tvdb(), self.episode_title_for_tvdb(),self.episode_number[0],self.episode_number[1])


def factory_from_tvdb(tvdb_episode):
    """ given a tvdb episode, create an Episode class """
    tvdb_show=tvdb_episode.season.show
    return Episode(show_name=tvdb_show["seriesname"], episode_title=tvdb_episode["episodename"], 
                   season_number=tvdb_episode["seasonnumber"], episode_number=tvdb_episode["episodename"])

        
class EpisodeWithTitle(Episode):
    pass
        