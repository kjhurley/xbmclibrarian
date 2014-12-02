'''
Created on 1 Dec 2014

@author: kehurley
'''
import unittest
import episode
import mock
import tvdb_api
import tvdb_exceptions

#import logging
#logging.getLogger().setLevel(logging.DEBUG)

class TestConvertingToNfo(unittest.TestCase):
    def test_episode_only_title(self):
        ep=episode.Episode("just a title")
        self.assertEqual(ep.show_name, "just a title")
        
        self.assertEqual(str(ep),"just a title;None")
        self.assertEqual(ep.convert_to_nfo(), """<?xml version='1.0' encoding='UTF-8'?>\n<episodedetails />""")


    def test_episode_title_and_episode_title(self):
        ep=episode.Episode("show title","the episode")
        
        self.assertEqual(str(ep),"show title;the episode")
        self.assertEqual(ep.show_name_for_tvdb(), "show title")
        self.assertEqual(ep.episode_title_for_tvdb(), "the episode")
        self.assertEqual(ep.convert_to_nfo(), """<?xml version='1.0' encoding='UTF-8'?>\n<episodedetails><title>the episode</title></episodedetails>""")


    def test_episode_with_title_and_details(self):
        plot="here a plot summary. not much happens"
        ep=episode.Episode("show title","the episode", details=plot)
        
        self.assertEqual(str(ep),"show title;the episode")
        self.assertEqual(ep.show_name_for_tvdb(), "show title")
        self.assertEqual(ep.episode_title_for_tvdb(), "the episode")
        self.assertEqual(ep.convert_to_nfo(), """<?xml version='1.0' encoding='UTF-8'?>\n<episodedetails><title>the episode</title><plot>%s</plot></episodedetails>"""%plot)
        
        
class TestEpisodeCrossCheckWithTvdb(unittest.TestCase):
    def test_show_and_episode_found(self):
        # the get method on episode object retrieves season and episode number depending on argument
        ep_attrs={'get.side_effect':lambda v: {'seasonnumber':3,'episodenumber':2}[v]}
        tvdb_episode=mock.Mock(spec=tvdb_api.Episode, **ep_attrs)
        
        show_attrs={'search.side_effect':lambda key: key=="the episode" and [tvdb_episode] or None}
        show=mock.Mock(spec=tvdb_api.Show, **show_attrs)
        with mock.patch("tvdb_api.Tvdb") as tv:
            tv.__getitem__.return_value=show
            plot="here a plot summary. not much happens"    
            ep=episode.Episode("show title","the episode", details=plot)
            ep.cross_check_with_tvdb(tv)
            self.assertEqual(ep.episode_number, (3,2))
            
            self.assertEqual(str(ep),'show title;the episode;s03.e02')
            
    def test_show_found_but_no_episode(self):
        def no_episode(x):
            raise tvdb_exceptions.tvdb_episodenotfound
        show_attrs={'search.side_effect': no_episode}
        show=mock.Mock(spec=tvdb_api.Show, **show_attrs)
        with mock.patch("tvdb_api.Tvdb") as tv:
            tv.__getitem__.return_value=show
            plot="here a plot summary. not much happens"    
            ep=episode.Episode("show title","the episode", details=plot)
            self.assertRaises(episode.NoMatchingEpisodesError, ep.cross_check_with_tvdb, tv)
            
            self.assertEqual(str(ep),'show title;the episode')
    
    
    def test_rainy_day_show_and_multiple_episodes(self):
        
        # the get method on episode object retrieves season and episode number depending on argument
        tvdb_episodes=[]
        episodes_by_season={}
        seasons={3:[2], 1:[5],2:[4]}
        for season in seasons:
            episodes_by_season[season]={}
            for ep in seasons[season]:
                ep_attrs={'get.side_effect':lambda v: {'seasonnumber':season,'episodenumber':ep}[v]}
                new_mock=mock.Mock(spec=tvdb_api.Episode, **ep_attrs)
                tvdb_episodes+=[new_mock]
                episodes_by_season[season][ep]=new_mock
        
        def match_episode(x):
            if x=="the episode":
                return tvdb_episodes
            else:
                raise tvdb_exceptions.tvdb_episodenotfound
            
        def get_season(season):
            return episodes_by_season[season]

        show_attrs={'search.side_effect': match_episode}
        mock_show=mock.MagicMock(spec=tvdb_api.Show, **show_attrs)
        mock_show.__getitem__.side_effect=get_season
        with mock.patch("tvdb_api.Tvdb") as tv:
            tv.__getitem__.return_value=mock_show
            plot="here a plot summary. not much happens"    
            ep=episode.Episode("show title","the episode", details=plot)
            self.assertRaises(episode.MultipleMatchingEpisodesError, ep.cross_check_with_tvdb, tv)
            self.assertEqual(ep.episode_number, (None,None))
            
            self.assertEqual(str(ep),'show title;the episode')
    
    def test_rainy_day_show_and_multiple_episodes_without_season_episode_catch_exception(self):
        
        # the get method on episode object retrieves season and episode number depending on argument
        tvdb_episodes=[]
        episodes_by_season={}
        seasons={3:[2], 1:[5],2:[4]}
        for season in seasons:
            episodes_by_season[season]={}
            for ep in seasons[season]:
                ep_attrs={'get.side_effect':lambda v: {'seasonnumber':season,'episodenumber':ep}[v]}
                new_mock=mock.Mock(spec=tvdb_api.Episode, **ep_attrs)
                tvdb_episodes+=[new_mock]
                episodes_by_season[season][ep]=new_mock
        
        def match_episode(x):
            if x=="the episode":
                return tvdb_episodes
            else:
                raise tvdb_exceptions.tvdb_episodenotfound
            
        def get_season(season):
            return episodes_by_season[season]

        show_attrs={'search.side_effect': match_episode}
        mock_show=mock.MagicMock(spec=tvdb_api.Show, **show_attrs)
        mock_show.__getitem__.side_effect=get_season
        with mock.patch("tvdb_api.Tvdb") as tv:
            tv.__getitem__.return_value=mock_show
            plot="here a plot summary. not much happens"    
            ep=episode.Episode("show title","the episode", details=plot)
            try:
                ep.cross_check_with_tvdb(tv)
            except episode.MultipleMatchingEpisodesError as err:
                self.assertEqual(err.matches, [episodes_by_season[1][5], episodes_by_season[2][4], episodes_by_season[3][2] ])
            self.assertEqual(str(ep),'show title;the episode')
                
    def test_rainy_day_show_and_multiple_episodes_with_season_episode_catch_exception(self):
        
        # the get method on episode object retrieves season and episode number depending on argument
        tvdb_episodes=[]
        episodes_by_season={}
        seasons={3:[2], 1:[5],2:[4]}
        for season in seasons:
            episodes_by_season[season]={}
            for ep in seasons[season]:
                ep_attrs={'get.side_effect':lambda v: {'seasonnumber':season,'episodenumber':ep}[v]}
                new_mock=mock.Mock(spec=tvdb_api.Episode, **ep_attrs)
                tvdb_episodes+=[new_mock]
                episodes_by_season[season][ep]=new_mock
        
        def match_episode(x):
            if x=="the episode":
                return tvdb_episodes
            else:
                raise tvdb_exceptions.tvdb_episodenotfound
            
        def get_season(season):
            try:
                return episodes_by_season[season]
            except KeyError:
                raise tvdb_exceptions.tvdb_seasonnotfound

        show_attrs={'search.side_effect': match_episode}
        mock_show=mock.MagicMock(spec=tvdb_api.Show, **show_attrs)
        mock_show.__getitem__.side_effect=get_season
        with mock.patch("tvdb_api.Tvdb") as tv:
            tv.__getitem__.return_value=mock_show
            plot="here a plot summary. not much happens"    
            ep=episode.Episode("show title","the episode", details=plot, season_number=6,episode_number=6)
            try:
                ep.cross_check_with_tvdb(tv)
            except episode.MultipleMatchingEpisodesError as err:
                self.assertEqual(err.matches, [episodes_by_season[1][5], episodes_by_season[2][4], episodes_by_season[3][2] ])
            self.assertEqual(str(ep),'show title;the episode;s06.e06')
            
            
class TestComparison(unittest.TestCase):
    def test_compare_episodes_that_only_have_show_title(self):
        ep1=episode.Episode("show1")
        ep2=episode.Episode("show2")
        
        self.assertNotEqual(ep1,ep2)
        
        ep3=episode.Episode("show1")
        self.assertEqual(ep1, ep3)
        
    def test_compare_episodes_that_have_show_and_episode_title_by_no_episode_number(self):
        ep1=episode.Episode("show1","episode 1")
        ep2=episode.Episode("show2","episode 2")
        
        # show titles differ
        self.assertNotEqual(ep1,ep2)
        
        ep3=episode.Episode("show1", "episode 1")
        self.assertEqual(ep1, ep3)
        
        # episode titles differ
        ep4=episode.Episode("show1","episode 2")
        self.assertNotEqual(ep1,ep4)
        
    def test_compare_episodes_that_have_show_and_episode_title_and_episode_number(self):
        ep1=episode.Episode("show1","episode 1",1,1)
        ep2=episode.Episode("show2","episode 2",1,2)
        
        # show titles differ
        self.assertNotEqual(ep1,ep2)
        
        ep3=episode.Episode("show1", "episode 1",1,1)
        self.assertEqual(ep1, ep3)
        
        # titles match but numbers differ (seasons)
        ep3=episode.Episode("show1", "episode 1",2,1)
        self.assertNotEqual(ep1, ep3)
        
        # titles match but numbers differ (episodes)
        ep3=episode.Episode("show1", "episode 1",1,2)
        self.assertNotEqual(ep1, ep3)
        
        # episode titles differ
        ep4=episode.Episode("show1","episode 2",1,2)
        self.assertNotEqual(ep1,ep4)
        
        
if __name__ == "__main__":
    #import sys;sys.argv = ['', 'Test.test_episode_constructor']
    unittest.main()