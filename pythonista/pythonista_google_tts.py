# -*- coding: utf-8 -*-
""" ios clipboard to google TTS (in Spanish)
  This was written for ios pythonista, a python 2.x language.  It takes whatever is in the clipboard
and reads it out using google text-to-speech.  The present form takes Spanish and reads it aloud as my
interest is in learning to understand spoken Spanish.  I take text from the immersion part of
Duolingo and listen.  It should be quite easy to modify for different purposes.

  On a jail-broken device one can even: copy to clipboard, use activator to launch the pythonista script, and
have it start speaking!  I simple gathered some python from the web, fit it together, debugged a bit, and I
had a new tool.  Pythonista blew my mind.
"""

""" After each line, it gives options to quit, read all lines without pause, read next line, or
for you to write your translation.  It's still rough around the edges (and deletes everything in the
'temporary' sub-directory without confirmation), but I thought I would share it in case
others can build on it.

stophlong at gmail.com 2014 Feb 02 """
from __future__ import print_function

import urllib2
import sound
import time
import os
import clipboard


def parseText(text):
 """ returns a list of phrases each with less than 100 caracters for use with google translate tts engine.
 based on http://glowingpython.blogspot.com/2012/11/text-to-speech-with-correct-intonation.html """

 toSay = []
 punct = [',',':',';','.','?','!'] # punctuation
 words = text.split(' ')
 phrase = ''
 for w in words:
  if len(w)>0 and w[len(w)-1] in punct: # encountered a punctuation mark
   if (len(phrase)+len(w)+1 < 100): # is there enough space?
    phrase += ' '+w # add the word
    toSay.append(phrase.strip()) # save the phrase
   else:
    toSay.append(phrase.strip()) # save the phrase
    toSay.append(w.strip()) # save the word as a phrase
   phrase = '' # start another phrase
  elif len(w) > 0:
   if (len(phrase)+len(w)+1 < 100):
    phrase += ' '+w # add the word
   else:
    toSay.append(phrase.strip()) # save the phrase
    phrase = w # start a new phrase
 if len(phrase) > 0:
  toSay.append(phrase.strip())
 return toSay

def SayIt(folderPath,toSay,language='en'):
 google_translate_url = 'http://translate.google.com/translate_tts'
 opener = urllib2.build_opener()
 opener.addheaders = [('User-agent', 'Mozilla/4.0 (compatible; MSIE 6.0; Windows NT 5.0)')]
 next_step=''
 phrase_out = list()
 print('q = quit. a = all without pause. or write translation. return = next.')
 for i,phrase in enumerate(toSay):
  #print i,len(phrase), phrase
  print(phrase)

  tts_string = urllib2.quote(urllib2.unquote(phrase.encode('utf-8')))
  response = opener.open(google_translate_url+'?q='+tts_string+'&tl=' + language)
  #see
  #https://gist.github.com/adc2874aa09640237f6f
  #use timestamps so all files are uniquely named which forces pythonista to load the new material correctly.
  timestamp=time.time()
  filename = folderPath + str(i)+'speech_google' + str(timestamp) + '.mp3'
  ofp = open(filename,'wb')
  ofp.write(response.read())
  ofp.close()

  # command to repeat thing?
  sound.play_effect(filename)

  if next_step!='a' and next_step!='A':
			next_step = raw_input('(q,a,ret):')
			if next_step == 'q' or next_step == 'Q':
				return phrase_out
			if next_step!='a' and next_step!='A':
				phrase_out.append(next_step)
  else:
			time.sleep(.08*len(phrase))
			
  # allow pauses or perhaps prompt to continue or go until end or quit
  # using length of mp3 would be better pause
  # for translation could let person enter phrase and save it

 return phrase_out
if __name__ == '__main__':
 # set up and clean up
 folderPath="temporary/" #must be temporary files. everything will be deleted in directory
 if not os.path.exists(folderPath[:-1]):
  os.mkdir(folderPath[:-1])
 for item in os.listdir(folderPath):
  os.remove(folderPath + item)

 language='es' #pick language en english,es spanish

 #text = 'Think of color, pitch, loudness, heaviness, and hotness.  Each is the topic of a branch of physics'

 text = clipboard.get()
 toSay = parseText(text)
 phrase_out = SayIt(folderPath,toSay,language)
 print(toSay)
 print(phrase_out)
'''El mundo. Geografía.  La historia de Canción de Hielo y Fuego tiene lugar principalmente en el continente de Poniente.  Es aproximadamente equivalente en extensión a Sudamérica, aunque el autor quiso recrear una especie de Inglaterra medieval.  Sin embargo, hay una gran extensión de tierra al norte sin cartografiar, debido a las temperaturas extremadamente bajas y los habitantes hostiles conocidos como salvajes.   Las tierras del norte de Poniente están menos habitadas que las del sur a pesar de su extensión aproximadamente igual.   Las cinco ciudades principales de Poniente son, en orden de tamaño: Desembarco del Rey, Antigua, Lannisport, Puerto Gaviota, y Puerto Blanco.'''

