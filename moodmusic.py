#! /usr/bin/python
# Runs MoodMusic
# Usage: ./test_cli.py path/to/song.mp3

from ui.cli import *
from song.song import Song
from input.Import import *
import myconfig

def run(songPath):

    #Start CLI
    application = CLI()
    mySong = Song.song_from_filepath(songPath)
    application.play_song(mySong)

    #Start background thread importer
    importer = Importer(MUSIC_LIBRARY_FILE_PATH, 100)
    importer.startDaemon()

if __name__ == '__main__':
    if sys.argv[1:] and sys.argv[1] not in ('-h', '--help'):
        run(sys.argv[1])

    else:
        print('Usage: %s <song_filename>' % sys.argv[0])
        print('Once launched, type ? for the menu.\n')
        