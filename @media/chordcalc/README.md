chordcalc
=========

https://github.com/polymerchm/chordcalc

Turning  Gek S. Low's chordcalc python script into a full-featured chord calculator/player 
Updated to be a full featured stringed instrument chord analysis tool by Steven K Pollack

*This is a major update and probably the last one for a while*


- **makeWaves.py**

generates a set of 96 2 second wave files  used by chordcalc.py to play the sound of the notes.

- **chordcalc.py**

- **chordcalc_constants.py**

- **debugStream.py**

There are three modes of operation: Calc, Identify and Scale.  These are selected by the C, I and S buttons

*Calc Mode:*

Select an instrument/tuning, a root (key), and a chord type, and all possible fingerings will be displayed on the fretboard.
You cycle through them with the up and down arrows.  By choosing various filters (lower right-hand corner list), you can  reduce the number and type of chords displayed. For example, 'LOW_3' is a mandolin filter that only presents chords played on the lower 3 strings and leaves the high E string unplayed.  The 'DOUBLE_STOP' filter (also for mandolin) will show all valid double stops for a given chord (2 note chord partials). 'NO_DEAD' will only show chords where every string is sounded.  

If a given instrument/tuning cannot represent the chord an appropriate offensive noise is sounded and message is displayed.  
The filters NO_ROOT, NO_3RD and NO_5TH will find chord shapes for 
mandolin (you notice the mandolin emphasis here) that allows those chord tones not to be 
ignored in testing for valid fingerings.  On mandolins, and other 4 stringed instrumetns, the player often abandons the root, 5th or 3rd.

Hitting the chord button will play the chord (see makeWaves.py above).  Hitting the arpeggio button will play the notes one by one. Hitting the button which describes the individual string tunings will play the sound of the instrument when un-fretted.

The slider at the bottom is a volume control and the slider at the top determines the "speed" of the arpeggio.

For any chord, touching the fretboard will display all of the chordtones on the entire fretboard.  Touching it again displays the current chord.

The chord tones and notes are displayed in the upper right 

*Identify mode*

In identify mode, you touch the fingerboard to indicate a fingering  When you hit Find, all possible "names" for the chord are given.  If the fingering is a chord partial, then the missing chord tones are indicated.  

*Scale Mode*

In scale mode, you select a key (the root) and the scale type.  All notes on the scale across the entire fretboard are displayed.  If you touch a root position, a two octave display is highlighted.  Hitting the scale button plays the scale.  The speed/volume sliders are also effective here.  If the mode is one of the greek modes, then the base key is displayed in the upper right hand corner (for example, A ionian is based on A, A Dorian is actually the key of G). Every effort is made to have the appropriate anharmonics (sharps or flats) display based on the most the key signature (or its base).  You can toggle the display between scale notes and scale degrees and for "ambiguous" key signatures (A#/Bb) you can toggle anharmonic notes between sharps and flats.  




You can add new instruments/tunings in the chordcalc_constants.py file.  You can also rearrange the order in which chords are presented by changing things here.  Note that if you make a change to this fiule, you must restart pythonista to have the changes show up.

- **debugStream.py** 

is a handy class for creating output that doesn't bog down the pythonista console which can slow debugging down.  

Usage:

```
out = debugStream()

out.push("this {} is formated to here {}",'string1','string2')
.
.
.
.
out.send()
```

first parameter is the format string that would be used with the `.format` method.  Any number of arguments that correspond to fields in the format string can follow.



Have fun