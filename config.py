#! /usr/bin/python
# Main Configuration file

import pickle

# SqLite Config
DEFAULT_DB = "default"
SANDBOX_DB = "sandboxDB"

CHOSEN_DB = DEFAULT_DB

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
