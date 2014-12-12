'''
Created on 11 Dec 2014

@author: kehurley
'''
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
        self.tvdb=tvdb
        self.episode=episode
        self.matches=None # candidate matches so far
        
    def clear(self):
        self.show=self.tvdb[self.episode.show_name]
        assert self.show is not None, "no show matching the show name for this episode"
        
        self.matches=None
        
    def narrow(self, **kwargs):
        """ apply info to narrow
        
        if called with no params then just use info in episode object to narrow
        
        @param term - string to search for
        @param key - only search in this key
        @param season - season number to try
        """
        if self.matches is None:
            self.matches=set([e for e in self.show.search(**kwargs)])
        else:
            len_current_matches=len(self.matches)   
            episodes=set([e for e in self.show.search(**kwargs)])
            print episodes
            if len(episodes)>0:
                if self.matches.isdisjoint(episodes):
                    self.matches=self.matches | episodes
                else:
                    self.matches = self.matches & episodes 
        