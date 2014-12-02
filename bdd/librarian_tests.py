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
        htsp_msg_list=[]
        filename="bdd/epg.dump"
        with open(filename) as a_file:
            for line in a_file.readlines():
                htsp_msg_list+=[eval(line)]
        self.lib.look_for_new_files(htsp_stream=htsp_msg_list)
        # get list of epidodes from the records list held by self.lib
        self.recordings=[rec.episode for rec in self.lib.records]
    
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
