#! /usr/bin/python
# Author: Brian Kracoff
# Helper class for the DB methods
# Usage: DB_Helper().method, since it is a singleton class

from data.SqLite import SqLite, C
from data.DB_constants import *
import config

class DB_Helper(object):

    #Singleton pattern
    _instance = None
    def __new__(cls, *args, **kwargs):
        if config.SANDBOX_DB in args:
            cls._instance = super(DB_Helper, cls).__new__(
                        cls)
        if True in args:
            return super(DB_Helper, cls).__new__(
                            cls, *args, **kwargs)
        elif not cls._instance:
            cls._instance = super(DB_Helper, cls).__new__(
                                cls)
        return cls._instance

    def __init__(self, new = False, db = config.SANDBOX_DB):
        self.db = SqLite(db);

    #Returns a dictionary of attributes for a song's filepath
    def attributes_for_filepath(self, filepath):
        songData = self.get_song(filepath)

        #Removes non-attributes
        if songData != None:
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

    #Returns all songs assigned moods and their assigned mood
    def all_song_moods(self):
        self.db.setNamespace(moodNamespace)

        #Get moods from DB with hash
        self.db.search()
        rawMoods = self.db.read()

        return rawMoods

    # get list of moods used by user
    def all_moods(self):
        self.db.setNamespace(moodNamespace)

        #Get moods from DB with hash
        self.db.search()
        rawMoods = self.db.read()

        ms = []
        for m in rawMoods:
            ms.append(m[moodTitle])

        return list(set(ms))

    # get filepath from hash
    def hash_to_file(self, h):
        self.db.setNamespace(songNamespace)
        
        self.db.search(C._raw(commonHash, '=', str(h)))
        result = self.db.read()
        
        # get filepath
        return result[0][songFilePath['name']]

    #Adds the given mood for the song's filepath
    def add_mood(self, filepath, title):
        self.db.setNamespace(moodNamespace)
        songHash = DB_Helper._hash(filepath)

        #Adds mood to DB
        self.db.write({commonHash:songHash, moodTitle:title})

    #Gets all of the data out of the Song namespace (except for id and hash)
    def all_songs(self):
        self.db.setNamespace(songNamespace)

        #Get songdata from DB with hash
        self.db.search() 
        songData = self.db.read()
                    
        return songData
        
    #Get the song with the given hash
    def get_song(self, filepath):
        songHash = DB_Helper._hash(filepath)
        self.db.setNamespace(songNamespace)

        #Finds song if it exists
        self.db.search(C._raw(commonHash, "=", songHash))
        return self.db.read(1)

    #Returns whether the filepath is in the DB or not
    def is_in_db(self, filepath):
        return self.get_song(filepath) != None

    #Adds the song to the DB
    def add_song(self, attributesDict):
        self.db.setNamespace(songNamespace)
        
        songHash = DB_Helper._hash(attributesDict[songFilePath['name']])

        #Adds hash to attributes
        attributesDict[commonHash] = songHash

        #Writes song to db
        try:
            self.db.write(attributesDict)
        except Exception:
            pass

    @staticmethod
    def _hash(filepath):
        h = 0
        for char in filepath:
            h = (31 * h + ord(char)) & 0xFFFFFFFF
        return ((h + 0x80000000) & 0xFFFFFFFF) - 0x80000000
