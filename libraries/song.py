#! /usr/bin/python
# Song object

import os
import sys

class Song:

    def __init__(self, filePath):
        self.filePath = filePath
        self.file = Song.file_from_path(filePath)
        self.moods = ['Happy', 'Sad']

    def get_moods(self):
        return self.moods

    def add_mood(self, newMood):
        self.moods.append(newMood)
        #TODO: make connection in db

    @staticmethod
    def file_from_path(filePath):
        songFile = os.path.expanduser(filePath)
        if not os.access(songFile, os.R_OK):
            print('Error: %s file not readable' % songFile)
            sys.exit(1)
        return songFile