'''
Created on 2 Dec 2014

@author: kehurley
'''
import unittest
import library_record


class TestLibraryRecords(unittest.TestCase):
    def test_compare_two_records_different_filename(self):
        record1=library_record.LibraryRecord("foo.bar")
        record2=library_record.LibraryRecord("foo.baz")
        
        self.assertNotEqual(record1, record2)
        
    def test_compare_two_records_same_filename(self):
        record1=library_record.LibraryRecord("foo.bar")
        record2=library_record.LibraryRecord("foo.bar")
        
        self.assertEqual(record1, record2)
        
    def test_associate_episode(self):
        record1=library_record.LibraryRecord("foo.bar")
        self.assertEqual(str(record1), "<LibraryRecord original name = 'foo.bar', episode = 'None'>")
        
        episode="foo_1"
        record1.associate_episode(episode)
        
        self.assertEqual(str(record1), "<LibraryRecord original name = 'foo.bar', episode = 'foo_1'>")
        
        

if __name__ == "__main__":
    #import sys;sys.argv = ['', 'Test.test_create_library_record']
    unittest.main()