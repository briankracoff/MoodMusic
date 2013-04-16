#! /usr/bin/python
# Runs the main program for MoodMusic
# Usage: ./moodmusic.py
# Use -h flag to see optional flags

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
def __check_db():
    db = SqLite();

    ns = config.CHOSEN_FEATURE_TABLE
    if not db.hasNamespace(ns):
        print ns + " namespace doesn't exist! Creating it..."
        song_def = {
            commonHash:"TEXT",
            commonTitle:"TEXT",
            commonArtist:"TEXT",
            commonPath:"TEXT"
        }

        if ns == config.DEFAULT_SONG_TABLE:
            from input.data_mining import attribute_schema
        else:
            from input.marsyas_mir import attribute_schema

        for attribute in attribute_schema:
            song_def[attribute.name] = attribute.type

        db.installNamespace(ns, song_def)
        print ns + " namespace created\n"

    #Mood namespace
    if not db.hasNamespace(moodNamespace):
        print "Mood namespace doesn't exist! Creating it..."

        mood_def = {
            commonHash:"TEXT",
            moodTitle:"TEXT"
        }
        db.installNamespace(moodNamespace, mood_def)
        print "Mood namespace created\n"

def __make_config_file():
    print "****************\nSince this is your first time, you'll need to enter some config parameters\n****************\n"

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
 
# Generates a playlist for a mood and allows the user to save the playlist as a .m3u file
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

# Runs a loop to ask the user to enter filepaths and add them to moods
def choice_d(db):
    while(True):
        moods = DB_Helper().all_moods()
        print "Enter the song file path you want to add to a mood (or q to quit):"
        filepath = raw_input("> ")

        if filepath == 'q':
            sys.exit(0)

        while not db.is_in_db(filepath) and filepath != "n":
            print "Song not in database. Try again. (or n to quit)"
            filepath = raw_input("> ")
        if filepath != "n":
            print "Choose mood to add (or enter a new mood)."
            for mood in moods:
                print mood
            chosenMood = raw_input('> ')
            db.add_mood(filepath, chosenMood)        

def run(runBackgroundImporter = True):    
    print "****************\nWelcome to MoodMusic!\n****************\n"

    atexit.register(FetchData.removePID)

    if not os.path.isfile('config.pkl'):
        __make_config_file()

    __check_db()

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
        # User enters a filepath for a song to play
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
        #User enters a mood to generate a playlist and play
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
        choice_d(db)

# Runs the sandbox test mode for the sandbox DB
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
    #Init argparser
    argparser = argparse.ArgumentParser(prog='MoodMusic', description='A playlist generator in Python')
    argparser.add_argument('-t', '--test', help='Run in the sandbox environment using a test DB', action='store_true')
    argparser.add_argument('--no-import', help="Don't run the background importer during execution", action='store_true')
    argparser.add_argument('-m', '--marsyas', help='Run with the alternative Marsyas feature detection', action='store_true')
    args = argparser.parse_args()

    if args.test:
        #Run test DB
        config.CHOSEN_DB = config.SANDBOX_DB
        run_sandbox()

    else:
        runBackgroundImporter = True

        if args.marsyas:
            #Use Marsyas features
            config.CHOSEN_FEATURE_TABLE = config.MARSYAS_SONG_TABLE

        if args.no_import:
            #Don't run the background importer
            runBackgroundImporter = False

        #Start main program
        run(runBackgroundImporter)
