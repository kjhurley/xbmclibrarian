'''
Created on 18 Aug 2014

@author: khurley
'''

import shutil
#import os


COPY_RULE=0
MOVE_RULE=1
LINK_RULE=2

def copy_old_to_new(old, new):
    shutil.copyfile(old, new)

def move_old_to_new(old, new):
    shutil.move(old, new)

def link_old_to_new(old, new):
    raise RuntimeError("not available in windows")
    #.symlink(old, new)

STORAGE_RULE_FUNCTION={
                       COPY_RULE: copy_old_to_new,
                       MOVE_RULE: move_old_to_new,
                       LINK_RULE: link_old_to_new
                       }

class FilingAssistant(object):
    '''
    Responsible for storing new files using the right rules and information
    '''


    def __init__(self, storage_rule=COPY_RULE):
        '''
        Constructor
        
        default is to create a copy of the original file
        '''
        self.rule=storage_rule
    
    def put_new_file_in_right_location(self, filer):
        """ work with the filer to store the new file using the right rules 
        
        Files can be stored by copying, moving or linking.
        
        The old and new filenames are determined by the filer from its library
        record member. 
        
        """
        old_name=filer.original_file()
        new_name=filer.build_new_filename()
        
        STORAGE_RULE_FUNCTION[self.rule](old_name, new_name)
        
        return
    
    