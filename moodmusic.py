#! /usr/bin/python
# Author: Brian Kracoff
# Runs the main program for MoodMusic
# Usage: ./moodmusic.py

from ui.cli import *
from song.song import Song
import pickle
from data.SqLite import *
from data.DB_Helper import *
import config
from search.songSearch import *
import argparse

from ml.Playlist import Playlist

from input.Import import FetchData
import atexit # used for removing the PID file on exit
import os

#Resets the DB schema
def __initialize_DB():
    print "Starting DB setup...\n"
    db = SqLite();

    print "............................\n"

    ns = config.CHOSEN_FEATURE_TABLE
    print "Checking for " + ns + " namespace"
    if db.hasNamespace(ns):
        print ns + " namespace exists"
        print "Deleting " + ns + " namespace"
        db.removeNamespace(ns)
        print ns + " namespace deleted"
    else:
        print ns + " namespace doesn't exist"

    print "Creating " + ns + " namespace"
    song_def = {
        commonHash:"TEXT",
        commonTitle:"TEXT",
        commonArtist:"TEXT",
        commonPath:"TEXT"
    }

    if ns == config.DEFAULT_SONG_TABLE:
        from input.data_mining import attribute_schema
    #else:
    #   from input.marsyas import attribute_schema

    for attribute in attribute_schema:
        song_def[attribute.name] = attribute.type

    db.installNamespace(ns, song_def)
    print ns + " namespace created\n"

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
    apiKey = raw_input('Enter your EchoNest API Key (if you don\'t have one, use YNBJILDXWEZ6LGWLG: ')
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

    print "****************\nFirst we are going to setup the DB:\n****************\n"
    __initialize_DB()

    print "****************\nNext we're going to enter in some config parameters\n****************\n"
    __make_config_file()

def choice_c(moods, db):
    print "Choose a mood from the options below:"
    for mood in moods:
        print mood

    chosenMood = raw_input('Enter choice: ')
    while chosenMood not in moods:
        chosenMood = raw_input('Please enter one of the options above: ')

    print "Max length of your playlist: "
    x = True
    while x:
        maxlen = raw_input("> ")
        try:
            maxlen = int(maxlen)
            x = False
        except:
            print "Cannot be converted to integer, try again."
    # make playlist
    p = Playlist(db, moods)
    p.add_mood(chosenMood)
    p.generate_list_mood()
        
    plist = p.get_list(maxlen)
    for s in plist:
        print str(s)

    print "Save as .m3u? y/n"
    save = raw_input("> ")
    if save == "y":
        m3u = open("playlist.m3u","wb")
        for song in plist:
            print>>m3u, song

def choice_d(moods, db):
    print "Enter the song file path you want to add to a mood:"
    filepath = raw_input("> ")
    while not db.is_in_db(filepath) and filepath != "n":
        print "Song not in database. Try again. (or n to quit)"
        filepath = raw_input("> ")
    if filepath != "n":
        print "Choose mood to add (or new mood)."
        for mood in moods:
            print mood
        chosenMood = raw_input('> ')
        db.add_mood(filepath, chosenMood)        

def run(runBackgroundImporter = True):    
    atexit.register(FetchData.removePID)

    if not os.path.isfile('config.pkl'):
        __first_time()

    daemon = None
    if runBackgroundImporter:
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
        print "c -> Generate a playlist from mood (without playing)"
    print "d -> Add song to mood (without playing)"

    choice = raw_input('\nEnter your choice: ')
    while(choice not in ['a', 'b', 'c', 'd']):
        choice = raw_input('Please enter an option above: ')

    if choice == 'a':

        print "\nHow would you like to select a song?\n"
        print "l -> Search your Library"
        print "f -> Enter a filepath"

        selection = raw_input('> ')
        while (selection not in ['l', 'f']):
            selection = raw_input('Please enter an option above: ')
        if selection == 'l':
            songFile = song_search(Config().get_attr('MUSIC_LIBRARY_FILE_PATH'))
        elif selection == 'f':
            #User enters a filepath
            songFile = raw_input('Enter song file: ')

        if songFile != None:
            chosenSong = Song.song_from_filepath(songFile)
            application.play_song(chosenSong)
        
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

    elif choice == 'c':
        choice_c(moods, db)
    elif choice == 'd':
        choice_d(moods, db)

def run_sandbox():
    print "****************\nWelcome to the sandboxed MoodMusic\n****************"
    print "\nYou are using our DB of thousands of songs so that you can test our machine learning algorithms\n"

    #Makes the DB_Helper use Tom's Sandbox DB
    db = DB_Helper()

    print "Choose a mood from the options below:"
    moods = DB_Helper().all_moods()
    for mood in moods:
        print mood

    chosenMood = raw_input('Enter choice: ')
    while chosenMood not in moods:
        chosenMood = raw_input('Please enter one of the options above: ')

    print "Max length of your playlist: "
    x = True
    while x:
        maxlen = raw_input("> ")
        try:
            maxlen = int(maxlen)
            x = False
        except:
            print "Cannot be converted to integer, try again."
    # make playlist
    p = Playlist(db, moods)
    p.add_mood(chosenMood)
    p.generate_list_mood()
    
    plist = p.get_list(maxlen)
    for s in plist:
        print str(s)

    print "Save as .m3u? y/n"
    save = raw_input("> ")
    if save == "y":
        m3u = open("playlist.m3u","wb")
        for song in plist:
            print>>m3u, song

if __name__ == '__main__':
    argparser = argparse.ArgumentParser(prog='MoodMusic', description='A playlist generator in Python')
    argparser.add_argument('-t', '--test', help='Run in the sandbox environment using a test DB', action='store_true')
    argparser.add_argument('--no-import', help="Don't run the background importer during execution", action='store_true')
    argparser.add_argument('-m', '--marsyas', help='Run with the alternative Marsyas feature detection', action='store_true')
    args = argparser.parse_args()

    if args.test:
        config.CHOSEN_DB = config.SANDBOX_DB
        run_sandbox()

    else:
        runBackgroundImporter = True

        if args.marsyas:
            config.CHOSEN_FEATURE_TABLE = config.MARSYAS_SONG_TABLE

        if args.no_import:
            runBackgroundImporter = False

        run(runBackgroundImporter)
