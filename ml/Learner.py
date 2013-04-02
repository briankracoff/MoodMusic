
from sklearn.semi_supervised import LabelSpreading
from scipy.stats import nanmean, nanstd

import numpy as np
import cPickle as cp

# KERNEL = 'gamma'     # fully connected, dense matrix, expensive
                       # mem+time
KERNEL = 'n_neighbors' # sparse matrix, not as expensive

class Learner:
    
    def __init__(self, moods, mode=LabelSpreading):
        # identify moods as integers
        self._moodToInt = dict((m,i) for i,m in enumerate(moods))
        # and vice versa
        self._intToMood = dict((i,m) for i,m in enumerate(moods))
        
        self._model = mode(kernel=KERNEL)

    def model_songs(self, songs, moods):
        ''' 
        take all song attributes and any mood ratings, train
        the machine learning model 
        '''
        data = self._normalize(songs)
        moods = self._convert_mood_to_int(moods)
        self._model = self._model.fit(data, moods)

    def categorize_songs_single(self, songs):
        ''' produces best fit category for list of songs'''
        data = self._normalize(songs)
        predictions = self._model.predict(data)
        return self._convert_int_to_mood(predictions)

    def categorize_songs_probab(self, songs):
        ''' produces probabilities for each song for each mood '''
        data = self._normalize(songs)
        predictions = self._model.predict_proba(data)
        header = self._convert_int_to_mood(predictions)
        return header, predictions

    def _convert_int_to_mood(self, arr):
        ''' represent ints as mood strings '''
        return [self._intToMood.get(i, -1) for i in arr.tolist()]

    def _convert_mood_to_int(self, arr):
        ''' represent moods as ints -- unassigned is -1 '''
        return [self._moodToInt.get(i, -1) for i in arr.tolist()]

    def _normalize(self, arr):
        ''' perform normalization routine on attributes ''' 
        for i in xrange(arr.shape[1]):
            arr[:,i] = (arr[:,i] - nanmean(arr[:,i])) / nanstd(arr[:,i])
        return arr

    def save(self, path):
        ''' save the model for later use '''
        cp.dump(self, open(path, 'wb'))

    @staticmethod
    def load(self, path):
        ''' load a previously created model '''
        cp.load(open(path,'rb'))


        
    
