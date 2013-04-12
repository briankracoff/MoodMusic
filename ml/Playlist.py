
from Learner import Learner
from random import shuffle
import numpy as np
from song.song import Song

from data.DB_constants import *

class Playlist:

    _excludeSongs = [commonHash, commonId, songFilePath.name,
                     songTitle.name, songArtist.name]
    _excludeMoods = [commonHash, commonId]
    
    def __init__(self, dbHelp, moods):
        ''' construct playlist object '''
        self._list = []
        self._currentI = 0
        self._moods = []
        self._generator = Learner(moods)
        self._db = dbHelp

    def add_mood(self, mood):
        ''' add mood classifier to playlist '''
        self._moods.append(mood)

    def add_moods(self, moods):
        ''' add a batch of mood classifiers to playlist '''
        self._moods += moods

    def reset_mood(self):
        ''' reset mood classifiers at work here '''
        self._moods = []

    def _get_songs_and_moods(self, songs=None, moods=None):
        ''' 
        retrieve (if necessary) songs and attribute 
        data, match to moods from mood table and pull
        out hashes 
        '''
        if songs == None:
            songs = self._db.all_songs()
        if moods == None:
            moods = self._db.all_song_moods()

        songs = np.array(self._prune(songs, Playlist._excludeSongs))
        moods = self._prune(moods, Playlist._excludeMoods)

        moods = self._get_mood_list(songs, moods)
        hashes = songs[:,0]
        songs = songs[:,1:].astype(float)
        
        return hashes, songs, moods

    def _prune(self, stuff, exclude):
        newStuff = []
        for row in stuff:
            newRow = [row[commonHash]]
            for item in row.keys():
                if item not in exclude:
                    newRow.append(row[item])
            newStuff.append(newRow)
        return newStuff

    def _compute_model(self):
        ''' compute the model of given songs with their ratings '''
        hashes, songs, moods = self._get_songs_and_moods()

        if len(hashes) == 0 or all(x == -1 for x in moods):
            print ("Must have songs in database and assign at "
                   "least one song to a mood.")
            return [], [], []
        self._generator.model_songs(songs, moods)

        return hashes, songs, moods

    def generate_list_mood(self):
        ''' 
        generate a playlist after computing a model of the 
        songs and mood assignments currently in the db
        '''
        hashes, songs, moods = self._compute_model()
        if len(hashes) == 0:
            return 

        header, categs = self._generator.categorize_songs_probab(songs)

        moodsIndices = [header.index(m) for m in self._moods]
    
        mergeCats = [(hashes[j],sum([x[i] for i in moodsIndices])) 
                     for j,x in enumerate(categs) 
                     if sum([x[i] for i in moodsIndices]) > .5]
        self._to_list([pair[0] for pair in sorted(mergeCats, reverse=True)])

    def generate_list_song(self, kernelsong):
        '''
        generates playlist based on a given song
        '''
        hashes, songs, moods = self._compute_model()
        if len(hashes) == 0:
            return 

        header, categs = self._generator.categorize_songs_probab(songs)

        i = list(hashes).index(str(kernelsong))
        kernelish = categs[i]
        self._to_list([hashes[i] for i,x in enumerate(categs) 
                       if self._similar(x, kernelish)])

    def _similar(self, one, two):
        '''decides if two same-length lists are similar'''
        avgDiff = sum([abs(two[i] - x) for i,x in enumerate(one)])
        avgDiff = avgDiff/len(one)
         
        return avgDiff < .15

    def _to_list(self, songs):
        '''converts list of hashes to list of filepaths'''
        files = []
        for x in songs:
            files.append(Song.song_from_filepath(self._db.hash_to_file(x)))
            
        # shuffle(files)
        self._list = files

    def _get_mood_list(self, songs, moods):
        ''' 
        match mood table data to song data (this sucks and should be 
        improved) 
        '''
        ms = []
        for i,x in enumerate(songs):
            ms.append(-1)
            for m in moods:
                if x[0] == m[0]:
                    ms[i] = m[1]
                    
        return ms

    def get_next_song(self):
        ''' return next song in list '''
        self._currentI += 1
        return self._list[self._currentI]
    
    def has_next_song(self):
        ''' ask if the playlist has a next song '''
        return self._currentI < len(self._list) - 1

    def get_current_song(self):
        ''' return currently playing song '''
        return self._list[self._currentI]

    def get_list(self, length=50):
        ''' '''
        plist = self._list[:length]
        shuffle(plist)
        return plist
