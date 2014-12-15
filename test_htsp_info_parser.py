'''
Created on 28 Nov 2014

@author: kevin
'''
import logging
import unittest
import htsp_info_parser

class TestShowTitleParser(unittest.TestCase):
    def test_brand_new(self):
        title_text_list=["BRAND NEW - The big bang", "New: The big bang",
                         "NEW - The big bang", "BRAND NEW - The big bang"]
        for t in title_text_list:
            parser=htsp_info_parser.ShowTitleParser(t)
            parser.parse()
            self.assertEqual(parser.title, "The big bang")

class TestParsingDetails(unittest.TestCase):

    def helper(self, text, title, details):
        parser=htsp_info_parser.DescriptionParser(text)
        self.assertTrue(parser.parse())
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
        self.assertEqual(parser.extract_details_from_description(),
                         description)
        
    def test_parse_text_with_title_and_episode_number(self):
        description="2/3. The Golden Age: Alastair Sooke explores the sumptuous treasures of the golden age of Egyptian art. Also in HD. [S]"
        details="Alastair Sooke explores the sumptuous treasures of the golden age of Egyptian art. Also in HD. [S]"
        parser=htsp_info_parser.DescriptionParser(
                     description)
        self.assertTrue(parser.parse())
        self.assertEqual(parser.episode_number, 2)
        self.assertEqual(parser.details,
                         details)
         
    def test_parse_text_with_new_in_title(self):
        description="Brand new series - The Itchy Brain Simulation: A worried Leonard thinks. Also in HD. [S]"
        details="A worried Leonard thinks. Also in HD. [S]"
        parser=htsp_info_parser.DescriptionParser(
                     description)
        self.assertTrue(parser.parse())
        self.assertEqual(parser.episode_title, "The Itchy Brain Simulation")
        self.assertEqual(parser.details,
                         details)
        
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
       
    def test_read_single_recording_for_new_series(self):
        recordings=[{'description': "Brand new series - The Itchy Brain Simulation: A worried Leonard thinks [S]", 'title': 'New: The Big Bang Theory', 'stop': 1416873000, 'method': 'dvrEntryAdd', 'start': 1416871200, 'state': 'completed', 'path': '/The-IT-Crowd.2014-11-24.23-20.ts', 'id': 245, 'channel': 54}
                    ]
        self.p.parse(recordings)
        self.assertEqual(self.p.shows[0]['title'],"The Big Bang Theory")
        self.assertEqual(self.p.shows[0]['episode_title'],"The Itchy Brain Simulation")
        
    def test_get_title(self):
        recordings=[{'description': "Brand new series - 3/3. Visiting the great mosques and palaces built by the Ottoman emperors, Simon Sebag Montefiore looks at how Istanbul became the imperial capital and Islam's most powerful city. Also in HD. [AD,S]", 'title': 'Byzantium: A Tale of Three Cities', 'stop': 1387937100, 'method': 'dvrEntryAdd', 'start': 1387933500, 'state': 'completed', 'path': '/Byzantium_-A-Tale-of-Three-Cities.2013-12-25.01-05.mkv', 'id': 20, 'channel': 80}
                    ]
        self.p.parse(recordings)
        self.assertEqual(self.p.shows[0]['title'],"Byzantium: A Tale of Three Cities")
        self.assertEqual( self.p.shows[0]['episode_title'], None)
        self.assertEqual( self.p.shows[0]['episode_number'], 3)
        
if __name__ == "__main__":
    #import sys;sys.argv = ['', 'Test.testName']
    unittest.main()