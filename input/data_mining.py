#! /usr/bin/python

from data.DB_Helper import *
import os
from myconfig import *
import math

from pyechonest import config as pyechonest_config
from pyechonest.track import track_from_file

pyechonest_config.ECHO_NEST_API_KEY=ECHO_NEST_API_KEY

## function to read a whole library into the DB
## takea a path as an argument
def library_attributes():
    for dirname, dirnames, filenames in os.walk(MUSIC_FOLDER):
        for filename in filenames:
            song_attributes(os.path.join(dirname, filename))

## function to read an individual song into the DB
## takes a filepath as an argument
 # this could be augmented to take a hash instead
def song_attributes(songpath, verbose = True, db = None):
    if db is None:
        db = DB_Helper()
    
    if not db.is_in_db(songpath):
        fp = open(songpath, 'rb')
        
        if verbose:
            print "Harvesting: " + songpath
        
        get_attr(fp, songpath, db)
            
## function that does the grunt work of reading a track and populating a list of attributes
def get_attr(fp, pathstring, db):
    try:
        track = track_from_file(fp, 'mp3')
    except Exception:
        return

    beatsavg = None
    beatsdev = None
    barsavg = None
    barsdev = None
    sectionsavg = None
    sectionsdev = None
    sectionscount = None
    segmentsavg = None
    segmentsdev = None
    tatumsavg = None
    tatumsdev = None
    tatumscount = None
    thisartist = None
    thisdanceability = None
    thisduration = None
    thisfadein = None
    thisenergy = None
    thiskey = None
    thiskeyconfidence = None
    thisliveness = None
    thisloudness = None
    thismode = None
    thismodeconfidence = None
    thisoffset = None
    thisspeechiness = None
    thisfadeout = None
    thistempo = None
    thistempoconfidence = None
    thistimesig = None
    thistimesigcon = None
    thistitle = None
        
    if hasattr(track, 'beats') and len(track.beats) > 0:
        beatsavg = get_average(track.beats, 'duration')
        beatsdev = get_deviation(track.beats, 'duration', beatsavg)
    if hasattr(track, 'bars') and len(track.bars) > 0:
        barsavg = get_average(track.bars, 'duration')
        barsdev = get_deviation(track.bars, 'duration', barsavg)
    if hasattr(track, 'sections') and len(track.sections) > 0:
        sectionsavg = get_average(track.sections, 'duration')
        sectionsdev = get_deviation(track.sections, 'duration', sectionsavg)
        sectionscount = len(track.sections)
    if hasattr(track, 'segments') and len(track.segments) > 0:
        segmentsavg = get_average(track.segments, 'duration')
        segmentsdev = get_deviation(track.segments, 'duration', segmentsavg)
    if hasattr(track, 'tatums') and len(track.tatums) > 0:
        tatumsavg = get_average(track.tatums, 'duration')
        tatumsdev = get_deviation(track.tatums, 'duration', tatumsavg)
        tatumscount = len(track.tatums)

    if hasattr(track, 'artist'):
        thisartist = str(track.artist)
    if hasattr(track, 'danceability'):
        thisdanceability = track.danceability
    if hasattr(track, 'duration'):
        thisduration = track.duration
    if hasattr(track, 'end_of_fade_in'):
        thisfadein = track.end_of_fade_in
    if hasattr(track, 'energy'):
        thisenergy = track.energy
    if hasattr(track, 'key'):
        thiskey = track.key
    if hasattr(track, 'key_confidence'):
        thiskeyconfidence = track.key_confidence
    if hasattr(track, 'liveness'):
        thisliveness = track.liveness
    if hasattr(track, 'loudness'):
        thisloudness = track.loudness
    if hasattr(track, 'mode'):
        thismode = track.mode
    if hasattr(track, 'mode_confidence'):
        thismodeconfidence = track.mode_confidence
    if hasattr(track, 'offset_seconds'):
        thisoffset = track.offset_seconds
    if hasattr(track, 'speechiness'):
        thisspeechiness = track.speechiness
    if hasattr(track, 'start_of_fade_out'):
        thisfadeout = track.start_of_fade_out
    if hasattr(track, 'tempo'):
        thistempo = track.tempo
    if hasattr(track, 'tempo_confidence'):
        thistempoconfidence = track.tempo_confidence
    if hasattr(track, 'time_signature'):
        thistimesig = track.time_signature
    if hasattr(track, 'time_signature_confidence'):
        thistimesigcon = track.time_signature_confidence
    if hasattr(track, 'title'):
        thistitle = str(track)

    
    song = { songFilePath['name']: pathstring,
             songTitle['name']: thistitle,
             songArtist['name']: thisartist,
             songBeatAverage['name']: beatsavg,
             songBeatDeviation['name']: beatsdev,
             songBarsAverage['name']: barsavg,
             songBarsDeviation['name']: barsdev,
             songDanceability['name']: thisdanceability,
             songDuration['name']: thisduration,
             songEndOfFadeIn['name']: thisfadein,
             songEnergy['name']: thisenergy,
             songKey['name']: thiskey,
             songKeyConfidence['name']: thiskeyconfidence,
             songLiveness['name']: thisliveness,
             songLoudness['name']: thisloudness,
             songMode['name']: thismode,
             songModeConfidence['name']: thismodeconfidence,
             songOffsetSeconds['name']: thisoffset,
             songSectionsAverage['name']: sectionsavg,
             songSectionsDeviation['name']: sectionsdev,
             songSectionsCount['name']: sectionscount,
             songSpeechiness['name']: thisspeechiness,
             songStartOfFadeOut['name']: thisfadeout,
             songTatumsAverage['name']: tatumsavg,
             songTatumsDeviation['name']: tatumsdev,
             songTatumsCount['name']: tatumscount,
             songTempo['name']: thistempo,
             songTempoConfidence['name']: thistempoconfidence,
             songTimeSignature['name']: thistimesig,
             songTimeSignatureConfidence['name']: thistimesigcon}
 
    ## calls a function to place these attributes in the DB
     # instead, should make this call through the DB abstraction layer
    db.add_song(song)

## function to average a specific set of values found in a dict
def get_average(array, feature):
    if len(array) > 0:
        aggr = 0
        for k in array:
            aggr += k[feature]
        return aggr/len(array)
    else:
        return 0

## function to get the standard deviation of a set of values found in a dict
 # requires that the average is computed first and passed as an argument
def get_deviation(array, feature, average):
    if len(array) > 0:
        aggr = 0
        for k in array:
            aggr += math.pow((k[feature] - average), 2)
        return math.sqrt(aggr/len(array))
    else:
        return 0
    