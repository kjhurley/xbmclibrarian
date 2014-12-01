'''
Created on 28 Nov 2014

@author: kevin
'''
import unittest
import htsp_info_parser

class TestParsingDetails(unittest.TestCase):

    def helper(self, text, title, details):
        parser=htsp_info_parser.DescriptionParser(text)
        self.assertTrue(parser.description_starts_with_episode_title())
        self.assertEqual(title,parser.extract_episode_title_from_description())
        self.assertEqual(details,parser.extract_details_from_description())
        
    def test_parse_very_simple_text(self):
        self.helper("The Title: A very short show.",
                    "The Title",
                    "A very short show.")
        
        self.helper("The Locomotive Manipulation: Love is in the air when Amy manages to convince Sheldon.",
                    "The Locomotive Manipulation",
                    "Love is in the air when Amy manages to convince Sheldon.")
        
    def test_parse_title_with_special_char(self):
        self.helper("Yesterday's Jam: In the very first episode, new recruit Jen is ... computers.  [S]",
                    "Yesterday's Jam",
                    "In the very first episode, new recruit Jen is ... computers.  [S]")

    def test_parse_text_with_no_title(self):
        description="Time team do stuff somewhere. It takes a while."
        parser=htsp_info_parser.DescriptionParser(
                     description)
        self.assertTrue(not parser.description_starts_with_episode_title())
        self.assertEqual(parser.extract_details_from_description(),
                         description)

class TestHTSPInfoParser(unittest.TestCase):
    def setUp(self):
        self.p=htsp_info_parser.HTSPInfoParser()
        
    def test_read_single_recording(self):
        recordings=[{'description': "The Red Door: What is behind the mysterious red door in the IT department? What has happened to Moss's new mug? And why is Roy in danger of becoming known as a 'desk rabbit'?  [S]", 'title': 'The IT Crowd', 'stop': 1416873000, 'method': 'dvrEntryAdd', 'start': 1416871200, 'state': 'completed', 'path': '/The-IT-Crowd.2014-11-24.23-20.ts', 'id': 245, 'channel': 54}
                    ]
        self.p.parse(recordings)
        self.assertEqual(self.p.shows[0]['title'],"The IT Crowd")
        self.assertEqual(self.p.shows[0]['episode_title'],"The Red Door")
        
        the_episode=self.p.episode_factory(self.p.shows[0])
        self.assertEqual(the_episode.show_name_for_tvdb(), "The IT Crowd")
        
if __name__ == "__main__":
    #import sys;sys.argv = ['', 'Test.testName']
    unittest.main()