#! /usr/bin/python
# Runs MoodMusic
# Usage: ./test_cli.py path/to/song.mp3

from ui.cli import *
from song.song import Song
import pickle
from data.SqLite import *
from data.DB_Helper import *
from config import *

from input.Import import FetchData

#Returns a list of attributes
def __get_attribute_schema():
    return [
        songFilePath,
        songTitle,
        songArtist,
        songBeatAverage,
        songBeatDeviation,
        songBarsAverage,
        songBarsDeviation,
        songDanceability,
        songDuration,
        songEndOfFadeIn,
        songEnergy,
        songKey,
        songKeyConfidence,
        songLiveness,
        songLoudness,
        songMode,
        songModeConfidence,
        songOffsetSeconds,
        songSectionsAverage,
        songSectionsDeviation,
        songSectionsCount,
        songSpeechiness,
        songStartOfFadeOut,
        songTatumsAverage,
        songTatumsDeviation,
        songTatumsCount,
        songTempo,
        songTempoConfidence,
        songTimeSignature,
        songTimeSignatureConfidence
    ]

#Resets the DB schema
def __initialize_DB():
    print "Starting DB setup...\n"
    db = SqLite();

    print "............................\n"
    
    #Song namespace
    print "Checking for Song namespace"
    if db.hasNamespace(songNamespace):
        print "Song namespace exists"
        print "Deleting Song namespace"
        db.removeNamespace(songNamespace)
        print "Song namespace deleted"
    else:
        print "Song namespace doesn't exist"

    print "Creating Song namespace"
    song_def = {
        commonHash:"TEXT"
    }

    for attribute in __get_attribute_schema():
        song_def[attribute['name']] = attribute['type']

    db.installNamespace(songNamespace, song_def)
    print "Song namespace created\n"

    print "............................\n"

    #Mood namespace
    print "Checking for Mood namespace"
    if db.hasNamespace(moodNamespace):
        print "Mood namespace exists"
        print "Deleting Mood namespace"
        db.removeNamespace(moodNamespace)
        print "Mood namespace deleted"
    else:    
        print "Mood namespace doesn't exist"

    print "Creating Mood namespace"
    mood_def = {
        commonHash:"TEXT",
        moodTitle:"TEXT"
    }
    db.installNamespace(moodNamespace, mood_def)
    print "Mood namespace created\n"

    print "............................\n"

    print "Done with DB setup!\n"

def __make_config_file():
    apiKey = raw_input('Enter your EchoNest API Key: ')
    musicLibraryFilePath = raw_input('Enter your music library file path: ')

    #Makes sure file exists
    while not os.path.isfile(musicLibraryFilePath):
        musicLibraryFilePath = raw_input('Please enter a valid music library file path: ')

    # Makes config file
    configDict = {  
        'ECHO_NEST_API_KEY': apiKey,
        'MUSIC_LIBRARY_FILE_PATH': musicLibraryFilePath
    }
    output = open('config.pkl', 'wb')
    pickle.dump(configDict, output)
    output.close()

    print "Config file created\n\n"
 

# Executes when the user hasn't run MoodMusic yet
# Sets up DB, and prompts user for config params 
def __first_time():
    print "****************\nWelcome to MoodMusic!\n****************\n"

    print "****************\nFirst we are going to setup the DB:\n****************\n"
    __initialize_DB()

    print "****************\nNext we're going to enter in some config parameters\n****************\n"
    __make_config_file()

def run():

    if not os.path.isfile('config.pkl'):
        __first_time()

    #Starts background daemon
    daemon = FetchData()
    daemon.start()

    #Start CLI
    application = CLI(daemon)

    print "\nPlease choose an option:\n"
    print "a -> Enter song to play"

    moods = []#DB_Helper().all_moods()
    if len(moods) > 0:
        print "b -> Enter mood to play"

    choice = raw_input('\nEnter your choice: ')
    while(choice not in ['a', 'b']):
        choice = raw_input('Please enter an option above: ')

    if choice == 'a':
        #User enters a filepath
        songFile = raw_input('Enter song file: ')
        mySong = Song.song_from_filepath(songFile)
        application.play_song(mySong)
    elif choice == 'b':
        #User enters a mood
        print "Choose a mood from the options below:"
        for mood in moods:
            print mood
        application.play_song(mySong)

        chosenMood = raw_input('Enter choice: ')
        while chosenMood not in moods:
            chosenMood = raw_input('Please enter one of the options above: ')

        songFile = ''
        mySong = Song.song_from_filepath(songFile)
        application.play_song(mySong)

if __name__ == '__main__':
    run()
