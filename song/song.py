#! /usr/bin/python
# Song object

import os
import sys

class Song:

    def __init__(self, filePath):
        self.filePath = filePath
        self.file = Song._file_from_path(filePath)
        self.moods = self._find_moods()
        self.attr = self._find_attr()

    def get_moods(self):
        return self.moods

    #Gets moods from DB
    def _find_moods(self):
        return ['Happy', 'Sad']
        #TODO: add DB stuff

    #User adds mood to DB
    def add_mood(self, newMood):
        self.moods.append(newMood)
        #TODO: make connection in db

    def get_attr(self):
        return self.attr;

    #First checks the DB for attributes
    #If it doesn't find the song in the db, get the attributes from echonest and save song to db
    def _find_attr(self):
        return {'test1':'value', 'test2':5}
        #TODO: add DB stuff

    @staticmethod
    def _file_from_path(filePath):
        songFile = os.path.expanduser(filePath)
        if not os.access(songFile, os.R_OK):
            print('Error: %s file not readable' % songFile)
            sys.exit(1)
        return songFile