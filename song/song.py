'''
Song Module, Defines classes to represent songs in the library and infomation
about them
'''

import os
import sys
from data.DB_Helper import DB_Helper

class Song:

    def __init__(self, filePath, attributes, moods):
        '''
        Constructor
        '''
        
        self.filepath = filePath
        self.file = Song._file_from_path(filePath)
        self.moods = moods
        self.attr = attributes

    @staticmethod
    def song_from_filepath(filepath):
        '''
        Returns a new song object using the given filepath
        '''
        moods = Song._find_moods(filepath)
        attributes = Song._find_attr(filepath)

        return Song(filepath, attributes, moods)

    def get_moods(self):
        '''
        Get stored song moods
        '''
        return self.moods

    @staticmethod
    def _find_moods(filepath):
        '''
        Gets moods from DB based on filepath
        '''
        return DB_Helper().moods_for_filepath(filepath)

    def add_mood(self, newMood):
        '''
        Add a new mood for this song
        '''
        self.moods.append(newMood)
        DB_Helper().add_mood(self.filepath, newMood)

    def get_attr(self):
        '''
        Returns song attributes
        '''
        return self.attr;

    @staticmethod
    def _find_attr(filepath):
        '''
        First checks the DB for attributes
        If it doesn't find the song in the db, get the attributes from echonest and save song to db
        '''
        attributes = DB_Helper().attributes_for_filepath(filepath)

        if len(attributes) > 0:
            return attributes
        else:
            # @todo: fetch data from echonest and persist them
            return {'No data in DB for this song':'it hasn\'t been imported yet'}

    @staticmethod
    def _file_from_path(filePath):
        '''
        Check to see if a file is readable, if not exits with error code 1
        
        @note: We can probably skip this step since we use the importer now and
        it check these kinds of stuff
        '''
        
        songFile = os.path.expanduser(filePath)
        if not os.access(songFile, os.R_OK):
            print('Error: %s file not readable' % songFile)
            sys.exit(1)
        return songFile