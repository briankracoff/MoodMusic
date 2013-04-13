# Author: Brian Kracoff
'''
Database fields and their types
'''

from collections import namedtuple

#Common keys
commonId = "id"
commonHash = "hash"
commonTitle = "title"
commonArtist = "artist"
commonPath = "filepath"

FieldInfo = namedtuple('FieldInfo', 'name type')

#Song namespace
songNamespace = "Song"
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


#Mood namespace
moodNamespace = "Mood"
moodTitle = "title"
