#! /usr/bin/python

from pyechonest import config, song

config.ECHO_NEST_API_KEY="YNBJILDXWEZ6LGWLG"

#Returns a song's audio features, including:
#mode, tempo, key, duration, time signature, loudness, danceability, energy
#Returns the dictionary of song attributes, or an empty dictionary if there was an error
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
