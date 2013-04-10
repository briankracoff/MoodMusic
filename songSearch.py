import os
import re
from config import *
import urllib, urlparse


MUSIC_FOLDER = Config().get_attr('MUSIC_LIBRARY_FILE_PATH')


def song_search():

    # Note that these fields are not
    print "Enter an Artist:",
    searcha = raw_input()
    print "Enter a song:",
    searchs = raw_input()

    if MUSIC_FOLDER.find('.xml') != -1:
        files = []
        with open(MUSIC_FOLDER) as f:
            for line in f:
                line = line.strip()
                if line.find('<key>Location</key>') != -1:
                    match = re.search("<string>(.*?)</string>", line)
                    
                    if match is not None:
                        # we need to change the location from file://url/to/file
                        # to an absolute path
                        p = urlparse.urlparse(match.group(1))
                        match = urllib.unquote(os.path.abspath(os.path.join(p.netloc, p.path)))
                        if match.find(searcha) != -1 and match.find(searchs) != -1:
                            print 'Found the filepath:', match
                            print 'Is this what you were looking for? (y or n, or g to give up)'
                            answer = raw_input()
                            if answer == 'y':
                                return match
                            elif answer == 'g':
                                return fail_recirc()
            return fail_recirc()
    
    else:
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


