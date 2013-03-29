'''
Created on Mar 29, 2013

@author: Behrooz Afghahi
@version: 0.1
'''

import os

class Filesystem(object):
    '''
    Read user library from a path and import all songs
    '''
    
    __extensions = ['.mp3','.m4a']
    __files = []

    def __init__(self, max_size):
        '''
        Constructor, returns the first `max_size` files from the filesystem
        '''
        self.__max_size = max_size
    
    def Import(self, params):
        '''
        Reads a directory and returns a list of files it contains that match the
        extensions. params should contain "path" which is the path of directory
        to search.
        '''
        
        if "path" not in params or self.__max_size < 1:
            return False
        
        path = params["path"]
        
        if not (os.path.isdir(path) and os.access(path, os.F_OK | os.R_OK)):
            return False
        
        if path[-1] == os.sep:
            path = path[0:-1]
        
        for f in os.listdir(path):
            if os.path.isfile(path + os.sep + f):
                self.ImportFile(path + os.sep + f)
            else:
                self.Import({"path": path + os.sep + f})
        
        return self.__files
        
    def ImportFile(self, file_path):
        '''
        Imports a single file, if it exists and its readable
        '''
        if os.access(file_path, os.F_OK | os.R_OK) and \
        os.path.splitext(file_path)[1] in self.__extensions:
            self.__files.append(file_path)
            self.__max_size -= 1
            
    def getFiles(self):
        '''
        Returns a list of found music files
        '''
        return self.__files