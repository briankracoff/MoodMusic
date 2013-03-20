<<<<<<< HEAD
#! /usr/bin/python

from pyechonest import config, song

config.ECHO_NEST_API_KEY="YNBJILDXWEZ6LGWLG"

#Returns a song's audio features, including:
#mode, tempo, key, duration, time signature, loudness, danceability, energy
#Returns the dictionary of song attributes, or an empty dictionary if there was an error
=======

import time
from pyechonest import config, song, artist

config.ECHO_NEST_API_KEY="OPKH9VHPDR0RT0GN3"

## Returns a song's audio features, including:
## mode, tempo, key, duration, time signature, loudness, danceability, energy
## Returns the dictionary of song attributes, or an empty dictionary if there was an error
>>>>>>> Added a module to Brian's code that reads the xml library, uses his
def get_features(songArtist = '', songTitle = ''):

    if songArtist == '' or songTitle == '':
        return {};

    #Searches for the song in pyechonest
    song_results = song.search(artist=songArtist, title=songTitle)

    if len(song_results) > 0:
        desiredSong = song_results[0]

        if desiredSong:
            #If song was found, return its attributes
            return desiredSong.audio_summary

    return {}
<<<<<<< HEAD
=======

def read_song():
    infile = open('Library.xml')
    outfile = open('output.xls', 'w+')

    line = infile.readline()

    counter = 0
    while line:
        if line.find('<key>Name</key>') != -1:
            counter += 1

            start = line.index('Name') + 18
            end = line.index('</string>')
            songtitle = line[start:end]

            line = infile.readline()
            songartist = line[28:line.index('</string>')]

            outfile.write(songartist)
            outfile.write("\t")

            outfile.write(songtitle)
            outfile.write("\t")

            feats = get_features(songartist, songtitle)
 #           print(feats)
            
            outfile.write(str(feats))
            outfile.write("\t")

            if (feats != {}):
                for k, v in feats.iteritems():
                    outfile.write(str(v)) 
                    outfile.write("\t")
            outfile.write("\n")
            #time.sleep(.8)
                
        line = infile.readline()
        
        if counter == 60:
            time.sleep(60)
            counter = 0

read_song()

>>>>>>> Added a module to Brian's code that reads the xml library, uses his
