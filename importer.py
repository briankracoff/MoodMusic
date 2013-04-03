'''
Created on Apr 3, 2013

@author: Behrooz Afghahi
@version: 0.1
'''
from input.Import import Importer
import myconfig

if __name__ == '__main__':
    #Start background thread importer
    importer = Importer(myconfig.MUSIC_LIBRARY_FILE_PATH, 100)
    importer.fetcher()