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

#Mood namespace
moodNamespace = "Mood"
moodTitle = "title"
