from Learner import Learner
from random import shuffle
import numpy as np

class Playlist:
    
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
            moods = self._db.all_moods()

        songs = np.array(songs)

        moods = self._get_mood_list(songs, moods)
        hashes = songs[:,0]
        songs = songs[:,1:].astype(float)
        
        return hashes, songs, moods

    def _compute_model(self, songs, moods):
        ''' compute the model of given songs with their ratings '''
        self._generator.model_songs(songs, moods)

    def generate_list(self):
        ''' 
        generate a playlist after computing a model of the 
        songs and mood assignments currently in the db
        '''
        hashes, songs, moods = self._get_songs_and_moods()
        
        self._compute_model(songs, moods)

        header, categs = self._generator.categorize_songs_probab(songs)

        moodsIndices = [header.index(m) for m in self._moods]
        mergeCats = [sum([x[i] for i in moodsIndices])/len(moodsIndices) 
                     for x in categs]
        self._list = [hashes[i] for i,x in enumerate(mergeCats) if x > .6]
        shuffle(self._list)

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
