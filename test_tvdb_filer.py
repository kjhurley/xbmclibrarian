'''
Created on 9 Dec 2014

@author: kehurley
'''
import unittest
import mock
import filer
import episode


class Test(unittest.TestCase):

    def test_simple_episode(self):
        episode_mock_config={'get_show_and_episode.return_value':("show title","The funny episode")}
        an_episode=mock.MagicMock(spec=episode.Episode, **episode_mock_config)
        a_record=mock.MagicMock()
        a_record.episode=an_episode
        a_record.original_file_name = "foo_bar.ts"
        a_filer=filer.EpisodeFiler(a_record)
        new_name=a_filer.build_new_filename()
        self.assertTrue(an_episode.get_show_and_episode.called)
        self.assertEqual(new_name, "show_title\\The_funny_episode.ts")


if __name__ == "__main__":
    #import sys;sys.argv = ['', 'Test.test_simple_episode']
    unittest.main()