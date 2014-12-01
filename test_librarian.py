'''
Created on 18 Aug 2014

@author: khurley
'''
import unittest
import mock
import librarian
import logging

logging.getLogger().setLevel(logging.DEBUG)

class Test(unittest.TestCase):
    def setUp(self):
        self.librarian = librarian.Librarian()


    def tearDown(self):
        pass


    def test_look_for_new_files(self):
        """ see if the librarian can identify when a new file is added """
        info_stream="""blah blah blah"""
        with mock.patch("iplayer_info_parser.IPlayerInfoParser.parse") as parse:
            parse.return_value=[{'original':'first_file.flv'}]
            with mock.patch("iplayer_info_parser.IPlayerInfoParser.episode_factory") as factory, mock.patch('iplayer_info_parser.HorizonEpisode') as horizon_episode:
                self.librarian.look_for_new_files(iplayer_stream=info_stream)
                self.assertEqual(1,parse.call_count)
                horizon_episode.title="bananna"
                horizon_episode.tvdb_ok=True
                factory.return_value=horizon_episode
                self.assertEqual(1,factory.call_count)
                self.assertEqual(len(self.librarian.records),1)
                self.assertEqual(self.librarian.records[0].original_file_name,"first_file.flv")
    
    def test_look_for_new_files_duplicates(self):
        """ parsing the iplayer stream indicates 2 new files but one is a duplicate """
        info_stream="""blah blah blah"""
        with mock.patch("iplayer_info_parser.IPlayerInfoParser.parse") as parse:
            parse.return_value=[{'original':'first_file.flv'},{'original':'first_file.flv'}]
            with mock.patch("iplayer_info_parser.IPlayerInfoParser.episode_factory") as factory, mock.patch('iplayer_info_parser.HorizonEpisode') as horizon_episode:
                self.librarian.look_for_new_files(iplayer_stream=info_stream)
                self.assertEqual(1,parse.call_count)
                factory.return_value=horizon_episode
                self.assertEqual(1,factory.call_count)
                self.assertEqual(len(self.librarian.records),1)
                self.assertEqual(self.librarian.records[0].original_file_name,"first_file.flv")

if __name__ == "__main__":
    #import sys;sys.argv = ['', 'Test.test_look_for_new_files']
    unittest.main()