'''
Created on Apr 3, 2013

@author: Behrooz Afghahi
@version: 0.1
'''
from input.Import import Importer
import config
from config import Config
import sys

if __name__ == '__main__':
    #Start background thread importer
    config.CHOSEN_FEATURE_TABLE = sys.argv[1]
    importer = Importer(Config().get_attr('MUSIC_LIBRARY_FILE_PATH'), 100000)
    importer.fetcher()
