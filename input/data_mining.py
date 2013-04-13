#! /usr/bin/python

from data.DB_Helper import *
import os
import math
from config import *
from itertools import tee, izip

from pyechonest import config as pyechonest_config
from pyechonest.track import track_from_file

#Song namespace
songBeatAverage = FieldInfo("beat_average", 'REAL')
songBeatDeviation = FieldInfo("beat_deviation", 'REAL')
songBarsAverage = FieldInfo("bars_average", 'REAL')
songBarsDeviation = FieldInfo('bars_deviation', 'REAL')
songDanceability = FieldInfo('danceability' , 'REAL')
songDuration = FieldInfo('duration' , 'REAL')
songEndOfFadeIn = FieldInfo('end_of_fade_in', 'REAL')
songEnergy = FieldInfo('energy', 'REAL')
songKey = FieldInfo('key' , 'INT')
songKeyConfidence = FieldInfo('key_confidence' , 'REAL')
songLiveness = FieldInfo('liveness' , 'REAL')
songLoudness = FieldInfo('loudness' , 'REAL')
songMode = FieldInfo('mode', 'INT')
songModeConfidence = FieldInfo('mode_confidence', 'REAL')
songOffsetSeconds = FieldInfo('offset_seconds' , 'REAL')
songSectionsAverage = FieldInfo('sections_average', 'REAL')
songSectionsDeviation = FieldInfo('sections_deviation', 'REAL')
songSectionsCount = FieldInfo('sections_count' , 'INT')
songSpeechiness = FieldInfo('speechiness', 'REAL')
songStartOfFadeOut = FieldInfo('start_of_fade_out', 'REAL')
songTatumsAverage = FieldInfo('tatums_average', 'REAL')
songTatumsDeviation = FieldInfo('tatums_deviation' , 'REAL')
songTatumsCount = FieldInfo('tatums_count', 'INT')
songTempo = FieldInfo('tempo', 'REAL')
songTempoConfidence = FieldInfo('tempo_confidence', 'REAL')
songTimeSignature = FieldInfo('time_signature', 'REAL')
songTimeSignatureConfidence = FieldInfo('time_signature_confidence', 'REAL')
songLoudnessMaxAverage = FieldInfo('loudness_max_average', 'REAL')
songLoudnessMaxDeviation = FieldInfo('loudness_max_deviation', 'REAL')
songLoudnessMaxDifferential = FieldInfo('loudness_max_differential', 'REAL')
songLoudnessMaxTimeAverage = FieldInfo('loudness_max_time_average', 'REAL')
songLoudnessMaxTimeDeviation = FieldInfo('loudness_max_time_deviation', 'REAL')
songLoudnessMaxTimeDifferential = FieldInfo('loudness_max_time_differential', 'REAL')
songLoudnessStartAverage = FieldInfo('loudness_start_average', 'REAL')
songLoudnessStartDeviation = FieldInfo('loudness_start_deviation', 'REAL')
songLoudnessStartDifferential = FieldInfo('loudness_start_differential', 'REAL')
songTimbre1Average = FieldInfo('timbre1_avg', 'REAL')
songTimbre1Dev = FieldInfo('timbre1_dev', 'REAL')
songTimbre1Diff = FieldInfo('timbre1_diff', 'REAL')
songTimbre2Average = FieldInfo('timbre2_avg', 'REAL')
songTimbre2Dev = FieldInfo('timbre2_dev', 'REAL')
songTimbre2Diff = FieldInfo('timbre2_diff', 'REAL')
songTimbre3Average = FieldInfo('timbre3_avg', 'REAL')
songTimbre3Dev = FieldInfo('timbre3_dev', 'REAL')
songTimbre3Diff = FieldInfo('timbre3_diff', 'REAL')
songTimbre4Average = FieldInfo('timbre4_avg', 'REAL')
songTimbre4Dev = FieldInfo('timbre4_dev', 'REAL')
songTimbre4Diff = FieldInfo('timbre4_diff', 'REAL')
songTimbre5Average = FieldInfo('timbre5_avg', 'REAL')
songTimbre5Dev = FieldInfo('timbre5_dev', 'REAL')
songTimbre5Diff = FieldInfo('timbre5_diff', 'REAL')
songTimbre6Average = FieldInfo('timbre6_avg', 'REAL')
songTimbre6Dev = FieldInfo('timbre6_dev', 'REAL')
songTimbre6Diff = FieldInfo('timbre6_diff', 'REAL')
songTimbre7Average = FieldInfo('timbre7_avg', 'REAL')
songTimbre7Dev = FieldInfo('timbre7_dev', 'REAL')
songTimbre7Diff = FieldInfo('timbre7_diff', 'REAL')
songTimbre8Average = FieldInfo('timbre8_avg', 'REAL')
songTimbre8Dev = FieldInfo('timbre8_dev', 'REAL')
songTimbre8Diff = FieldInfo('timbre8_diff', 'REAL')
songTimbre9Average = FieldInfo('timbre9_avg', 'REAL')
songTimbre9Dev = FieldInfo('timbre9_dev', 'REAL')
songTimbre9Diff = FieldInfo('timbre9_diff', 'REAL')
songTimbre10Average = FieldInfo('timbre10_avg', 'REAL')
songTimbre10Dev = FieldInfo('timbre10_dev', 'REAL')
songTimbre10Diff = FieldInfo('timbre10_diff', 'REAL')
songTimbre11Average = FieldInfo('timbre11_avg', 'REAL')
songTimbre11Dev = FieldInfo('timbre11_dev', 'REAL')
songTimbre11Diff = FieldInfo('timbre11_diff', 'REAL')
songTimbre12Average = FieldInfo('timbre12_avg', 'REAL')
songTimbre12Dev = FieldInfo('timbre12_dev', 'REAL')
songTimbre12Diff = FieldInfo('timbre12_diff', 'REAL')
songPitch1Average = FieldInfo('pitch1_avg', 'REAL')
songPitch1Dev = FieldInfo('pitch1_dev', 'REAL')
songPitch1Diff = FieldInfo('pitch1_diff', 'REAL')
songPitch2Average = FieldInfo('pitch2_avg', 'REAL')
songPitch2Dev = FieldInfo('pitch2_dev', 'REAL')
songPitch2Diff = FieldInfo('pitch2_diff', 'REAL')
songPitch3Average = FieldInfo('pitch3_avg', 'REAL')
songPitch3Dev = FieldInfo('pitch3_dev', 'REAL')
songPitch3Diff = FieldInfo('pitch3_diff', 'REAL')
songPitch4Average = FieldInfo('pitch4_avg', 'REAL')
songPitch4Dev = FieldInfo('pitch4_dev', 'REAL')
songPitch4Diff = FieldInfo('pitch4_diff', 'REAL')
songPitch5Average = FieldInfo('pitch5_avg', 'REAL')
songPitch5Dev = FieldInfo('pitch5_dev', 'REAL')
songPitch5Diff = FieldInfo('pitch5_diff', 'REAL')
songPitch6Average = FieldInfo('pitch6_avg', 'REAL')
songPitch6Dev = FieldInfo('pitch6_dev', 'REAL')
songPitch6Diff = FieldInfo('pitch6_diff', 'REAL')
songPitch7Average = FieldInfo('pitch7_avg', 'REAL')
songPitch7Dev = FieldInfo('pitch7_dev', 'REAL')
songPitch7Diff = FieldInfo('pitch7_diff', 'REAL')
songPitch8Average = FieldInfo('pitch8_avg', 'REAL')
songPitch8Dev = FieldInfo('pitch8_dev', 'REAL')
songPitch8Diff = FieldInfo('pitch8_diff', 'REAL')
songPitch9Average = FieldInfo('pitch9_avg', 'REAL')
songPitch9Dev = FieldInfo('pitch9_dev', 'REAL')
songPitch9Diff = FieldInfo('pitch9_diff', 'REAL')
songPitch10Average = FieldInfo('pitch10_avg', 'REAL')
songPitch10Dev = FieldInfo('pitch10_dev', 'REAL')
songPitch10Diff = FieldInfo('pitch10_diff', 'REAL')
songPitch11Average = FieldInfo('pitch11_avg', 'REAL')
songPitch11Dev = FieldInfo('pitch11_dev', 'REAL')
songPitch11Diff = FieldInfo('pitch11_diff', 'REAL')
songPitch12Average = FieldInfo('pitch12_avg', 'REAL')
songPitch12Dev = FieldInfo('pitch12_dev', 'REAL')
songPitch12Diff = FieldInfo('pitch12_diff', 'REAL')
songPitch1Ratioa = FieldInfo('pitch1_ratio_a', 'REAL')
songPitch2Ratioa = FieldInfo('pitch2_ratio_a', 'REAL')
songPitch3Ratioa = FieldInfo('pitch3_ratio_a', 'REAL')
songPitch4Ratioa = FieldInfo('pitch4_ratio_a', 'REAL')
songPitch5Ratioa = FieldInfo('pitch5_ratio_a', 'REAL')
songPitch6Ratioa = FieldInfo('pitch6_ratio_a', 'REAL')
songPitch7Ratioa = FieldInfo('pitch7_ratio_a', 'REAL')
songPitch8Ratioa = FieldInfo('pitch8_ratio_a', 'REAL')
songPitch9Ratioa = FieldInfo('pitch9_ratio_a', 'REAL')
songPitch10Ratioa = FieldInfo('pitch10_ratio_a', 'REAL')
songPitch11Ratioa = FieldInfo('pitch11_ratio_a', 'REAL')
songPitch12Ratioa = FieldInfo('pitch12_ratio_a', 'REAL')
songPitch1Ratiob = FieldInfo('pitch1_ratio_b', 'REAL')
songPitch2Ratiob = FieldInfo('pitch2_ratio_b', 'REAL')
songPitch3Ratiob = FieldInfo('pitch3_ratio_b', 'REAL')
songPitch4Ratiob = FieldInfo('pitch4_ratio_b', 'REAL')
songPitch5Ratiob = FieldInfo('pitch5_ratio_b', 'REAL')
songPitch6Ratiob = FieldInfo('pitch6_ratio_b', 'REAL')
songPitch7Ratiob = FieldInfo('pitch7_ratio_b', 'REAL')
songPitch8Ratiob = FieldInfo('pitch8_ratio_b', 'REAL')
songPitch9Ratiob = FieldInfo('pitch9_ratio_b', 'REAL')
songPitch10Ratiob = FieldInfo('pitch10_ratio_b', 'REAL')
songPitch11Ratiob = FieldInfo('pitch11_ratio_b', 'REAL')
songPitch12Ratiob = FieldInfo('pitch12_ratio_b', 'REAL')

attribute_schema = [
    songBeatAverage,
    songBeatDeviation,
    songBarsAverage,
    songBarsDeviation,
    songDanceability,
    songDuration,
    songEndOfFadeIn,
    songEnergy,
    songKey,
    songKeyConfidence,
    songLiveness,
    songLoudness,
    songMode,
    songModeConfidence,
    songOffsetSeconds,
    songSectionsAverage,
    songSectionsDeviation,
    songSectionsCount,
    songSpeechiness,
    songStartOfFadeOut,
    songTatumsAverage,
    songTatumsDeviation,
    songTatumsCount,
    songTempo,
    songTempoConfidence,
    songTimeSignature,
    songTimeSignatureConfidence,
    songLoudnessMaxAverage,
    songLoudnessMaxDeviation,
    songLoudnessMaxDifferential,
    songLoudnessMaxTimeAverage,
    songLoudnessMaxTimeDeviation,
    songLoudnessMaxTimeDifferential,
    songLoudnessStartAverage,
    songLoudnessStartDeviation,
    songLoudnessStartDifferential,
    songTimbre1Average,
    songTimbre1Dev,
    songTimbre1Diff,
    songTimbre2Average,
    songTimbre2Dev,
    songTimbre2Diff,
    songTimbre3Average,
    songTimbre3Dev,
    songTimbre3Diff,
    songTimbre4Average,
    songTimbre4Dev,
    songTimbre4Diff,
    songTimbre5Average,
    songTimbre5Dev,
    songTimbre5Diff,
    songTimbre6Average,
    songTimbre6Dev,
    songTimbre6Diff,
    songTimbre7Average,
    songTimbre7Dev,
    songTimbre7Diff,
    songTimbre8Average,
    songTimbre8Dev,
    songTimbre8Diff,
    songTimbre9Average,
    songTimbre9Dev,
    songTimbre9Diff,
    songTimbre10Average,
    songTimbre10Dev,
    songTimbre10Diff,
    songTimbre11Average,
    songTimbre11Dev,
    songTimbre11Diff,
    songTimbre12Average,
    songTimbre12Dev,
    songTimbre12Diff,
    songPitch1Average,
    songPitch1Dev,
    songPitch1Diff,
    songPitch2Average,
    songPitch2Dev,
    songPitch2Diff,
    songPitch3Average,
    songPitch3Dev,
    songPitch3Diff,
    songPitch4Average,
    songPitch4Dev,
    songPitch4Diff,
    songPitch5Average,
    songPitch5Dev,
    songPitch5Diff,
    songPitch6Average,
    songPitch6Dev,
    songPitch6Diff,
    songPitch7Average,
    songPitch7Dev,
    songPitch7Diff,
    songPitch8Average,
    songPitch8Dev,
    songPitch8Diff,
    songPitch9Average,
    songPitch9Dev,
    songPitch9Diff,
    songPitch10Average,
    songPitch10Dev,
    songPitch10Diff,
    songPitch11Average,
    songPitch11Dev,
    songPitch11Diff,
    songPitch12Average,
    songPitch12Dev,
    songPitch12Diff,
    songPitch1Ratioa,
    songPitch2Ratioa,
    songPitch3Ratioa,
    songPitch4Ratioa,
    songPitch5Ratioa,
    songPitch6Ratioa,
    songPitch7Ratioa,
    songPitch8Ratioa,
    songPitch9Ratioa,
    songPitch10Ratioa,
    songPitch11Ratioa,
    songPitch12Ratioa,
    songPitch1Ratiob,
    songPitch2Ratiob,
    songPitch3Ratiob,
    songPitch4Ratiob,
    songPitch5Ratiob,
    songPitch6Ratiob,
    songPitch7Ratiob,
    songPitch8Ratiob,
    songPitch9Ratiob,
    songPitch10Ratiob,
    songPitch11Ratiob,
    songPitch12Ratiob
]

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
        

    
    song = { commonPath: pathstring,
             commonTitle: thistitle,
             commonArtist: thisartist,
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

    return get_aver([abs(second - first) for first, second
                                         in pairwise(array)])

## function to get the standard deviation of a set of values found in a dict
 # requires that the average is computed first and passed as an argument
def get_devi(array, average):
    if not array:
        return None

    return math.sqrt(get_aver([(k - average)**2 for k in array]))

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
