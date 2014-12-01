'''
Created on 18 Aug 2014

@author: khurley
'''

import iplayer_info_parser
import htsp_info_parser
import library_record
import filing_assistant
import logging

class Librarian(object):
    '''
    Responsible for identifying new files and initiating their storage
    '''


    def __init__(self):
        '''
        Constructor
        '''
        self.iplayer_parser=iplayer_info_parser.IPlayerInfoParser()
        self.htsp_parser=htsp_info_parser.HTSPInfoParser()
        
        self.records=[]
        self.filing_assistant = filing_assistant.FilingAssistant()
    
    def is_a_new_record(self, a_record):
        # no matches in current list of records:
        return not a_record in self.records
    
    def look_for_new_files(self, iplayer_stream=None, htsp_stream=None):
        """ talk to the log parsers to see if there are any new files 
        
        Parsers for IPlayer, TVHeadend etc know how to look in their 
        respective logs to find episodes and movies. Librarian asks them
        to identify candidates for new files
        """
        
        if iplayer_stream is not None:
            parser=self.iplayer_parser
            raw_stream=iplayer_stream
            logging.debug("parsing iplayer stream")   
        else:
            parser=self.htsp_parser
            raw_stream=htsp_stream
            logging.debug("parsing htsp stream")   
            
        shows=parser.parse(raw_stream)
        for show_info in shows:
            logging.debug("found a show - %s"%show_info)
            a_record=library_record.LibraryRecord(show_info)
            if self.is_a_new_record(a_record):
                logging.debug("new record found")
                self.records+=[a_record]
                an_episode = parser.episode_factory(show_info)
                a_record.associate_episode(an_episode)            
