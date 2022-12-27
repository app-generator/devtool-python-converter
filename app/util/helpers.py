# -*- encoding: utf-8 -*-
"""
Copyright (c) 2019 - present AppSeed.us
License: MIT
"""

from lib2to3.pgen2 import driver
import os, csv, fnmatch, time, shutil

from io import StringIO 
import sys

'''
This file should contain primitives used in other modules
'''

class COMMON:
    DB_SQLITE = 'SQLITE'
    DB_MYSQL  = 'MYSQL'
    DB_PGSQL  = 'PGSQL'

def h_list_to_s( aList, aSeparator=',' ):
    if isinstance(aList, list):
        return aSeparator.join([str(elem) for elem in aList])
    else: 
        return aList

def file_exists( aPath ):

    try:

        if open( aPath, 'r'):
            return True

    except:
        return False   

def file_p( aPath ):

    try:

        f = open( aPath, 'r') 
        
        if f:
            return f

        return None 
    except:
        return None   

def file_read( aPath, as_list=False ):

    try:

        if not file_exists( aPath ):
            return None

        f = open( aPath, 'r')
        if f:

            if as_list:
                content = f.readlines()
            else:
                content = f.read()    
            
            f.close()
            return content

    except UnicodeDecodeError as err:

        return None

    except:
        return None

def file_rm ( aPath ):
    if file_exists( aPath ):
        os.remove( aPath )

def file_cp ( aSrc, aDest ):
    if file_exists( aSrc ):
        shutil.copyfile(aSrc, aDest)

def file_write( aPath, aContent, isAppend=False ): 

    try:

        f = None

        if file_exists( aPath ):
            if isAppend:    
                f = open( aPath, 'a+')
            else:
                f = open( aPath, 'w+')    
        else:
            f = open( aPath, 'w+')

        if not f:
            return False

        f.seek(0) 
        f.write( aContent )
        f.truncate()
        f.close()

        return True

    except IOError:
        return False

    except:
        return False

def list_files(dir_to_scan, ext='html'):

    matches = []

    for root, dirnames, filenames in os.walk( dir_to_scan ):
        for filename in fnmatch.filter(filenames, '*.'+ ext):

            item = os.path.join(root, filename)

            #print ' **** type(item) = ' + str( type ( item ) )
            matches.append( item )

    return matches

def list_sqlite( aPath ):

    return list_files( aPath, 'sqlite3' )

def get_tail( aPath ):
    head, tail = os.path.split( aPath )
    return tail

def get_date(aFormat='%H_%M_%S'):
    return time.strftime( aFormat, time.gmtime())

# Credits:
# https://stackoverflow.com/questions/16571150/how-to-capture-stdout-output-from-a-python-function-call
class Capturing(list):
    def __enter__(self):
        self._stdout = sys.stdout
        sys.stdout = self._stringio = StringIO()
        return self
    def __exit__(self, *args):
        self.extend(self._stringio.getvalue().splitlines())
        del self._stringio    # free up some memory
        sys.stdout = self._stdout
