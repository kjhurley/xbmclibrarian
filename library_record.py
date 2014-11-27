'''
Created on 18 Aug 2014

@author: khurley
'''

class LibraryRecord(object):
    '''
    Keep info about tv shows used by Librarian in one place
    '''


    def __init__(self, file_info):
        '''
        Constructor
        '''
        self.original_file_name = file_info["original"]
        self.episode = None
        
    def associate_episode(self, episode):
        self.episode = episode
    
    def __eq__(self, other):
        return self.original_file_name == other.original_file_name
    
    def __ne__(self,other):
        return not self.__eq__(other)
    
    def __repr__(self):
        return "<LibraryRecord original name = '%s', episode = '%s'>"%(self.original_file_name,self.episode)
    