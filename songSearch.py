## This function takes user input to search the default library for a specified
### song
## Returns the local filepath of the closest match found

## This search is primitve:
### It simply looks for the two strings you provided in the filepath, independent
### of order and which one is actually the Artist or Song title

import os
from myconfig import *


def song_search():
    searchpath = None
    
    while searchpath == None:
        print "Enter an Artist:",
        searcha = raw_input()
        print "Enter a song:",
        searchs = raw_input()

        for dirname, dirnames, filenames in os.walk(MUSIC_FOLDER):
            for filename in filenames:
                currpath = os.path.join(dirname, filename)
                if currpath.find(searcha) != -1 and currpath.find(searchs) != -1:
                    searchpath = currpath
    return searchpath
