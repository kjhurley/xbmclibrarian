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
        self.show=None
        
    def refresh_data(self):
        self.show=self.tvdb[self.episode.show_name]
        assert self.show is not None, "no show matching the show name for this episode"
        
    def narrow(self, terms):
        """ apply info to narrow
        
        if called with no params then just use info in episode object to narrow
        
        updates the matches list 
        
        @param terms - list of strings to search for
        
        @return: the list of matching tvdb episode objects
        
        """
        if self.show is None:
            self.refresh_data()
        matches=None
        for term in terms:
            if matches is None:
                matches=set([e for e in self.show.search(term)])
            else:
                len_current_matches=len(matches)   
                episodes=set([e for e in self.show.search(term)])
                print "term =",term,"; episodes=",episodes
                if len(episodes)>0:
                    if matches.isdisjoint(episodes):
                        matches=matches | episodes
                    else:
                        matches = matches & episodes 
                print "matches =", matches
        return matches