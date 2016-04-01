# Changelog
*Please note*: this log has only been updated since version 0.7.0, as this was effectively the first 'working' release.
This log is **only** for major features in each update.  I will not be listing every single character I change here, considering GitHub can do that for me.

### 0.7.8
 - Removed all `from import *` in `Phantom.core`
 - Fix mystery `int('m')` bug in `epd_read.py`
 - Code in `Phantom.core` updated according to PEP8 (mostly)
 - Update `Simple.exe` and `Phantom_installer.exe`
 - Add automatic `exc_catch` deactivation if debug level is above a set number

### 0.7.7
 - Removed `from scene import *` in all `gui_pythonista` files, not just `scene_main`
 - Added the `promote()` method to the `ChessGame` class rather than just the board
 - Using the GUI's promoter screen no longer crashes, just doesn't actually promote the pawn
 - Added promote and castle commands to `Run_this.py` and `Simple.exe`
 - Bug fixed: the `Simple.exe` crashed on boot due to trying to find a nonexistant file
 - Bug noticed: `Phantom.core.pieces.ChessPiece.path_to` sometimes doesn't work correctly (only noticed with diagonal movement so far)
 - Bug noticed: En passant doesn't kill the right piece, if it kills any piece at all
 - Bug fixed: `Board.fen_str()` method no longer gives "Side('black')" but rather the correct "b"

### 0.7.6
 - Actually added the pawn promotion mechanism this time (oops)
 - Bug noticed: the `Phantom.core.pieces.ChessPiece.path_to()` method; it seems to give paths that are longer than they should be
 - Added call tracing to several functions

### 0.7.5
 - Bug fixed: Pieces could take their own color (this actually was fixed in v0.7.4 but I forgot to put it in the log)
 - Bug noticed & fixed (I think): Pawns could take pieces that were directly infront of them
 - Added experimental promotion mechanism to the Pythonista GUI
 - Added piece information command to the almost-shell
 - Bug noticed: Sometimes (only sometimes) the `Phantom.core.board.Board.fen_str()` method generates FEN strings incorrectly (for example, puts "Side('black')" instead of "b")

### 0.7.4
 - Bug noticed & fixed: Pythonista GUI didn't allow moving kings to any of the points that would normally be castling positions
 - AI easy works! YAY! (It's not particularly smart though...its very first move killed it's own king...)
 - Added some contributor info to `__version__.py`
 - Fixed `NameError` in `Phantom.utils.debug.clear_log()`
 - Fixed (I think) the `Phantom.core.game_class.ChessGame.is_won()` method
 - Added a much more user-friendly and functional almost-shell to the Run_this.py and Simple.exe (the only things they don't yet support are castling & promotion - planned for later versions)

### 0.7.3
 - Altered default settings to work better on computer
 - Much improved `Simple.exe` 
 - Fixed bug in which the game always thought the current player had won
 - Improved checkmate detection
 - Attempted to fix the AI tree generation (and probably failed)

### 0.7.2
 - Added experimental `Timer` class (doesn't work properly yet)
 - Made the "Force Moves" option actually do stuff (completely disables move validation)
 - Installer also now functions as an updater
 - Installer will add Phantom to the user's site-packages folder
 - Fixed bug in which a capture didn't switch turn
 - Added option (Pythonista only) to copy FEN to clipboard
 - Added experimental checkmate detection (***very*** experimental)
 - New bug: the game thinks the player whose turn it is has won the game

### 0.7.1
 - Added castling ability to GUI
 - Added (*very* experimental) options screen
 - Functional `subvalidcache` cache mechanism - each piece gets a list of coords approved by its `apply_ruleset()` method to speed up operations like `valid()`
 - New bug: caches don't load properly on game creation (don't let the lack of green squares on the GUI fool you - you can still move)

### 0.7.0
 - Added functional GUI to Pythonista
 - Pawn promotion
 - Much improved file IO
 - Package-wide base class
 - integer_args() decorator - convert all float arguments such as 1.0, 2.0 to 1, 2 but **NOT** 1.5 or 2.5
 - Fix issue in Phantom.core.coord.point.Coord.as_chess() method where chess coordinates were given starting at 0 rather than 1
 - Fix issue where pawns would just...kind of...disappear randomly
 - New bug: pawns that can capture en passant can go just about anywhere
 - New bug: after a piece is killed, it does not become the other player's turn