#! /usr/bin/python

from data.DB_Constants import *
from data.DB_Helper import *

import myconfig
import math

from pyechonest import config
from pyechonest.track import track_from_file

import os



config.ECHO_NEST_API_KEY=myconfig.ECHO_NEST_API_KEY



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
    if not DB_Helper().is_in_db(songpath):
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
    
    song = { songFilePath: pathstring,
             songTitle: str(track),
             songArtist: str(track.artist),
             songBeatAverage: beatavg,
             songBeatDeviation: beatdev,
             songBarsAverage: barsavg,
             songBarsDeviation: barsdev,
             songDanceability: track.danceability,
             songDuration: track.duration,
             songEndOfFadeIn: track.end_of_fade_in,
             songEnergy: track.energy,
             songKey: track.key,
             songKeyConfidence: track.key_confidence,
             songLiveness: track.liveness,
             songLoudness: track.loudness,
             songMode: track.mode,
             songModeConfidence: track.mode_confidence,
             songOffsetSeconds: track.offset_seconds,
             songSectionsAverage: sectionsavg,
             songSectionsDeviation: sectionsdeviation,
             songSectionsCount: len(track.sections),
             songSpeechiness: track.speechiness,
             songStartOfFadeOut: track.start_of_fade_out,
             songTatumsAverage: tatumsavg,
             songTatumsDeviation: tatumsdev,
             songTatumsCount: len(track.tatums),
             songTempo: track.tempo,
             songTempoConfidence: track.tempo_confidence,
             songTimeSignature: track.time_signature,
             songTimeSignatureConfidence: track.time_signature_confidence}
 
    ## calls a function to place these attributes in the DB
     # instead, should make this call through the DB abstraction layer
    DB_Helper().add_song(song)

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

    
