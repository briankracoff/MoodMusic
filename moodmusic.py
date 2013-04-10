#! /usr/bin/python
# Author: Brian Kracoff
# Runs the main program for MoodMusic
# Usage: ./moodmusic.py

from ui.cli import *
from song.song import Song
import pickle
from data.SqLite import *
from data.DB_Helper import *
from config import *

from ml.Playlist import Playlist

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
        songTimeSignatureConfidence,
        songLoudnessMaxAverage,
        songLoudnessMaxDeviation,
        songLoudnessMaxDifferential,
        songLoudnessMaxTimeAverage,
        songLoudnessMaxTimeDeviation,
        songLoudnessMaxTimeDifferential,
        songLoudnessStartAverage,
        songLoudnessStartDeviation,
        songLoudnessStartDifferential,
        songTimbre1Average,
        songTimbre1Dev,
        songTimbre1Diff,
        songTimbre2Average,
        songTimbre2Dev,
        songTimbre2Diff,
        songTimbre3Average,
        songTimbre3Dev,
        songTimbre3Diff,
        songTimbre4Average,
        songTimbre4Dev,
        songTimbre4Diff,
        songTimbre5Average,
        songTimbre5Dev,
        songTimbre5Diff,
        songTimbre6Average,
        songTimbre6Dev,
        songTimbre6Diff,
        songTimbre7Average,
        songTimbre7Dev,
        songTimbre7Diff,
        songTimbre8Average,
        songTimbre8Dev,
        songTimbre8Diff,
        songTimbre9Average,
        songTimbre9Dev,
        songTimbre9Diff,
        songTimbre10Average,
        songTimbre10Dev,
        songTimbre10Diff,
        songTimbre11Average,
        songTimbre11Dev,
        songTimbre11Diff,
        songTimbre12Average,
        songTimbre12Dev,
        songTimbre12Diff,
        songPitch1Average,
        songPitch1Dev,
        songPitch1Diff,
        songPitch2Average,
        songPitch2Dev,
        songPitch2Diff,
        songPitch3Average,
        songPitch3Dev,
        songPitch3Diff,
        songPitch4Average,
        songPitch4Dev,
        songPitch4Diff,
        songPitch5Average,
        songPitch5Dev,
        songPitch5Diff,
        songPitch6Average,
        songPitch6Dev,
        songPitch6Diff,
        songPitch7Average,
        songPitch7Dev,
        songPitch7Diff,
        songPitch8Average,
        songPitch8Dev,
        songPitch8Diff,
        songPitch9Average,
        songPitch9Dev,
        songPitch9Diff,
        songPitch10Average,
        songPitch10Dev,
        songPitch10Diff,
        songPitch11Average,
        songPitch11Dev,
        songPitch11Diff,
        songPitch12Average,
        songPitch12Dev,
        songPitch12Diff,
        songPitch1Ratioa,
        songPitch2Ratioa,
        songPitch3Ratioa,
        songPitch4Ratioa,
        songPitch5Ratioa,
        songPitch6Ratioa,
        songPitch7Ratioa,
        songPitch8Ratioa,
        songPitch9Ratioa,
        songPitch10Ratioa,
        songPitch11Ratioa,
        songPitch12Ratioa,
        songPitch1Ratiob,
        songPitch2Ratiob,
        songPitch3Ratiob,
        songPitch4Ratiob,
        songPitch5Ratiob,
        songPitch6Ratiob,
        songPitch7Ratiob,
        songPitch8Ratiob,
        songPitch9Ratiob,
        songPitch10Ratiob,
        songPitch11Ratiob,
        songPitch12Ratiob
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
<<<<<<< HEAD
    apiKey = raw_input('Enter your EchoNest API Key: ')
=======
    apiKey = raw_input('Enter your EchoNest API Key (if you don\'t have one, use YNBJILDXWEZ6LGWLG: ')
>>>>>>> parent of f230c82... fixed search module
    musicLibraryFilePath = raw_input('Enter your music library file path: ')

    #Makes sure file exists
    while not (os.path.isfile(musicLibraryFilePath) or os.path.isdir(musicLibraryFilePath)):
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
<<<<<<< HEAD

    print "****************\nFirst we are going to setup the DB:\n****************\n"
    __initialize_DB()

=======

    print "****************\nFirst we are going to setup the DB:\n****************\n"
    __initialize_DB()

>>>>>>> parent of f230c82... fixed search module
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

    #Init Database Chatter
    db = DB_Helper()

    print "\nPlease choose an option:\n"
    print "a -> Enter song to play"

    moods = db.all_moods()
    if len(moods) > 0:
        print "b -> Enter mood to play"

    choice = raw_input('\nEnter your choice: ')
    while(choice not in ['a', 'b']):
        choice = raw_input('Please enter an option above: ')

    if choice == 'a':
        #User enters a filepath
<<<<<<< HEAD
        p = Playlist(db, moods)

=======
>>>>>>> parent of a4cfc74... Merge branch 'master' of https://github.com/briankracoff/MoodMusic
        songFile = raw_input('Enter song file: ')

        p.generate_list_song(db._hash(songFile))
        application.set_list(p)

        application.play_song()
        
    elif choice == 'b':
        #User enters a mood
        print "Choose a mood from the options below:"
        for mood in moods:
            print mood

        chosenMood = raw_input('Enter choice: ')
        while chosenMood not in moods:
            chosenMood = raw_input('Please enter one of the options above: ')

        # make playlist
        p = Playlist(db, moods)
        p.add_mood(chosenMood)
        p.generate_list_mood()
        application.set_list(p)

        application.play_song()

if __name__ == '__main__':
    run()
