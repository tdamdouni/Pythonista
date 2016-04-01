<IMG SRC="https://raw.githubusercontent.com/marcus67/rechtschreibung/master/lib/rechtschreibung_64.png">
#  rechtschreibung
A little Python app to be used with Pythonista to test different rule sets for German spelling.

## Requirements

You need to have [Pythonista](https://itunes.apple.com/us/app/pythonista/id528579881?mt=8) installed on iOS.

## Basic Functionality

This project allows you to test different combinations of German spelling rules with a simple GUI. Each change of rules is immediately reflected in a text especially written for this purpose. The GUI can be used to store favorite combinations and compare them.

<CENTER>
<IMG SRC="https://raw.githubusercontent.com/marcus67/rechtschreibung/master/doc/main_screen.png" WIDTH="800px">
</CENTER>

## Installation

The source code is available as a self-extracting Python script. See file `build/rechtschreibung_zip.py`. Download this file and follow the instructions contained therein.

## Usage

### Main View

The main view is shown upon start of the application. It looks different for small devices (iPhone) and large devices (iPad). We'll concentrate on the version for larger devices first.

<CENTER>
<IMG SRC="https://raw.githubusercontent.com/marcus67/rechtschreibung/master/doc/main_screen.png" WIDTH="800px">
</CENTER>

On the left an especially designed text (see screenshot above) is displayed. It serves two purposes. The first purpose is to explain the motivation behind the app and introduce to fictional characters (Casimir and Wendy) representing the two opposing positions in the discussion about German spelling: Casimir is the conservative person trying to main the status quo and Wendy is the progressive person trying to change rules to make them easier and more consistent.

The second purpose is to display the impact of the various rules on a concrete text, which is to say that every time the user changes one of the rules the changes in the text are immediately reflected. For a short period of time the actual changes are highlighted: letters which are to be deleted are shown with grey background and striked out. Letters which are to be inserted are shown with green background. (see screenshot below) Usually (unless deactivated) the highlighted sections are removed after a certain delay (e.g. 5 seconds). 

<CENTER>
<IMG SRC="https://raw.githubusercontent.com/marcus67/rechtschreibung/master/doc/highlighted_rule_change.png" WIDTH="480px">
</CENTER>


Since some of the rules have very little impact on a standard text, it has been seen to it that in the conversation between 
Casimir and Wendy there are especially designed sample sentences showing the differences.

#### Rule Sets

The spelling rules are organized in currently six sections (see upper right navigation area in screen shot above). Actually, the term "spelling" is a little wider than just the correct use of letters for words. The rule sets also contain aspects of punctuation ("Zeichensetzung") and layout.

##### App Control View

The App Control view in the lower right corner shows some setting influencing the behaviour of the app.

<CENTER>
<IMG SRC="https://raw.githubusercontent.com/marcus67/rechtschreibung/master/doc/control_view.png" WIDTH="320px">
</CENTER>

##### Highlighting of Changes
There are three modes for highlighting the changes after an applied rule change:

 * The highlighting is off ("aus").
 * The highlighting is done compared to the immediately previous rule set ("Delta").
 * The highlighting is done compared to the reference rule set ("Referenz"). The initial reference rule set is the currently valid spelling rule set as proposed by the book "Duden". It can be changed by loading other rule sets (see below).

The switch next to the clock icon enables the "auto off" mode for highlighting of changes. When set to "on" the highlighting will automatically disappear after a certain time delay. If set to "off" the highlighting will remain active indefinitely.

##### Speaking the Text
The play button will make the iDevice read the current text. This can be quite entertaining if the user has chosen a rule combination that the built-in pronunciation logic cannot handle. Of course, the pause button will make the playback stop.

##### Loading the Reference Rule Set

The icon next to the "Referenz" rule set will open a view to load a new reference rule set.

<CENTER>
<IMG SRC="https://raw.githubusercontent.com/marcus67/rechtschreibung/master/doc/load_configuration.png" WIDTH="320px">
</CENTER>

The user can a pick a rule set from the list by tapping on the list entry.

##### Loading the Working Rule Set ("Current")

The first icon next to the "Aktuell" rule set will open a view to load the working rule set which will be compared to the reference rule set.

<CENTER>
<IMG SRC="https://raw.githubusercontent.com/marcus67/rechtschreibung/master/doc/load_configuration.png" WIDTH="320px">
</CENTER>

The user can a pick a rule set from the list by tapping on the list entry. Tapping on the information icons on the right end of the list entries will show the comment that has been saved with the rule set.

##### Loading the Working Rule Set ("Current")

The second icon next to the "Aktuell" rule set will open a view to save the working rule set.

<CENTER>
<IMG SRC="https://raw.githubusercontent.com/marcus67/rechtschreibung/master/doc/save_configuration.png" WIDTH="320px">
</CENTER>

The user will have to choose a name (if not already present) and optionally a comment. Tapping on a list entry will fetch the name and the comment of the chosen rule set for overwriting. The button will show "Überschreiben" if a saved rule set with the given name exists or "Speichern" otherwise. Note: The labels of the button will be adapted to the current rule set! :-)

##### Statistics

NOT IMPLEMENTED YET.

Have fun!
