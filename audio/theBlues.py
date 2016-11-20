# Play a blues melody on Pythonista on the iPad (iOS)
import sound
import time

def playNotes(inNotes, inWithEmphisis=False):
	for note in inNotes:
	  sound.play_effect('Piano_' + note)
	  if (inWithEmphisis):
	  	time.sleep(0.25)
	  	sound.play_effect('Piano_' + note)
	  	time.sleep(0.25)
	  else:
	    time.sleep(0.5)

cnotes = ['C3', 'E3', 'G3', 'A3', 'C4', 'A3', 'G3', 'E3']
fnotes = ['F3', 'A3', 'C4', 'D4', 'F4', 'D4', 'C4', 'A3']
gnotes = ['G3', 'B3', 'D4', 'E4', 'F3', 'A3', 'C4', 'D4']
xnotes = ['C3', 'E3', 'F3', 'F3#', 'G3', 'A3#', 'G3', 'G3']

for i in range(2):
  playNotes(cnotes)
  cnotes[4] = 'A3#'
  playNotes(cnotes)
  playNotes(fnotes)
  cnotes[4] = 'C4'
  playNotes(cnotes)
  playNotes(gnotes)
  playNotes(cnotes, True)
