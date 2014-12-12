'''
Created on 11 Dec 2014

@author: kehurley
'''
import unittest
import mock
import htsp_info_parser
import manual_matcher
import tvdb_api

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

        import os
        os.environ["http_proxy"]="http://emea-proxy-pool.eu.alcatel-lucent.com:8000"
        os.environ["https_proxy"]="https://emea-proxy-pool.eu.alcatel-lucent.com:8000"
        tvdb=tvdb_api.Tvdb()
        matcher=manual_matcher.ManualEpisodeMatcher(the_episode, tvdb)
        matcher.clear()
        matcher.narrow(term="Norman", key='overview')
        self.assertEqual(len(matcher.matches), 14)
        match_repr=[str(ep) for ep in matcher.matches]
        print len(match_repr),":",match_repr
        last_match_len=len(matcher.matches)
        matcher.narrow(term="Castle", key='overview')
        self.assertTrue(len(matcher.matches)<last_match_len)
        print len(matcher.matches),":",[str(ep) for ep in matcher.matches]
        last_match_len=len(matcher.matches)
        matcher.narrow(term="Henley", key='overview')
        self.assertTrue(len(matcher.matches)>last_match_len)
        print len(matcher.matches),":",[str(ep) for ep in matcher.matches]
        last_match_len=len(matcher.matches)
        
        matcher.clear()
        matcher.narrow(term="Henley", key='overview')
        self.assertTrue(len(matcher.matches)==1)
        print len(matcher.matches),":",[str(ep) for ep in matcher.matches]
        
        


if __name__ == "__main__":
    #import sys;sys.argv = ['', 'Test.test_time_team_one_filter']
    unittest.main()