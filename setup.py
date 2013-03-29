#! /usr/bin/python
# Resets the SqLite database to spec
# You must run this before using MoodMusic
# NOTE: RUNNING THIS WILL ERASE ALL DATA IN DB AND RESET EVERYTHING

from data.SqLite import *
from data.DB_constants import *

def get_attribute_schema():
    return [
        songFilePath,
        songTitle,
        songArtist,
        songBeatAverage,
        songBeatDeviaton,
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
        songTimeSignatureConfidence
    ]

def initializeDB():
    print "Starting setup...\n"
    db = SqLite();

    print "............................\n"
    
    #Song namespace
    print "Checking for Song namespace"
    if db.hasNamespace(songNamespace):
        print "Song namespace exists"
        print "Deleting Song namespace"
        db.removeNamespace(songNamespace)
        print "Song namespace deleted"
    else:
        print "Song namespace doesn't exist"

    print "Creating Song namespace"
    song_def = {
        commonHash:"TEXT"
    }

    for attribute in get_attribute_schema():
        song_def[attribute['name']] = attribute['type']

    db.installNamespace(songNamespace, song_def)
    print "Song namespace created\n"

    print "............................\n"

    #Mood namespace
    print "Checking for Mood namespace"
    if db.hasNamespace(moodNamespace):
        print "Mood namespace exists"
        print "Deleting Mood namespace"
        db.removeNamespace(moodNamespace)
        print "Mood namespace deleted"
    else:    
        print "Mood namespace doesn't exist"

    print "Creating Mood namespace"
    mood_def = {
        commonHash:"TEXT",
        moodTitle:"TEXT"
    }
    db.installNamespace(moodNamespace, mood_def)
    print "Mood namespace created\n"

    print "............................\n"

    print "Done with setup\nYou can now use MoodMusic\n"

if __name__ == '__main__':
    initializeDB()