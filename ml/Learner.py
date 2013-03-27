
from sklearn.semi_supervised import LabelSpreading

class Learner 
    
    def __init__(self, moods, mode=LabelSpreading):
        # identify moods as integers
        self._moodToInt = dict((m,i) for i,m in enumerate(moods))
        # and vice versa
        self._intToMood = dict((i,m) for i,m in enumerate(moods))
        
        self._model = mode()

    def model_songs(listOfSongs):
        data = [song.get_attr() + [m]
                for m in song.get_moods() 
                for song in listOfSongs]
        
        data = self._normalize(np.array(data[:,:-1]))
        
        self._model.fit(data[:,:-1], data[:,-1])

    def categorize_songs_single(listOfSongs):
        data = np.array([song.get_attr() for song in listOfSongs])
        predictions = self._model.predict(data)
        
        return self._convert_int_to_mood(predictions)

    def categorize_songs_probab(listOfSongs):
        data = np.array([song.get_attr() for song in listOfSongs])
        predictions = self._model.predict_proba(data)
        
        header = [self._intToMood[i] for i in xrange(predictions.shape[1])]

        return header, predictions

    def _convert_int_to_mood(arr):
        return [self._intToMood[i] for i in arr.tolist()]

    def _normalize(arr):
        for i in arr.shape[1]:
            arr[:,i] = (arr[:,i] - arr[:,1].mean()) / arr[:,i].std()
        return arr