#! /usr/bin/python
# Song object

import os
import sys
from data.DB_Helper import DB_Helper

class Song:

    def __init__(self, filePath, attributes, moods):
        self.filepath = filePath
        self.file = Song._file_from_path(filePath)
        self.moods = moods
        self.attr = attributes

    @staticmethod
    #Returns a new song with the given filepath
    def song_from_filepath(filepath):
        moods = Song._find_moods(filepath)
        attributes = Song._find_attr(filepath)

        return Song(filepath, attributes, moods)

    def get_moods(self):
        return self.moods

    @staticmethod
    #Gets moods from DB
    def _find_moods(filepath):
        return DB_Helper().moods_for_filepath(filepath)

    #User adds mood to DB
    def add_mood(self, newMood):
        self.moods.append(newMood)
        DB_Helper().add_mood(self.filepath, newMood)

    def get_attr(self):
        return self.attr;

    @staticmethod
    #First checks the DB for attributes
    #If it doesn't find the song in the db, get the attributes from echonest and save song to db
    def _find_attr(filepath):
        attributes = DB_Helper().attributes_for_filepath(filepath)

        if len(attributes) > 0:
            return attributes
        else:
            #Use echonest if no entry in db
            return {'No data in DB for this song':'it hasn\'t been imported yet'}

    @staticmethod
    def _file_from_path(filePath):
        songFile = os.path.expanduser(filePath)
        if not os.access(songFile, os.R_OK):
            print('Error: %s file not readable' % songFile)
            sys.exit(1)
        return songFile