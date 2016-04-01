# Phantom
Phantom is a (in development) game of Chess written in Python 2.7.  It is a completely standalone package and at this time has no support for [Universal Chess Interface][UCI] (UCI), although it is something lurking at the back of my mind to implement.

On Windows currently the only form of Graphical User Interface (GUI) provided is pretty-printing, ex:
```
  a b c d e f g h   
8 r n b q k b n r 8 
7 p p p p p p p p 7 
6   .   .   .   . 6 
5 .   .   .   .   5 
4   .   .   .   . 4 
3 .   .   .   .   3 
2 P P P P P P P P 2 
1 R N B Q K B N R 1 < 
  a b c d e f g h   
```
If your system supports Unicode printing, then the output may look like this:
```
  a b c d e f g h
8 ♜ ♞ ♝ ♛ ♚ ♝ ♞ ♜ 8 
7 ♟ ♟ ♟ ♟ ♟ ♟ ♟ ♟ 7 
6 ◦ • ◦ • ◦ • ◦ • 6 
5 • ◦ • ◦ • ◦ • ◦ 5 
4 ◦ • ◦ • ◦ • ◦ • 4 
3 • ◦ • ◦ • ◦ • ◦ 3 
2 ♙ ♙ ♙ ♙ ♙ ♙ ♙ ♙ 2 
1 ♖ ♘ ♗ ♕ ♔ ♗ ♘ ♖ 1 ◀ 
  a b c d e f g h
```
A proper GUI is *almost* working for the iOS app [Pythonista][pythonista].

Please note: this project is a huge learning experience for me.  This is the 3rd revision (I've restarted from scratch twice) of my ongoing chess project, each one getting better.  Hopefully there is no 4th revision.  If you find a bug, **please** don't hesitate to let me know so I can fix it.

## Features

- [x] Human vs. human play
- [ ] Checkmate detection  (work-in-progress)
- [x] Static board analysis (always improving)
- [ ] Move search engine (work-in-progress)
- [ ] Descriptive game notation
- [x] Move validation
- [x] En passant
- [x] Pawn promotion
- [x] Pretty printing
- [x] Save/load boards
- [x] Read/write FEN strings
- [x] Read EPD strings
- [ ] Write EPD strings
- [x] Algebraic chess notation
- [ ] Pythonista GUI *see below
- [ ] Windows GUI
- [x] Self-test suite
- [ ] Timers

*The basics of a GUI exist and work, however, at this time pawn promotion does not work correctly.  Until this is fixed, the GUI is considered incomplete.

## Installation
To download & extract PhantomChess, the first thing to do is to copy the [`Phantom_installer.py`](https://github.com/671620616/PhantomChess/blob/master/Phantom_installer.py) file into a local directory and run it.  For Windows users, the same file is available as a `.exe`.  Both versions of Phantom_installer will also work to update the package once it has been installed.  Occasionally there may be an update to the installer, but all older versions should continue to work if for some reason you don't wish to update.

### Easy method on Windows
Although it is more error-prone and not quite as user friendly as I'd like, a single executable is available (`Simple.exe`).  All you have to do is download this.  You don't even have to have Python installed to run it! (built with [PyInstaller][pyinstall])  Please note, Simple.exe does not have the ability to save/load boards.

## Static board analysis
How exactly does Phantom analyze a board and give it a score?  It uses a set of heuristics coded into the Phantom.ai.pos_eval.heuristics file.  This is a list of the currently active heuristics that are used to analyze a board:

- developed pieces
- advanced pawns
- separate scoring method for kings based on opening, midgame, endgame
- does player have the bishop pair
- has the player castled
- analyze pawn structure (work-in-progress)
- assess pawns, knights, bishops, rooks, queens & kings according to the Phantom.ai.pos_eval.piece_tables file (which came from [here][piece_tables])
- assess bad bishops

as well as the much simpler material analysis.

### Why no mobility heuristic?
Briefly considering how chess works, one would assume a piece that could make more moves would be more valuable.  And that would be correct, although it wouldn't make the piece as valuable as you might think because most legal moves in any given chess game *are pointless*.  Also, the main reason the function isn't put to use (it does exist in the file) is that it simply takes too long to generate the list of valid moves.

### Score system
Scores are given in "centipawns", such that 100 cp = 1 pawn.  The values used are too many to list here, and can be found in the Phantom.ai.settings file.

# Usage
To create and play a new game, simply do this:

```python
$ Phantom/Run_this.py
     New Game
-------------------
  a b c d e f g h   
8 r n b q k b n r 8 
7 p p p p p p p p 7 
6   .   .   .   . 6 
5 .   .   .   .   5 
4   .   .   .   . 4 
3 .   .   .   .   3 
2 P P P P P P P P 2 
1 R N B Q K B N R 1 < 
  a b c d e f g h   

:> e2e4  # move the piece at e2 to e4
     New Game
-------------------
  a b c d e f g h   
8 r n b q k b n r 8 < 
7 p p p p p p p p 7 
6   .   .   .   . 6 
5 .   .   .   .   5 
4   .   . P .   . 4 
3 .   .   .   .   3 
2 P P P P   P P P 2 
1 R N B Q K B N R 1 
  a b c d e f g h
```

In the Pythonista app, it is possible to activate a GUI by running `Phantom/gui_pythonista/main_scene.py`.  This feature is planned for Windows, etc. as well, but will most likely require the [Pygame][pygame] package.

# Contributing
Are you a programmer?  Know Python?  Interested in Phantom?  Feel free to help! I've never actually been taught Python, just learned it from trial & error, so I'm sure there's plenty of things that could be done much better.
Not a programmer but still interested in chess? Good, I need help there too! (I stink at chess).  Mainly the evaluation function - I don't have a good idea of what makes a board good or bad.
If you have any ideas, ***please*** open an issue or make a pull request so I can make things better.

[pythonista]: http://omz-software.com/pythonista
[UCI]: http://en.wikipedia.org/wiki/Universal_Chess_Interface
[pyinstall]: https://github.com/pyinstaller/pyinstaller/wiki
[pygame]: http://pygame.org/news.html
[piece_tables]: https://chessprogramming.wikispaces.com/Simplified+evaluation+function
