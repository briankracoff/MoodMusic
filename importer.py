'''
Created on Apr 3, 2013

@author: Behrooz Afghahi
@version: 0.1
'''
from input.Import import Importer
from config import *

if __name__ == '__main__':
    #Start background thread importer
    importer = Importer(Config().get_attr('MUSIC_LIBRARY_FILE_PATH'), 100000)
    importer.fetcher()
