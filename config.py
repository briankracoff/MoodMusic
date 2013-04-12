#! /usr/bin/python
# Main Configuration file

import pickle

# SqLite Config
DEFAULT_DB = "default"
SANDBOX_DB = "sandboxDB"

#Different feature-detection namespaces
DEFAULT_SONG_TABLE = "Song"
MARSYAS_SONG_TABLE = "M_Song"

#Whether to use the default DB or the test sandbox DB (set by a command-line argument)
CHOSEN_DB = DEFAULT_DB

#Whether to use the default EchoNest features or the alternative Marsyas features
CHOSEN_FEATURE_TABLE = DEFAULT_SONG_TABLE

class Config:

    #Singleton pattern
    _instance = None
    def __new__(cls, *args, **kwargs):
        if not cls._instance:
            cls._instance = super(Singleton, cls).__new__(
                                cls, *args, **kwargs)
        return cls._instance

    def __init__(self):
        configFile = open('config.pkl', 'rb')
        self._params = pickle.load(configFile)
        configFile.close()

    def get_attr(self, attr):
        return self._params[attr]
