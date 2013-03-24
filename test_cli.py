#! /usr/bin/python
# A simple test class for cli.py
# Usage: ./test_cli.py path/to/song.mp3

from ui.cli import *
from song.song import Song

def run(songPath):
    
    myCLI = CLI()
    mySong = Song(songPath)
    myCLI.play_song(mySong)

if __name__ == '__main__':
    if sys.argv[1:] and sys.argv[1] not in ('-h', '--help'):
        run(sys.argv[1])

    else:
        print('Usage: %s <song_filename>' % sys.argv[0])
        print('Once launched, type ? for the menu.\n')
        