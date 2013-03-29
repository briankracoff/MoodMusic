#! /usr/bin/python

from data.DB_constants import *
from data.DB_Helper import *

from myconfig import *
import math

from pyechonest import config
from pyechonest.track import track_from_file

import os



config.ECHO_NEST_API_KEY=ECHO_NEST_API_KEY



## function to read a whole library into the DB
## takea a path as an argument
def library_attributes():
    for dirname, dirnames, filenames in os.walk(MUSIC_FOLDER):
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
    
    song = { songFilePath['name']: pathstring,
             songTitle['name']: str(track),
             songArtist['name']: str(track.artist),
             songBeatAverage['name']: beatavg,
             songBeatDeviation['name']: beatdev,
             songBarsAverage['name']: barsavg,
             songBarsDeviation['name']: barsdev,
             songDanceability['name']: track.danceability,
             songDuration['name']: track.duration,
             songEndOfFadeIn['name']: track.end_of_fade_in,
             songEnergy['name']: track.energy,
             songKey['name']: track.key,
             songKeyConfidence['name']: track.key_confidence,
             songLiveness['name']: track.liveness,
             songLoudness['name']: track.loudness,
             songMode['name']: track.mode,
             songModeConfidence['name']: track.mode_confidence,
             songOffsetSeconds['name']: track.offset_seconds,
             songSectionsAverage['name']: sectionsavg,
             songSectionsDeviation['name']: sectionsdev,
             songSectionsCount['name']: len(track.sections),
             songSpeechiness['name']: track.speechiness,
             songStartOfFadeOut['name']: track.start_of_fade_out,
             songTatumsAverage['name']: tatumsavg,
             songTatumsDeviation['name']: tatumsdev,
             songTatumsCount['name']: len(track.tatums),
             songTempo['name']: track.tempo,
             songTempoConfidence['name']: track.tempo_confidence,
             songTimeSignature['name']: track.time_signature,
             songTimeSignatureConfidence['name']: track.time_signature_confidence}
 
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


library_attributes()    
