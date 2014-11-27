'''
Created on 18 Aug 2014

@author: khurley
'''

class TVDBFiler(object):
    '''
    How to file a show which can be looked up in TVDB
    
    Created using the library record
    '''


    def __init__(self,a_record):
        '''
        Constructor
        '''
        self.record=a_record
        
    def build_new_filename(self):
        the_episode=self.record.episode
        show_name,episode_title=the_episode.get_show_and_episode()
   
        return "newfilename"
    
    def original_file(self):
        return self.record.original_file_name
    
    