'''
Created on 14 Aug 2014

@author: khurley



'''
import re
import logging
import episode

class DragonsRidersOfBerk(episode.Episode):
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
    
class HorizonEpisode(episode.Episode):
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
        
class DragonsDen(episode.Episode):
    @staticmethod
    def match_info(info_dict):
        """ test if info fields are a match for this Episode class """
        try:
            return info_dict['name']=="Dragons' Den"
        except KeyError:
            return False

class BakeOffExtraSlice(episode.Episode):
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
    

class IPlayerInfoParser(object):
    '''
    Reads the long info output by get_iplayer and builds objects representing individual shows
    '''


    def __init__(self):
        '''
        Constructor
        '''
        self.shows=[]
        
    def parse(self, info_stream):
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
                self.shows+=[current_show]
                #self.shows+=[episode_factory(current_show)]
                current_show={}

    @staticmethod
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
        return episode.Episode(show_name=episode_info['name'],episode_title=episode_info['title'],season_number=int(season_index),episode_number=int(episode_index))


        
if __name__ == '__main__':
    import sys
    p=IPlayerInfoParser()
    p.parse(sys.stdin)
    for s in p.shows:
        s.cross_check_with_tvdb()
        print s
        
            
        