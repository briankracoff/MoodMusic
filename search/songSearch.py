import os
import re
import urllib, urlparse


def song_search(MUSIC_FOLDER):

    # Note that these fields are not
    print "Enter an Artist:",
    searcha = raw_input()
    searcha = searcha.lower()
    print "Enter a song:",
    searchs = raw_input()
    searchs = searchs.lower()

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
                        matchlowered = match.lower()
                        if matchlowered.find(searcha) != -1 and matchlowered.find(searchs) != -1:
                            print 'Found the filepath:', match
                            print 'Is this what you were looking for? (y or n, or g to give up)'
                            answer = raw_input('> ')
                            if answer == 'y':
                                return match
                            elif answer == 'g':
                                return fail_recirc(MUSIC_FOLDER)
            return fail_recirc(MUSIC_FOLDER)
    
    else:
        for dirname, dirnames, filenames in os.walk(MUSIC_FOLDER):
            for filename in filenames:
                currpath = os.path.join(dirname, filename)
                currpathlowered = currpath.lower()
                if currpathlowered.find(searcha) != -1 and currpathlowered.find(searchs) != -1:
                    print 'Found the filepath:', currpath
                    print 'Is this what you were looking for? (y or n, or g to give up)'
                    answer = raw_input()
                    if answer == 'y':
                        return currpath
                    elif answer == 'g':
                        return fail_recirc(MUSIC_FOLDER)
        return fail_recirc(MUSIC_FOLDER)
    
        

def fail_recirc(MUSIC_FOLDER):
    print 'Song not found in library'
    print 'Would you like to try again? (y or n)'
    answer = raw_input()
    if answer == 'y':
        return song_search(MUSIC_FOLDER)
    else:
        return None


