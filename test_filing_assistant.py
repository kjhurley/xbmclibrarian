'''
Created on 9 Dec 2014

@author: kehurley
'''
import unittest
import mock
import filing_assistant

class Test(unittest.TestCase):

    def test_copy_tvdb_file(self):
        filer=mock.MagicMock()
        f=filing_assistant.FilingAssistant()
        with mock.patch('shutil.copyfile') as copier_fn:
            f.put_new_file_in_right_location(filer)
        
            self.assertTrue(filer.build_new_filename.called)
            self.assertTrue(copier_fn.called)
    def test_move_tvdb_file(self):
        filer=mock.MagicMock()
        f=filing_assistant.FilingAssistant(filing_assistant.MOVE_RULE)
        with mock.patch('shutil.move') as move_fn:
            f.put_new_file_in_right_location(filer)
        
            self.assertTrue(filer.build_new_filename.called)
            self.assertTrue(move_fn.called)
            
    # not on windows        
    @unittest.skipIf(True, "skip on windows")        
    def test_link_tvdb_file(self):
        filer=mock.MagicMock()
        f=filing_assistant.FilingAssistant(filing_assistant.LINK_RULE)
        with mock.patch('os.symlink') as link_fn:
            f.put_new_file_in_right_location(filer)
            self.assertTrue(filer.build_new_filename.called)
            self.assertTrue(link_fn.called)

if __name__ == "__main__":
    #import sys;sys.argv = ['', 'Test.testName']
    unittest.main()