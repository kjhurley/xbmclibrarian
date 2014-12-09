'''
Created on 18 Aug 2014

@author: khurley
'''
import re
import os.path

def remove_non_alphanumeric(in_str):
    return re.sub("[\W]","_",in_str.strip())

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
        """ generate file name - path relative to TVShow top """
        the_episode=self.record.episode
        show_name,episode_title=the_episode.get_show_and_episode()
        folder_name=remove_non_alphanumeric(show_name)
        episode_file_name= remove_non_alphanumeric(episode_title)
   
        new_suffix=os.path.splitext(self.record.original_file_name)[-1]
   
        return os.path.join(folder_name, episode_file_name+new_suffix)
    
    def original_file(self):
        return self.record.original_file_name
    
    