
This is the basic framework for a text-adventure style game which can be used on the iPad app [Pythonista](http://omz-software.com/pythonista/).

It only uses modules from the standard library so it requires no special setup and should Just Work. Since that is the case, it will also work on any system that has python installed.  [This may change if I add any functionality specific to Pythonista.]

Based on a talk at PyOhio by [Jeff Armstrong](https://github.com/ArmstrongJ). Videos of this presentation can be found <http://pyvideo.org/video/2270/a-text-adventure-in-python>

Source code at: <https://github.com/ArmstrongJ/pyohio2013>

## TODO:

* Add objects to examine, pick up and use. 
* Add the ability to combine objects into larger "tools" to solve puzzles.
* Add NPCs and be able to interact with them.

## Rooms:

The rooms contain a json object which will be saved to the sqlite database.

Note that the file extension is intentionally json.py because Pythonista only recognizes .py files and will not display them otherwise.
