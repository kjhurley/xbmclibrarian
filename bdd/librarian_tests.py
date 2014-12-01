'''
Created on 1 Dec 2014

@author: kehurley
'''

import librarian

class librarian_tests(object):
    '''
    Implement user keywords for robot testing
    '''


    def __init__(self):
        '''
        Constructor
        '''
        self.lib=librarian.Librarian()
        self.recordings=None
        self.current_recording=None
        
    def prepare_data(self):
        """ get the test data ready """
        self.recordings=[{'description': "The Red Door: What is behind the mysterious red door in the IT department? What has happened to Moss's new mug? And why is Roy in danger of becoming known as a 'desk rabbit'?  [S]", 'title': 'The IT Crowd', 'stop': 1416873000, 'method': 'dvrEntryAdd', 'start': 1416871200, 'state': 'completed', 'path': '/The-IT-Crowd.2014-11-24.23-20.ts', 'id': 245, 'channel': 54},
 {'description': "The Anything Can Happen Recurrence: Penny and Leonard distract Sheldon from his career problems by reinstating Anything Can Happen Thursday. Raj asks for Howard's advice.  [AD,S]", 'title': 'The Big Bang Theory', 'stop': 1416753000, 'method': 'dvrEntryAdd', 'start': 1416751200, 'state': 'completed', 'path': '/The-Big-Bang-Theory.2014-11-23.14-00.ts', 'id': 243, 'channel': 54}                        
                    ]
        self.current_recording=self.recordings[1]
        return
    
    def is_data_refreshed(self):
        """ true if epg has been synched (or a mock-up is ready) """
        assert len(self.recordings)>0, "no recordings found"
    
    def is_there_a_new_recording(self):
        """ after the latest synch, was a new recording found """
        assert self.current_recording is not None, "current selected recording not set"
    
    def is_new_recording_a_tv_show(self):
        """ is a new recording found a tv show """
        assert True
    
    def new_recording_title_matches(self, given_title):
        actual_title="The Big Bang Theory"
        assert given_title == actual_title, "given title: <<%s>> doesn't match <<%s>>"%(given_title, actual_title)
        
    def does_new_recording_have_episode_title(self):
        """ can an episode title be extracted from the description for the new recording """
        assert True
    
    def is_there_a_match_in_tvdb(self):
        """ given an episode title can be extracted, can it be matched in tvdb """
        assert True
    
    def new_recording_season_and_episode_matches(self, season, episode):
        actual_season=1
        actual_episode=1
        season=int(season)
        episode=int(episode)
        assert (actual_episode,actual_season) == (season, episode), "season=%d, episode=%d doesn't match actual (%d,%d)"%(season,episode, actual_season, actual_episode)
