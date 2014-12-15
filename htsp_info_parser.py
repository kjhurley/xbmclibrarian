'''
Created on 14 Aug 2014

@author: khurley

'''
import re
import htsp.htsprefresh
import episode
import logging
import library_record

#logging.getLogger().setLevel(logging.DEBUG)

class ShowTitleParser(object):
    def __init__(self, title_text):
        self.text=title_text
        self.title=None
        
    def parse(self):
        skip_new_regex=re.compile("((Brand|BRAND)?\s?(New|NEW)\s?(:|-)*\s+)?(?P<title>.*)$")
        match=skip_new_regex.search(self.text)
        if match is not None:
            self.title=match.group('title')
        else:
            self.title=self.text    

class DescriptionParser(object):
    def __init__(self, description):
        self.text=description
        self.details=None
        self.episode_title=None
        self.episode_number=None
        self.new_ep_re=re.compile("Brand new series - (?P<the_rest>.*)")
        self.episode_number_re=re.compile("(?P<episode_number>\d+)\/\d+\.\s+(?P<the_rest>.*)")
        self.episode_title_re=re.compile("(?P<title>([A-Z]\S+\s*)+):\s+(?P<the_rest>.*)")

    def parse(self):
        logging.debug("text="+self.text)
        if self.new_ep_re.match(self.text):
            self.text=self.new_ep_re.match(self.text).group('the_rest')
            logging.debug("Remove brand new ... text="+self.text)
        if self.episode_number_re.match(self.text):
            self.episode_number=int(self.episode_number_re.match(self.text).group('episode_number'))
            self.text=self.episode_number_re.match(self.text).group('the_rest')
            logging.debug("Removed episode number ... text="+self.text)
        if self.episode_title_re.match(self.text):
            self.episode_title=self.episode_title_re.match(self.text).group('title')
            self.text=self.episode_title_re.match(self.text).group('the_rest')
            logging.debug("Removed episode title ... text="+self.text)
        
        # skip 'new' or 'band new' style prefix to the episode title
        details_regex=re.compile("^(?P<details>.*)$")
        self.match=details_regex.match(self.text)
        if self.match is not None:
            self.details=self.match.group('details')
        else:
            self.details=self.text
        return self.details is not None
    
    def extract_episode_title_from_description(self):
        assert self.episode_title is not None
        return self.episode_title
    
    def extract_details_from_description(self):
        """ if title matched at start then return the rest else return all of it """
        if self.details is not None:
            return self.details
        else:
            return self.text
       
class HTSPInfoParser(object):
    '''
    Reads the htsp epg dump and build objects representing individual shows
    '''

    def __init__(self):
        '''
        Constructor
        '''
        self.shows=[]
        
    def parse(self, recordings):
        """ read through the whole stream building the list of shows 
        
        Initially populate dictionaries built from the fields in the info stream
        
        """
        
        show_info=[]
        current_show={}
        for recording in recordings:
            logging.debug("examinging record %s"%recording)
            if recording['state']=='completed':
                title_parser=ShowTitleParser(recording['title'])
                title_parser.parse()
                current_show={
                    'title': title_parser.title,
                    'path': recording['path']
                    }
                parser=DescriptionParser(recording['description'])
                logging.debug("parsed into %s"%parser)
                if parser.parse():
                    current_show['episode_title']=parser.episode_title
                    current_show['details']=parser.details
                    current_show['episode_number']=parser.episode_number
                    logging.debug("extracted episode title")
                else:
                    current_show['details']=recording['description']
                    current_show['episode_title']=None
                    logging.debug("no episode title")
                self.shows+=[current_show]
                logging.debug("added %s"%current_show)
                #self.shows+=[episode_factory(current_show)]
                current_show={}
        return self.shows

    @staticmethod
    def episode_factory(recording_info):
        """ use dict representing recording_info to choose episode class and
        create an instance of Episode
        """
        if 'episode_title' in recording_info:
            return episode.Episode(show_name=recording_info['title'], episode_title=recording_info['episode_title'], details=recording_info["details"], episode_number=recording_info['episode_number'])
        else: 
            return episode.Episode(show_name=recording_info['title'], details=recording_info["details"], episode_number=recording_info['episode_number'])
        
    @staticmethod
    def library_record_factory(recording_info):
        return library_record.LibraryRecord(recording_info["path"])
        
if __name__ == '__main__':
    p=HTSPInfoParser()
    recordings=htsp.htsprefresh.refresh("192.168.1.78")
    p.parse(recordings)
    print p.shows
    if False:
        for s in p.shows:
            s.cross_check_with_tvdb()
            print s
        
            
        