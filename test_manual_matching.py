'''
Created on 11 Dec 2014

@author: kehurley
'''
import unittest
import mock
import htsp_info_parser
import manual_matcher

class Test(unittest.TestCase):
    def setUp(self):
        self.p=htsp_info_parser.HTSPInfoParser()
        
    def test_time_team_one_filter(self):
        recordings=[{'description': "Tony Robinson and the Team have three days to uncover a Norman castle that once dominated the Midlands village of Henley-in-Arden.  [S]", 'title': 'Time Team', 'stop': 1416873000, 'method': 'dvrEntryAdd', 'start': 1416871200, 'state': 'completed', 'path': '/Time-Team.2014-11-24.23-20.ts', 'id': 245, 'channel': 54}
                    ]
        self.p.parse(recordings)
        the_episode=self.p.episode_factory(self.p.shows[0])
        print the_episode
        self.assertEqual(the_episode.show_name,"Time Team")
        self.assertEqual(the_episode.episode_title,None)
        self.assertEqual(the_episode.details[:37], "Tony Robinson and the Team have three")

        tvdb=mock.MagicMock()
        matcher=manual_matcher.ManualEpisodeMatcher(the_episode, tvdb)
        


if __name__ == "__main__":
    #import sys;sys.argv = ['', 'Test.test_time_team_one_filter']
    unittest.main()