#! /usr/bin/python
# Author: Brian Kracoff
# Runs the main program for MoodMusic
# Usage: ./moodmusic.py

from first_time import *
from ui.cli import *
from song.song import Song
import pickle
from data.SqLite import *
from data.DB_Helper import *
from config import *
from songSearch import *

from ml.Playlist import Playlist

from input.Import import FetchData


 



def run():

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
        p = Playlist(db, moods)

        print '\nHow would you like to select a song?\n'
        print 'f -> Provide a filepath'
        print 'l -> Search your Library'
        selection = raw_input()
        if selection == 'f':
            songFile = raw_input('Enter song file: ')
        elif selection == 'l':
            songFile = song_search()
        if songFile != None:
    
            p.generate_list_song(db._hash(songFile))

            application.set_list(p)
            application.play_song()

 
        songFile = raw_input('Enter song file: ')

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

if __name__ == '__main__':
    run()
