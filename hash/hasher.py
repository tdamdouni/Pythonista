# https://gist.github.com/kultprok/a77ca138b042cc8632b7

# -*- coding: utf-8 -*-

import argparse
import clipboard
import hashlib
from sys import argv
import webbrowser

def hash_data(hashstring, hashfunction, url):
    '''Get the hash of given string.'''
    # Determine if a method for hashfunction
    # exists in hashlib. If no attribute/method is
    # found, default to sha1.   
    if hasattr(hashlib, hashfunction):
      hash_method = getattr(hashlib, hashfunction)
    else:
    	hash_method = hashlib.sha1
        
    # Put hash to clipboard, if hashstring exists.
    if hashstring:
    	clipboard.set(hash_method(hashstring).hexdigest())
    else:
        raise ValueError

    # Pythonista doesn't support x-callback.
    # So this is a pragmatic approach to calling
    # another app after hashing the string.
    webbrowser.open(url)

def parse_input(data):
    '''Parse input from Drafts command-line-like.'''
    parser = argparse.ArgumentParser(description='input a string to hash.')

    # Expects strings to hash.
    parser.add_argument('inputstring',
                        metavar='STRING',
                        nargs='*',
                        help='the string to hash')
                        
    # Set the hash function.
    parser.add_argument('-hs', '--hs', '-hash', '--hash',
                        metavar='HASH-NAME',
                        default='sha1',
                        dest='hash',
                        help='the hash function of hashlib to use. defaults to sha1')

    # Intended to set a callback-like action.
    # Use to open a specific app via url scheme, if necessary. Otherwise will open Drafts.
    parser.add_argument('-u', '--u', '-uri', '--uri',
                        metavar='URL',
                        default='drafts://',
                        dest='url',
                        help='url scheme to call after hashing. use to call an app.')

    args = parser.parse_args(data)
    hash_data(' '.join(args.inputstring), args.hash, args.url)

if __name__ == '__main__':
    parse_input(argv[1].split(' '))
