import os
from myconfig import *


def song_search():


    # Note that these fields are not
    print "Enter an Artist:",
    searcha = raw_input()
    print "Enter a song:",
    searchs = raw_input()


    for dirname, dirnames, filenames in os.walk(MUSIC_FOLDER):
        for filename in filenames:
            currpath = os.path.join(dirname, filename)
            if currpath.find(searcha) != -1 and currpath.find(searchs) != -1:
                print 'Found the filepath:', currpath
                print 'Is this what you were looking for? (y or n, or g to give up)'
                answer = raw_input()
                if answer == 'y':
                    return currpath
                elif answer == 'g':
                    return fail_recirc()
    return fail_recirc()
    
        

def fail_recirc():
    print 'Song not found in library'
    print 'Would you like to try again? (y or n)'
    answer = raw_input()
    if answer == 'y':
        return song_search()
    else:
        return None
