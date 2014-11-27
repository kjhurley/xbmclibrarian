'''
Created on 14 Aug 2014

@author: khurley



'''
import re
import tvdb_api
import tvdb_exceptions
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

class DragonsRidersOfBerk(Episode):
    @staticmethod
    def match_info(info_dict):
        """ test if info fields are a match for this Episode class """
        try:
            return info_dict['name']=='Dragons - Riders of Berk'
        except KeyError:
            return False
    
    def show_name_for_tvdb(self):
        " tvdb expects the name to be Dragons rather than Dragons: Riders of Berk"
        return "Dragons"
    
    def episode_title_for_tvdb(self):
        """ convert 'Part N' into (N)
        """
        
        # strip out the year from the episode title:
        return re.sub('(Part )(?P<part>\d+)','(\g<part>)',self.episode_title)
    
class HorizonEpisode(Episode):
    @staticmethod
    def match_info(info_dict):
        """ test if info fields are a match for this Episode class """
        try:
            return info_dict['name']=='Horizon'
        except KeyError:
            return False
    
    def episode_title_for_tvdb(self):
        """ iplayer puts year: at start of episode title """
        # strip out the year from the episode title:
        return ':'.join(self.episode_title.split(':')[1:]).strip()
        
class DragonsDen(Episode):
    @staticmethod
    def match_info(info_dict):
        """ test if info fields are a match for this Episode class """
        try:
            return info_dict['name']=="Dragons' Den"
        except KeyError:
            return False

class BakeOffExtraSlice(Episode):
    @staticmethod
    def match_info(info_dict):
        """ test if info fields are a match for this Episode class """
        try:
            return info_dict['title']=="An Extra Slice"
        except KeyError:
            return False
    
    def show_name_for_tvdb(self):
        " tvdb expects the name to be Dragons rather than Dragons: Riders of Berk"
        return "The Great British Bake Off: An Extra Slice"
    
    def episode_title_for_tvdb(self):
        """ convert 'Part N' into (N)
        """
        
        # strip out the year from the episode title:
        return "Episode %d"%self.episode_number[1]

def episode_factory(episode_info):
    """ take the dictionary parsed from iplayer info fields and create an episode """
    logging.debug("episode_factory(info=%s)"%episode_info)
    try:
        senum=episode_info['senum']
        season_episode_match=re.compile('s(\d+)e(\d+)').match(senum)
        season_index,episode_index=season_episode_match.groups()
    except KeyError:
        # senum missing
        logging.warning("senum missing from episode info")
        season_index,episode_index=0,0
            
    
    specials=[HorizonEpisode, DragonsRidersOfBerk, DragonsDen, BakeOffExtraSlice
              ]
    for episode_class in specials:
        if episode_class.match_info(episode_info):
            return episode_class(episode_info['name'],episode_info['title'],int(season_index),int(episode_index))
    return Episode(episode_info['name'],episode_info['title'],int(season_index),int(episode_index))
    

class IPlayerInfoParser(object):
    '''
    Reads the long info output by get_iplayer and builds objects representing individual shows
    '''


    def __init__(self):
        '''
        Constructor
        '''
        self.shows=[]
        
    def read_log(self, info_stream):
        """ read through the whole stream building the list of shows 
        
        Initially populate dictionaries built from the fields in the info stream
        
        """
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
        
            
        