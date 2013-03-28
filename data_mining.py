#! /usr/bin/python

import myconfig
import math

from pyechonest import config
from pyechonest.track import track_from_file

import os

## Database initialization
import sqlite3 as lite
import sys

con = lite.connect('output.db')

with con:
    cur = con.cursor()

#    cur.execute("DROP TABLE IF EXISTS Songs")
#    cur.execute("CREATE TABLE Songs(Title, Artist, Path, Beat_Average, Beat_Deviation, Bars_Average, Bars_Deviation, Danceability, Duration, End_of_fade_in, Energy, Key, Key_Confidence, Liveness, Loudness, Mode, Mode_Confidence, Offset_Seconds, Sections_Average, Sections_Deviation, Sections_Count, Speechiness, Start_of_fade_out, Tatums_Average, Tatums_Deviation, Tatums_Count, Tempo, Tempo_Confidence, Time_Signature, Time_Signature_Confidence)")



config.ECHO_NEST_API_KEY=myconfig.ECHO_NEST_API_KEY


## function to insert a song and all its attributes into the DB
def put_in_db(song):
    con = lite.connect('output.db')

    with con:
        cur = con.cursor()

        i = 1
        qmarks = "( ? "
        while i < len(song):            
            qmarks += " , ? "
            i += 1
        
        cur.execute("INSERT INTO Songs VALUES" + qmarks + ")", song)


## function to query the DB for the presence of a song
def in_db(songpath):
    con = lite.connect('output.db')
    with con:
        cur.execute("SELECT Path FROM Songs")
        rows = cur.fetchall()
        for row in rows:
            if str(row).find(songpath) != -1:
                return True
        return False

## function to display the DB
## just for diagnostics
def display_db():
    con = lite.connect('output.db')
    with con:
        cur.execute("SELECT * FROM Songs")
        rows = cur.fetchall()
        for row in rows:
            print str(row)

## function to read a whole library into the DB
## takea a path as an argument
def library_attributes(libpath):
    for dirname, dirnames, filenames in os.walk(libpath):
        for filename in filenames:
            song_attributes(os.path.join(dirname, filename))

## function to read an individual song into the DB
## takes a filepath as an argument
 # this could be augmented to take a hash instead
def song_attributes(songpath):
    if in_db(songpath) == False:
        fp = open(songpath, 'rb')
        print fp
        ## check file extension to only read valid types
         # if there's a better way to check file extensions, that would be good
        if (str(fp).find('.mp3') != -1) or  (str(fp).find('.m4a') != -1):
            get_attr(fp, songpath)
            
## function that does the grunt work of reading a track and populating a list of attributes
def get_attr(fp, pathstring):
    track = track_from_file(fp, 'mp3')

    beatavg = get_average(track.beats, 'duration')
    beatdev = get_deviation(track.beats, 'duration', beatavg)
    barsavg = get_average(track.bars, 'duration')
    barsdev = get_deviation(track.bars, 'duration', barsavg)
    sectionsavg = get_average(track.sections, 'duration')
    sectionsdev = get_deviation(track.sections, 'duration', sectionsavg)
    segmentsavg = get_average(track.segments, 'duration')
    segmentsdev = get_deviation(track.segments, 'duration', segmentsavg)
    tatumsavg = get_average(track.tatums, 'duration')
    tatumsdev = get_deviation(track.tatums, 'duration', tatumsavg)
    
    song = [str(track), str(track.artist), pathstring, beatavg, beatdev, barsavg, barsdev, str(track.danceability), str(track.duration), str(track.end_of_fade_in), str(track.energy), str(track.key), str(track.key_confidence), str(track.liveness), str(track.loudness), str(track.mode), str(track.mode_confidence), str(track.offset_seconds), sectionsavg, sectionsdev, len(track.sections), str(track.speechiness), str(track.start_of_fade_out), tatumsavg, tatumsdev, len(track.tatums), str(track.tempo), str(track.tempo_confidence), str(track.time_signature), str(track.time_signature_confidence)]

    ## calls a function to place these attributes in the DB
     # instead, should make this call through the DB abstraction layer
    put_in_db(song)

## function to average a specific set of values found in a dict
def get_average(array, feature):
    aggr = 0
    for k in array:
        aggr += k[feature]
    return aggr/len(array)

## function to get the standard deviation of a set of values found in a dict
 # requires that the average is computed first and passed as an argument
def get_deviation(array, feature, average):
    aggr = 0
    for k in array:
        aggr += math.pow((k[feature] - average), 2)
    return math.sqrt(aggr/len(array))

## hardcoding of my library for reading purposes
#library_attributes('/Users/TomWeaver/Music/iTunes/iTunes Media/Music')

display_db()

    
