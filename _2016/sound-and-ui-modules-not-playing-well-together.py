# https://forum.omz-software.com/topic/3739/sound-and-ui-modules-not-playing-well-together

@ui.in_background
def playProgression(button):
	if os.path.exists('waves'):
		if not model._InstrumentOctave:
			return
		else:
			baseOctave = model._InstrumentOctave
		strings = model._InstrumentTuning
		
		for chordNumber in range(len(model._ProgFingerings))
 # here is where I inserted code to trigger a redraw of a custom view.
  # the redraw happens when this loop finished
			thisFingering = model._ProgFingeringsPointers[chordNumber]
			cc = model._ProgFingerings[chordNumber][thisFingering]
			frets = cc[2]
			dead_notes = [item[3] == 'X' for item in cc[0]]
			tones = []
			for fret,string,dead_note in zip(frets,strings,dead_notes):
				if  dead_note:
					continue
				octave,tone = divmod(string + fret,12)
				tones.append((tone,octave+baseOctave))
			for tone,octave in tones:
				sound.play_effect(getWaveName(tone,octave))
				time.sleep(model.play_arpSpeed*0.25)
			time.sleep(3*model.play_arpSpeed) # rest between chords
# the "chords" play just fine as well as the final sleeps between chords.

# --------------------
import sound,ui
v=ui.View()
v.bg_color='red'
v.present()
p=sound.Player('piano:A3')
def g():
	v.bg_color='green'
	p.finished_handler=None
	p.play()
def f():
	v.bg_color='blue'
	p.finished_handler=g
	p.play()
	
p.finished_handler=f
p.play()
# --------------------

