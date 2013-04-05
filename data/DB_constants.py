# Author: Brian Kracoff
'''
Database fields and their types
'''

#Common keys
commonId = "id"
commonHash = "hash"

#Song namespace
songNamespace = "Song"
songFilePath = {'name': "filepath", 'type': 'TEXT'}
songTitle = {'name': "title", 'type': 'TEXT'} 
songArtist = {'name': "artist", 'type': 'TEXT'}
songBeatAverage = {'name': "beat_average", 'type': 'REAL'}
songBeatDeviation = {'name': "beat_deviation", 'type': 'REAL'}
songBarsAverage = {'name':"bars_average", 'type': 'REAL'}
songBarsDeviation = {'name': 'bars_deviation', 'type': 'REAL'}
songDanceability = {'name': 'danceability' , 'type': 'REAL'}
songDuration = {'name': 'duration' , 'type':'REAL'}
songEndOfFadeIn = {'name': 'end_of_fade_in', 'type': 'REAL'}
songEnergy = {'name': 'energy', 'type':'REAL'}
songKey = {'name': 'key' , 'type': 'INT'}
songKeyConfidence = {'name': 'key_confidence' , 'type': 'REAL'}
songLiveness = {'name': 'liveness' , 'type': 'REAL'}
songLoudness = {'name': 'loudness' , 'type':'REAL'}
songMode = {'name': 'mode', 'type': 'INT'}
songModeConfidence = {'name': 'mode_confidence', 'type': 'REAL'}
songOffsetSeconds = {'name': 'offset_seconds' , 'type':'REAL'}
songSectionsAverage = {'name': 'sections_average', 'type':'REAL'}
songSectionsDeviation = {'name': 'sections_deviation', 'type':'REAL'}
songSectionsCount = {'name': 'sections_count' , 'type': 'INT'}
songSpeechiness = {'name': 'speechiness', 'type':'REAL'}
songStartOfFadeOut = {'name': 'start_of_fade_out', 'type': 'REAL'}
songTatumsAverage = {'name': 'tatums_average', 'type': 'REAL'}
songTatumsDeviation = {'name': 'tatums_deviation' , 'type': 'REAL'}
songTatumsCount = {'name': 'tatums_count', 'type': 'INT'}
songTempo = {'name': 'tempo', 'type': 'REAL'}
songTempoConfidence = {'name': 'tempo_confidence', 'type': 'REAL'}
songTimeSignature = {'name': 'time_signature', 'type': 'REAL'}
songTimeSignatureConfidence = {'name': 'time_signature_confidence', 'type': 'REAL'}


#Mood namespace
moodNamespace = "Mood"
moodTitle = "title"
