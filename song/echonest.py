#! /usr/bin/python

import myconfig

import time
from pyechonest import song, config

config.ECHO_NEST_API_KEY=myconfig.ECHO_NEST_API_KEY

## Returns a song's audio features, including:
## mode, tempo, key, duration, time signature, loudness, danceability, energy
## Returns the dictionary of song attributes, or an empty dictionary if there was an error
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

def read_song():
    infile = open('Library.xml')
    outfile = open('output.xls', 'w+')

    line = infile.readline()

    counter = 0
    while line:
        if line.find('<key>Name</key>') != -1:
            counter += 1

            title = line[26:line.index('</string>')]
            if title.find('&') != -1:
                title = title.replace('#38;', '')
            outfile.write(title)
            outfile.write("\t")
            line = infile.readline()
            
            artist = line[28:line.index('</string>')]
            if artist.find('&') != -1:
                artist = artist.replace('#38;','')
            outfile.write(artist)
            outfile.write("\t")
            line = infile.readline()

            while line.find('</dict>') == -1:
                if line.find('<key>Album</key>') != -1:
                    album = line[27:line.index('</string>')]
                    if album.find('&') != -1:
                        album = album.replace('#38;','')
                    outfile.write(album)
                    line = infile.readline()
                
                if line.find('<key>Genre</key>') != -1:
                    outfile.write("\t")
                    genre = line[27:line.index('</string>')]
                    if genre.find('&') != -1:
                        genre = genre.replace('#38;','')
                    outfile.write(genre)
                    outfile.write("\t")
                
                if line.find('<key>Year</key>') != -1:
                    year = line[27:line.index('</integer>')]
                    outfile.write(year)

                line = infile.readline()
            outfile.write("\t")
            

            feats = get_features(artist, title)
            
            outfile.write(str(feats))
            outfile.write("\t")

            if (feats != {}):
                for k, v in feats.iteritems():
                    outfile.write(str(v)) 
                    outfile.write("\t")
            outfile.write("\n")
                
        line = infile.readline()
        
        
        if counter == 50:
            time.sleep(60)
            counter = 0
