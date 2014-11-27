'''
Created on 18 Aug 2014

@author: khurley
'''

import info_parser.iplayer_info_parser
import library_record
import filing_assistant
import tvdb_filer

class Librarian(object):
    '''
    Responsible for identifying new files and initiating their storage
    '''


    def __init__(self):
        '''
        Constructor
        '''
        self.iplayer_parser=info_parser.iplayer_info_parser.IPlayerInfoParser()
        self.records=[]
        self.filing_assistant = filing_assistant.FilingAssistant()
    
    def is_a_new_record(self, a_record):
        # no matches in current list of records:
        return not a_record in self.records
    
    def look_for_new_files(self, info_stream):
        """ talk to the log parsers to see if there are any new files 
        
        Parsers for IPlayer, TVHeadend etc know how to look in their 
        respective logs to find episodes and movies. Librarian asks them
        to identify candidates for new files
        """
        
        iplayer_list = self.iplayer_parser.read_log(info_stream)
        for file_info in iplayer_list:
            a_record=library_record.LibraryRecord(file_info)
            if self.is_a_new_record(a_record):
                self.records+=[a_record]
                an_episode = info_parser.iplayer_info_parser.episode_factory(file_info)
                a_record.associate_episode(an_episode)
                    
        
        