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
