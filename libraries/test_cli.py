#! /usr/bin/python

from cli import *

def run(songPath):
    
    myCLI = CLI()
    myCLI.play_song(songPath)

if __name__ == '__main__':
    if sys.argv[1:] and sys.argv[1] not in ('-h', '--help'):
        run(sys.argv[1])

    else:
        print('Usage: %s <song_filename>' % sys.argv[0])
        print('Once launched, type ? for the menu.\n')