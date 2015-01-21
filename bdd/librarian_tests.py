'''
Created on 1 Dec 2014

@author: kehurley
'''

import librarian
import tvdb_api
import episode
import logging
import configuration
import manual_matcher

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
        
    def update_data(self, filename):
        # read in epg dump data for TVH
        htsp_msg_list=[]
        with open(filename) as a_file:
            for line in a_file.readlines():
                if 'dvrEntryAdd' in line:
                    htsp_msg_list+=[eval(line)]
        return htsp_msg_list
        
    def load_first_data(self):
        """ prepare initial data """
        # configure web proxy environment: 
        cfg=configuration.Configuration()
        cfg.parse_config_file()
        cfg.apply()
        htsp_msg_list=self.update_data("bdd/epg.dump")
        self.old_num_recordings=len(self.lib.records)
        self.lib.look_for_new_files(htsp_stream=htsp_msg_list)
        # get list of epidodes from the records list held by self.lib
        self.recordings=[rec.episode for rec in self.lib.records]
        self.current_recording = self.recordings[0]
        
    def load_second_data(self):
        htsp_msg_list=self.update_data("bdd/epg_update.dump")
        self.old_num_recordings=len(self.lib.records)
        self.lib.look_for_new_files(htsp_stream=htsp_msg_list)
        self.current_recording=self.lib.records[-1].episode
        
    def load_third_data(self):
        htsp_msg_list=self.update_data("bdd/epg_third_update.dump")
        self.old_num_recordings=len(self.lib.records)
        self.lib.look_for_new_files(htsp_stream=htsp_msg_list)
        self.current_recording=self.lib.records[-1].episode
    
    def is_data_refreshed(self):
        """ true if epg has been synched (or a mock-up is ready) """
        assert len(self.recordings)>0, "no recordings found"
    
    def is_there_a_new_recording(self):
        """ after the latest synch, was a new recording found """
        assert self.old_num_recordings!=len(self.lib.records), "%d old recordings - %d new recordings"%(self.old_num_recordings,len(self.lib.records))
        assert self.current_recording is not None, "current selected recording not set"
    
    def is_new_recording_a_tv_show(self):
        """ is a new recording found a tv show """
        assert True
    
    def new_recording_title_matches(self, given_title):
        actual_title=self.current_recording.show_name_for_tvdb()
        assert given_title == actual_title, "given title: <<%s>> doesn't match <<%s>>"%(given_title, actual_title)
        
    def does_new_recording_have_episode_title(self):
        """ can an episode title be extracted from the description for the new recording """
        assert self.current_recording.episode_title_for_tvdb() is not None, "episode = %s"%self.current_recording
    
    def env_variables_for_tvdb(self):
        pass
    
    def is_there_a_match_in_tvdb(self):
        """ given an episode title can be extracted, can it be matched in tvdb """
        logging.getLogger().setLevel(logging.DEBUG)
        try:
            a_tvdb=tvdb_api.Tvdb()
            self.current_recording.cross_check_with_tvdb(a_tvdb)
            return True
        except (episode.NoMatchingEpisodesError, episode.NoMatchingShowsError, episode.MultipleMatchingEpisodesError):
            return False
                
    
    def new_recording_season_and_episode_matches(self, season, episode):
        actual_episode=1
        season=int(season)
        episode=int(episode)
        assert self.current_recording.episode_number == (season, episode), "season=%d, episode=%d doesn't match actual %s"%(season,episode, self.current_recording.episode_number)


    def select_a_tvh_recording(self, index):
        """ select current recording from recording list """
        logging.debug("recording list = %s"%self.lib.records)
        self.current_recording = self.lib.records[int(index)]
        logging.debug("selected %s"%self.current_recording)
        
    def expect_number_of_matches_using(self, num_expected_matches, *args):  
        a_tvdb=tvdb_api.Tvdb()
        m=manual_matcher.ManualEpisodeMatcher(self.current_recording.episode, a_tvdb)
        if len(args)>0:
            search_term = args[0]
        matches=m.narrow([search_term])
        num_expected_matches=int(num_expected_matches)
        assert num_expected_matches == len(matches), "expected %d matches, got %d"%(num_expected_matches, len(matches))
        for ep_match in matches:
            print ep_match, ": overview =", ep_match.get('overview')
        
        
