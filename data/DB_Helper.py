#! /usr/bin/python
# Helper class for the DB methods

from song.song import *
from data.SqLite import SqLite, C
from data.DB_constants import *

class DB_Helper(object):

    #Singleton pattern
    _instance = None
    def __new__(cls, *args, **kwargs):
        if not cls._instance:
            cls._instance = super(DB_Helper, cls).__new__(
                                cls, *args, **kwargs)
        return cls._instance

    def __init__(self):
        self.db = SqLite();

    #Returns a dictionary of attributes for a song's filepath
    def attributes_for_filepath(self, filepath):
        self.db.setNamespace(songNamespace)
        songHash = DB_Helper._hash(filepath)

        #Get songdata from DB with hash
        self.db.search(C._raw("hash", "=", songHash)) 
        songData = self.db.read(1)

        #Removes non-attributes
        if songData != None:
            songData.pop(commonId, None)
            songData.pop(commonHash, None)
            songData.pop(songFilename, None)
            return songData
        else:
            return {}

    #Returns a list of moods for a given song's filepath
    def moods_for_filepath(self, filepath):
        self.db.setNamespace(moodNamespace)
        songHash = DB_Helper._hash(filepath)

        #Get moods from DB with hash
        self.db.search(C._raw(commonHash, "=", songHash))
        rawMoods = self.db.read()

        moods = []
        for rawMood in rawMoods:
            moods.append(rawMood[moodTitle])

        return moods

    #Returns all the moods that the user has created
    def all_moods(self):
        self.db.setNamespace(moodNamespace)

        #Get moods from DB with hash
        self.db.search()
        rawMoods = self.db.read()

        moods = []
        for rawMood in rawMoods:
            moods.append(rawMood[moodTitle])

        return moods

    #Adds the given mood for the song's filepath
    def add_mood(self, filepath, title):
        self.db.setNamespace(moodNamespace)
        songHash = DB_Helper._hash(filepath)

        #Adds mood to DB
        self.db.write({commonHash:songHash, moodTitle:title})

    #Gets all of the data out of the Song namespace (except for id and hash)
    def all_songs(self):
        self.db.setNamespace(songNamespace)
        songHash = DB_Helper._hash(filepath)

        #Get songdata from DB with hash
        self.db.search() 
        songData = self.db.read()

        #Removes id and hash
        for song in songData:
            song.pop(commonId, None)
            song.pop(commonHash, None)

        return songData

    @staticmethod
    def _hash(filepath):
        h = 0
        for char in filepath:
            h = (31 * h + ord(char)) & 0xFFFFFFFF
        return ((h + 0x80000000) & 0xFFFFFFFF) - 0x80000000
