'''
Created on 11 Dec 2014

@author: kehurley
'''
from episode import Episode

class ManualEpisodeMatcher(object):
    '''
    help to find a manual match by narrowing search of online data
    
    
     @param episode: the episode object for the show we are trying to match
     @param tvdb: instance of the Tvdb api interface class  
    '''


    def __init__(self, episode, tvdb):
        '''
        Constructor
        '''
        self.episode=episode
        self.matches=[] # candidate matches so far
        self.filter={} # inputs used to narrow search so far
        
    def narrow(self, **kwargs):
        """ apply info to narrow
        
        if called with no params then just use info in episode object to narrow
        
        @param show - show title
        @param keywords - significant words
        @param season - season number to try
        """
        
        