'''
Created on Mar 29, 2013

@author: Behrooz Afghahi
@version: 0.1
'''

import os
import re
import urllib, urlparse

class iTunes(object):
    '''
    Read all the files from the iTunes library.xml file
    '''

    def __init__(self, max_size):
        '''
        Constructor, returns the first `max_size` files from the itunes library
        '''
        
        self.__max_size = max_size
        
    def Import(self, params):
        '''
        Imports will do all the magic, params should contain "xml_path" which is
        the path to the Library.xml file
        '''
        if "xml_path" not in params:
            return False
        
        path = params["xml_path"]
        
        if not os.path.isfile(path) or not os.access(path, os.F_OK | os.R_OK):
            return False
        
        files = []
        with open(path) as f:
            for line in f:
                if self.__max_size < 1:
                    break
                
                line = line.strip()
                if line.find('<key>Location</key>') != -1:
                    match = re.search("<string>(.*?)</string>", line)
                    
                    if match is not None:
                        p = urlparse.urlparse(match.group(1))
                        match = urllib.unquote(os.path.abspath(os.path.join(p.netloc, p.path))) 
                        
                        files.append(match)
                        self.__max_size -= 1
                
        return files