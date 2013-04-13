#! /usr/bin/python

from data.DB_Helper import *
import os
import math
from config import *
from itertools import tee, izip

from pyechonest import config as pyechonest_config
from pyechonest.track import track_from_file

#Sets the EchoNest api Key
#MUST be called before EchoNest can be used
def set_api_key():
    pyechonest_config.ECHO_NEST_API_KEY = Config().get_attr('ECHO_NEST_API_KEY')

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
    thisloudnessmaxaverage = None
    thisloudnessmaxdeviation = None
    thisloudnessmaxdifferential = None
    thisloudnessmaxtimeaverage = None
    thisloudnessmaxtimedeviation = None
    thisloudnessmaxtimedifferential = None
    thisloudnessstartaverage = None
    thisloudnessstartdeviation = None
    thisloudnessstartdifferential = None

    thistimbreaverage = [None, None, None, None, None, None, None, None, None, None, None, None]
    thistimbredev = [None, None, None, None, None, None, None, None, None, None, None, None]
    thistimbrediff = [None, None, None, None, None, None, None, None, None, None, None, None]
    thispitchaverage = [None, None, None, None, None, None, None, None, None, None, None, None]
    thispitchdev = [None, None, None, None, None, None, None, None, None, None, None, None]
    thispitchdiff = [None, None, None, None, None, None, None, None, None, None, None, None]
    thispitchratioa = [None, None, None, None, None, None, None, None, None, None, None, None]
    thispitchratiob = [None, None, None, None, None, None, None, None, None, None, None, None]
    
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

    if hasattr(track, 'segments') and len(track.segments) != 0:
        loudness_maxarray = []
        loudness_max_timearray = []
        loudness_startarray = []
        timbrearrays = [],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[]
        pitcharrays = [],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[]

        for k in track.segments:
            loudness_maxarray.append(k['loudness_max'])
            loudness_max_timearray.append(k['loudness_max_time'])
            loudness_startarray.append(k['loudness_start'])
            
            i = 0
            while i < 12:
                timbrearrays[i].append(k['timbre'][i])
                i += 1
            i = 0
            while i < 12:
                pitcharrays[i].append(k['pitches'][i])
                i += 1

        avg = get_aver(loudness_maxarray)
        thisloudnessmaxaverage = avg
        thisloudnessmaxdeviation = get_devi(loudness_maxarray, avg)
        thisloudnessmaxdifferential = get_differential(loudness_maxarray)
        
        avg = get_aver(loudness_max_timearray)
        thisloudnessmaxtimeaverage = avg
        thisloudnessmaxtimedeviation = get_devi(loudness_max_timearray, avg)
        thisloudnessmaxtimedifferential =  get_differential(loudness_max_timearray)
        
        avg = get_aver(loudness_startarray)
        thisloudnessstartaverage = avg
        thisloudnessstartdeviation = get_devi(loudness_startarray, avg)
        thisloudnessstartdifferential = get_differential(loudness_startarray)
        
        i = 0
        while i < 12:
            avg = get_aver(timbrearrays[i])
            thistimbreaverage[i] = avg
            thistimbredev[i] = get_devi(timbrearrays[i], avg)
            thistimbrediff[i] = get_differential(timbrearrays[i])
            avg = get_aver(pitcharrays[i])
            thispitchaverage[i] = avg
            thispitchdev[i] = get_devi(pitcharrays[i], avg)
            thispitchdiff[i] = get_differential(pitcharrays[i])
            thispitchratioa[i] = get_ratio(pitcharrays[i], .5)
            thispitchratiob[i] = get_ratio(pitcharrays[i], 1)
            i += 1
        

    
    song = { songFilePath.name: pathstring,
             songTitle.name: thistitle,
             songArtist.name: thisartist,
             songBeatAverage.name: beatsavg,
             songBeatDeviation.name: beatsdev,
             songBarsAverage.name: barsavg,
             songBarsDeviation.name: barsdev,
             songDanceability.name: thisdanceability,
             songDuration.name: thisduration,
             songEndOfFadeIn.name: thisfadein,
             songEnergy.name: thisenergy,
             songKey.name: thiskey,
             songKeyConfidence.name: thiskeyconfidence,
             songLiveness.name: thisliveness,
             songLoudness.name: thisloudness,
             songMode.name: thismode,
             songModeConfidence.name: thismodeconfidence,
             songOffsetSeconds.name: thisoffset,
             songSectionsAverage.name: sectionsavg,
             songSectionsDeviation.name: sectionsdev,
             songSectionsCount.name: sectionscount,
             songSpeechiness.name: thisspeechiness,
             songStartOfFadeOut.name: thisfadeout,
             songTatumsAverage.name: tatumsavg,
             songTatumsDeviation.name: tatumsdev,
             songTatumsCount.name: tatumscount,
             songTempo.name: thistempo,
             songTempoConfidence.name: thistempoconfidence,
             songTimeSignature.name: thistimesig,
             songTimeSignatureConfidence.name: thistimesigcon,
             songLoudnessMaxAverage.name: thisloudnessmaxaverage,
             songLoudnessMaxDeviation.name: thisloudnessmaxdeviation,
             songLoudnessMaxDifferential.name: thisloudnessmaxdifferential,
             songLoudnessMaxTimeAverage.name: thisloudnessmaxtimeaverage,
             songLoudnessMaxTimeDeviation.name: thisloudnessmaxtimedeviation,
             songLoudnessMaxTimeDifferential.name: thisloudnessmaxtimedifferential,
             songLoudnessStartAverage.name: thisloudnessstartaverage,
             songLoudnessStartDeviation.name: thisloudnessstartdeviation,
             songLoudnessStartDifferential.name: thisloudnessstartdifferential,
             songTimbre1Average.name: thistimbreaverage[0],
             songTimbre1Dev.name: thistimbredev[0],
             songTimbre1Diff.name: thistimbrediff[0],
             songTimbre2Average.name: thistimbreaverage[1],
             songTimbre2Dev.name: thistimbredev[1],
             songTimbre2Diff.name: thistimbrediff[1],
             songTimbre3Average.name: thistimbreaverage[2],
             songTimbre3Dev.name: thistimbredev[2],
             songTimbre3Diff.name: thistimbrediff[2],
             songTimbre4Average.name: thistimbreaverage[3],
             songTimbre4Dev.name: thistimbredev[3],
             songTimbre4Diff.name: thistimbrediff[3],
             songTimbre5Average.name: thistimbreaverage[4],
             songTimbre5Dev.name: thistimbredev[4],
             songTimbre5Diff.name: thistimbrediff[4],
             songTimbre6Average.name: thistimbreaverage[5],
             songTimbre6Dev.name: thistimbredev[5],
             songTimbre6Diff.name: thistimbrediff[5],
             songTimbre7Average.name: thistimbreaverage[6],
             songTimbre7Dev.name: thistimbredev[6],
             songTimbre7Diff.name: thistimbrediff[6],
             songTimbre8Average.name: thistimbreaverage[7],
             songTimbre8Dev.name: thistimbredev[7],
             songTimbre8Diff.name: thistimbrediff[7],
             songTimbre9Average.name: thistimbreaverage[8],
             songTimbre9Dev.name: thistimbredev[8],
             songTimbre9Diff.name: thistimbrediff[8],
             songTimbre10Average.name: thistimbreaverage[9],
             songTimbre10Dev.name: thistimbredev[9],
             songTimbre10Diff.name: thistimbrediff[9],
             songTimbre11Average.name: thistimbreaverage[10],
             songTimbre11Dev.name: thistimbredev[10],
             songTimbre11Diff.name: thistimbrediff[10],
             songTimbre12Average.name: thistimbreaverage[11],
             songTimbre12Dev.name: thistimbredev[11],
             songTimbre12Diff.name: thistimbrediff[11],
             songPitch1Average.name: thispitchaverage[0],
             songPitch1Dev.name: thispitchdev[0],
             songPitch1Diff.name: thispitchdiff[0],
             songPitch2Average.name: thispitchaverage[1],
             songPitch2Dev.name: thispitchdev[1],
             songPitch2Diff.name: thispitchdiff[1],
             songPitch3Average.name: thispitchaverage[2],
             songPitch3Dev.name: thispitchdev[2],
             songPitch3Diff.name: thispitchdiff[2],
             songPitch4Average.name: thispitchaverage[3],
             songPitch4Dev.name: thispitchdev[3],
             songPitch4Diff.name: thispitchdiff[3],
             songPitch5Average.name: thispitchaverage[4],
             songPitch5Dev.name: thispitchdev[4],
             songPitch5Diff.name: thispitchdiff[4],
             songPitch6Average.name: thispitchaverage[5],
             songPitch6Dev.name: thispitchdev[5],
             songPitch6Diff.name: thispitchdiff[5],
             songPitch7Average.name: thispitchaverage[6],
             songPitch7Dev.name: thispitchdev[6],
             songPitch7Diff.name: thispitchdiff[6],
             songPitch8Average.name: thispitchaverage[7],
             songPitch8Dev.name: thispitchdev[7],
             songPitch8Diff.name: thispitchdiff[7],
             songPitch9Average.name: thispitchaverage[8],
             songPitch9Dev.name: thispitchdev[8],
             songPitch9Diff.name: thispitchdiff[8],
             songPitch10Average.name: thispitchaverage[9],
             songPitch10Dev.name: thispitchdev[9],
             songPitch10Diff.name: thispitchdiff[9],
             songPitch11Average.name: thispitchaverage[10],
             songPitch11Dev.name: thispitchdev[10],
             songPitch11Diff.name: thispitchdiff[10],
             songPitch12Average.name: thispitchaverage[11],
             songPitch12Dev.name: thispitchdev[11],
             songPitch12Diff.name: thispitchdiff[11],
             songPitch1Ratioa.name: thispitchratioa[0],
             songPitch2Ratioa.name: thispitchratioa[1],
             songPitch3Ratioa.name: thispitchratioa[2],
             songPitch4Ratioa.name: thispitchratioa[3],
             songPitch5Ratioa.name: thispitchratioa[4],
             songPitch6Ratioa.name: thispitchratioa[5],
             songPitch7Ratioa.name: thispitchratioa[6],
             songPitch8Ratioa.name: thispitchratioa[7],
             songPitch9Ratioa.name: thispitchratioa[8],
             songPitch10Ratioa.name: thispitchratioa[9],
             songPitch11Ratioa.name: thispitchratioa[10],
             songPitch12Ratioa.name: thispitchratioa[11],
             songPitch1Ratiob.name: thispitchratiob[0],
             songPitch2Ratiob.name: thispitchratiob[1],
             songPitch3Ratiob.name: thispitchratiob[2],
             songPitch4Ratiob.name: thispitchratiob[3],
             songPitch5Ratiob.name: thispitchratiob[4],
             songPitch6Ratiob.name: thispitchratiob[5],
             songPitch7Ratiob.name: thispitchratiob[6],
             songPitch8Ratiob.name: thispitchratiob[7],
             songPitch9Ratiob.name: thispitchratiob[8],
             songPitch10Ratiob.name: thispitchratiob[9],
             songPitch11Ratiob.name: thispitchratiob[10],
             songPitch12Ratiob.name: thispitchratiob[11]}

 
    ## calls a function to place these attributes in the DB
     # instead, should make this call through the DB abstraction layer
    db.add_song(song)
    
def get_ratio(array, value):
    if not array:
        return None

    count = sum(1 for k in array if k >= value)

    return float(count)/float(len(array))

def get_aver(array):
    if not array:
        return None

    return float(sum(array)) / float(len(array))

def pairwise(iterable):
    "s -> (s0,s1), (s1,s2), (s2, s3), ..."
    a, b = tee(iterable)
    next(b, None)
    return izip(a, b)
    
def get_differential(array):
    if not array:
        return 0

    diffs = [second - first for first, second in pairwise(array)]

    abssum = sum(abs(k) for k in diffs)

    return float(abssum)/float(len(diffs))

## function to get the standard deviation of a set of values found in a dict
 # requires that the average is computed first and passed as an argument
def get_devi(array, average):
    if not array:
        return None

    aggr = sum((k - average)**2 for k in array)

    return math.sqrt(aggr/len(array))

## function to average a specific set of values found in a dict
def get_average(array, feature):
    if not array:
        return None

    return get_aver([k[feature] for k in array])

## function to get the standard deviation of a set of values found in a dict
 # requires that the average is computed first and passed as an argument
def get_deviation(array, feature, average):
    if not array:
        return None

    return get_devi([k[feature] for k in array], average)
