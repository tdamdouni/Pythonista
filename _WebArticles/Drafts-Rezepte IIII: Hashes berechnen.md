# Drafts-Rezepte IIII: Hashes berechnen

_Captured: 2015-09-28 at 23:17 from [kulturproktologie.de](http://kulturproktologie.de/?p=4639)_

Dann geht es frohlich in der Reihe kleiner Skripte fur _Drafts_ und _Pythonista_ weiter. Da ich hin und wieder mal Hashes als Prufsummen benotige, hatte ich immer eigene Apps dafur auf dem iPhone. Da diese allerdings fur ihren eigentlichen Zweck zu groß waren - sie waren allesamt auch noch hasslich -, habe ich sie nun durch folgendes Skript ersetzt. Das lauft bei mir ganz ordentlich.

Hierzu brauche ich wieder einen Action in _Drafts_, die in diesem Fall auf das Skript _hasher_in _Pythonista_ zugreifen soll. Das sieht so aus:

[Import-Link](drafts://x-callback-url/import_action?type=URL&name=Hasher&url=pythonista%3A%2F%2Fhasher%3Faction%3Drun%26argv%3D%5B%5Bdraft%5D%5D)

Etwas umfangreicher, daher auch erklarungsbedurftiger ist das Skript in Python. Dieses habe ich mal im Grunde angelegt, dass es wie ein Programm fur die Shell genutzt werden kann.

```
# @Drafts
# http://kulturproktologie.de/?p=4639
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
    
```

Ich muss also etwas erklaren, was das Skript macht. Es kann drei Sorten von Input verarbeiten:

> -hs (-hs, -hash, -hash) HASH_BEZEICHNUNG: Dieser Befehl ist optional und gibt die zu verwendenden Hashfunktion* an. Ist die Bezeichnung unbekannt oder falsch, wird der Standardwert 'sha1′ angenommen.
> 
> -u (-u, -url, -url) URL_SCHEMA: Dieser Befehl ist optional und gibt das URL-Schema einer aufzurufenden Anwendung an. Standardmaßig ist ‚drafts://' vorgegeben.
> 
> inputstring *STRING: Alle ubrigen Übergabewerte werden zum Inputstring hinzugefugt, der gehasht wird.

Es lasst sich doch besser mit einigen Beispielen erklaren. Nehmen wir mal folgenden Eingaben in _Drafts _an, wobei jede Zeile einer Eingabe entspricht:

> Test
> 
> Test -s md5
> 
> Test -u tweetbot://
> 
> Test und noch mehr Test -s sha512

Die erste Eingabe wurde den SHA1-Hash von ‚Test' berechnen, die zweite wurde denselben String als MD5-Hash berechnen. Beide Eingaben fuhren dazu, dass nach der Berechnung in _Pythonista_ wieder _Drafts_ aufgerufen wird. Die dritte Eingabe berechnet den Standard, also SHA1, von ‚Test, kehrt aber nicht nach _Drafts_ zuruck, sondern offnet _Tweetbot_ (sofern es installiert wurde). Die letzte Eingabe nimmt ‚Test und noch mehr Test' und berechnet den SHA512-Hashwert fur die Zeichenfolge.

* Laut der [Dokumentation fur Python 2.7](http://docs.python.org/2/library/hashlib.html), das von _Pythonista_ genutzt wird, werden folgende Hashfunktionen unterstutzt:

> This module implements a common interface to many different secure hash and message digest algorithms. Included are the FIPS secure hash algorithms SHA1, SHA224, SHA256, SHA384, and SHA512 (defined in FIPS 180-2) as well as RSA's MD5 algorithm (defined in Internet RFC 1321).
