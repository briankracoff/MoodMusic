'''
Created on Mar 29, 2013

@author: Behrooz Afghahi
@version: 0.1
@see: /docs/API/Input.Importer.txt
'''

import os, threading
import iTunes, Filesystem
from data_mining import song_attributes
from data.DB_Helper import DB_Helper
import subprocess
from sys import stdout

class Importer(object):
    '''
    Imports the library in the background
    '''
    
    __daemon = None

    def __init__(self, path, max_files = 100):
        '''
        Tries to detect library type and import it
        '''
        
        if os.path.isfile(path):
            if os.path.splitext(path)[1].lower() == "xml":
                lib = iTunes.Input(max_files)
                self.__files = lib.Import({"xml_path": path})
            else:
                self.__files = [path]
        else:
            lib = Filesystem.Input(max_files)
            self.__files = lib.Import({"path":path})
        
        if self.__files is False:
            self.__files = []
            
    def startDaemon(self):
        '''
        Starts the daemon process
        '''
        self.__daemon = FetchData(self.fetcher)
        self.__daemon.start()
        
    def fetcher(self):
        '''
        This is called to fetch song data
        '''
        print (str(len(self.__files)))
        stdout.flush()
        db = DB_Helper(True)
        
        for song in self.__files:
            song_attributes(song, False, db)
            #print("#")
            #stdout.flush()
    
    def isAlive(self):
        '''
        Check to see if the damon is alive (maybe killed or the job is finished)
        '''
        return self.__daemon.isAlive()
    
    def join(self):
        '''
        Wait until the damon is finished.
        '''
        self.__daemon.join()

class FetchData(threading.Thread):
    '''
    Implements the Thread class to create a daemon
    '''
    
    def __init__(self, fetcher_function = None):
        '''
        Constructor
        '''
        threading.Thread.__init__(self)
        
        if fetcher_function is None:
            self.runnable = self.subprocess
        else:
            self.runnable = fetcher_function
        
        self.daemon = True
        
    def run(self):
        '''
        Call the provided runnable function
        '''
        self.runnable()
    
    def subprocess(self):
        self.process = {"total":0, "done":0}
        proc = subprocess.Popen(['python', './importer.py'], stdout=subprocess.PIPE, bufsize=1)
        
        while True:
            line = proc.stdout.readline().strip()
            if not line: break
            
            if line == "#":
                self.process["done"] += 1
            else:
                self.process["total"] = int(line)