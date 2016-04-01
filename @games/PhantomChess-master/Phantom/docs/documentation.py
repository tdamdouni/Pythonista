# -*- coding: utf-8 -*-
from __future__ import (absolute_import, division, print_function, unicode_literals)

#########################################################################
# This file is part of PhantomChess.                                    #
#                                                                       #
# PhantomChess is free software: you can redistribute it and/or modify  #
# it under the terms of the GNU General Public License as published by  #
# the Free Software Foundation, either version 3 of the License, or     #
# (at your option) any later version.                                   #
#                                                                       #
# PhantomChess is distributed in the hope that it will be useful,       #
# but WITHOUT ANY WARRANTY; without even the implied warranty of        #
# MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the         #
# GNU General Public License for more details.                          #
#                                                                       #
# You should have received a copy of the GNU General Public License     #
# along with PhantomChess.  If not, see <http://www.gnu.org/licenses/>. #
#########################################################################

# R0 20150215T2048
def top():
    pass
#                                                   CHESS
###################################################################################################################

# In this documentation, I'll be using functions that return strings.  These allow the documentation to be import-
# able from anywhere and read from anywhere.  I find it quite useful personally.

def move_logic(): return """
            HOW THE PROGRAM DETERMINES MOVE VALIDITY
––––––––––––––––––––––––––––––––––––––––––––––––––––
 The program determines whether or not a move is valid by applying the following
 steps, in order.  They are grouped into several levels in a logical order.

 +-Level 0
 | +- 0.0: select piece to move from board
 | +- 0.1: alert board for scheduled move
 | |       freeze board layout & other player
 +-Level 1
 | +- 1.0: determine if piece's color is correct
 | |       for the current turn_color
 | +- 1.1: test the move in the piece's ruleset
 | +- 1.2: test if the target is valid
 | +- 1.3: test if there are pieces "in the way"
 | |       of the move
 | +- 1.4: checkmate test
 +-Level 2
 | +- 2.0: freeze piece
 | +- 2.1: kill piece at target
 | +- 2.2: move piece
 | +- 2.3: unfreeze piece
 | |       alert board move is complete
 | |       unfreeze board & other player
"""

def class_interface(): return """
        HOW LOW-LEVEL CLASSES ACCESS DATA IN HIGHER LEVELS
––––––––––––––––––––––––––––––––––––––––––––––––––––––––––
 A problem arises in level 1.2 of the move validation.  This problem is because
 level 1.2 checks the color of the piece at a target.  However, since the pieces are
 held in sets in an instance of the Phantom.core.board.Board class, the individual
 pieces do not have access to the list they are contained in.  This means the piece
 cannot get the piece at it's target and therefore cannot check it's color.

 The solution to this is to store the board instance as an attribute of the piece.

 An example:
 ```
 class low_level (object):
     def __init__(self, y):
         self.y = y

 class mid_level (object):
     def __init__(self, a):
         self.a = low_level(a)

 class top_level (object):
     def __init__(self, x):
         self.x = mid_level(x)
 ```
 Now say the low_level class needs to access the top_level's x attr.  This can be done by:
 ```
 class low_level (object):
     def __init__(self, y):
         self.y = y
     def set_owner(self, o):
         self.owner = o

 class mid_level (object):
     def __init__(self, a):
         self.a = low_level(a)
         self.a.set_owner(self)
     def set_owner(self, o):
         self.owner = o

 class top_level (object):
     def __init__(self, x):
         self.x = mid_level(x)
         self.x.set_owner(self)
         self.z = 5
 ```
 Now, the class low_level can access the top_level by:
 self.owner.owner.z

 However, using this method, one must be careful not to cause indirect recursion errors by doing the following:
 `self.owner.a.owner.a.owner.`···
 as a is the low_level itself.
"""

# FIXME To be continued...

def location_in_phantom(): return """
                 HOW DOES LOCATION WORK IN PHANTOM
––––––––––––––––––––––––––––––––––––––––––––––
 The chess board is set up in columns from 'a' to 'h' and rows from '8' to '1'.
 These are combined into a board location called a "fen_loc" e.g. a8, h1, etc.
 Every chess piece and board tile has a fen_loc variable and the following properties:
     row -- possible top to bottom values '8', '7', '6', '5', '3', '3', '2', '1'
     col -- possible left to right values 'a', 'b', 'c', 'd', 'e', 'f', 'g', 'h'
       x -- possible left to right values 0 thru 7
       y -- possible top to bottom values 0 thru 7
 
 Cheat sheet of mappings of fen_locs (e.g. d4)
 to x, y coordinates (e.g. (3,4)).

     a    b    c    d    e    f    g    h
    ======================================
 8  0,0  1,0  2,0  3,0  4,0  5,0  6,0  7,0  8
 7  0,1  1,1  2,1  3,1  4,1  5,1  6,1  7,1  7
 6  0,2  1,2  2,2  3,2  4,2  5,2  6,2  7,2  6
 5  0,3  1,3  2,3  3,3  4,3  5,3  6,3  7,3  5
 4  0,4  1,4  2,4  3,4  4,4  5,4  6,4  7,4  4
 3  0,5  1,5  2,5  3,5  4,5  5,5  6,5  7,5  3
 2  0,6  1,6  2,6  3,6  4,6  5,6  6,6  7,6  2
 1  0,7  1,7  2,7  3,7  4,7  5,7  6,7  7,7  1
    ======================================
     a    b    c    d    e    f    g    h

 Note that a8 is (0,0) while h1 is (7,7) which
 is unintuitive and caused difficult to spot
 location bugs in earlier versions of Phantom.

 Now Phantom objects Tile and Piece have
 attributes .row, .col, .x and .y to
 facilitate the interchangable use of both
 col,row-based fen_locs and x, y coordinates. 
 """

# FIXME Is eval() still used?  Eval() is also a security nightmare which is another reason to avoid it.

def use_of_eval(): return """
                 WHEN/WHERE/WHY IS EVAL() USED
––––––––––––––––––––––––––––––––––––––––––––––
 As a more experienced programmer will know, using the eval() function or the exec statement
 makes things slow.  If they're used often enough in a program, they make it REALLY slow.
 As such I have attempted to avoid using these.  There are 2 occasions of use so far:

 eval(): Phantom.core.pieces.ChessPiece.__init__
         eval() is used to determine display character name from the Phantom.constants file
  exact use: `self.disp_char = eval('d_{}_{}'.format(self.color, self.ptype))`

 eval(): Phantom.core.pieces.ChessPiece.__init__
         eval() is used to determine FEN notation character name from the Phantom.constants file
  exact use: `self.fen_char = eval('c_{}_{}'.format(self.color, self.ptype))`

 Both of these are only called once at piece instantiation time when the board is generated.  Because of
 this they will be used no more than 32 times per game generation.
"""

def import_cleanness(): return """
            WHAT IS A CLEAN IMPORT AND WHY IS IT IMPORTANT
––––––––––––––––––––––––––––––––––––––––––––––––––––––––––
 A clean import is a module within a package that doesn't import anything from the package.
 It may import standard library modules, such as `os` or `sys`, but with Phantom as an example
 it cannot import anything that would begin with `Phantom.` (such as `Phantom.core.board`).

 Sometimes you may see a file saying it is a 1-level clean import -- what I meant by saying this
 is that the file only imports clean-import files.

 Why is it important?
 While writing this package, I constantly got ImportErrors that looked similar to this:

    Traceback (most recent call last):
      File "<string>", line 1, in <module>
      File "game_class.py", line 5, in <module>
        from Phantom.core.board import Board, Tile, load
      File "/var/.../Phantom/core/board.py", line 12, in <module>
        from Phantom.boardio.load import loadgame, listgames
      File "/var/.../Phantom/boardio/load.py", line 6, in <module>
        from Phantom.core.board import Board
    ImportError: cannot import name Board

 As you can see from this traceback, in the Phantom.core.game_class file I import Board from Phantom.core.board.
 In Phantom.core.board, I import Phantom.boardio.load.
 In Phantom.boardio.load, I import Phantom.core.board.
 In Phantom.core.board, I import Phantom.boardio.load.
 And the loop of imports never ends.

 This is why clean imports are important -- importing something that isn't clean can often lead to errors.
 """

def links(): return """
                    USEFUL ONLINE READING
–––––––––––––––––––––––––––––––––––––––––

 A good list of links for reading that I'm not going to bother typing out again:
 http://stackoverflow.com/questons/494721/what-are-some-good-resources-for-writing-a-chess-engine/502029#502029

 An article that includes a bit of the history of computer chess as well:
 http://arstechnia.com/gaming/2011/08/force-fersus-heuristics-the-contentious-rise-of-computer-chess/

 The oblicatory Wikipedia link:
 http://en.wikipedia.org/wiki/Computer_chess

 How to read/write FEN strings
 http://en.wikipedia.org/wiki/Forsyth-Edwards_Notation

 A good article on algebraic chess notation
 http://chesshouse.com/how_to_read_and_write_chess_notation_a/166.htm
"""

# FIXME Is freeze still useful?

def why_freeze(): return '''
            WHY FREEZE THE BOARD?
–––––––––––––––––––––––––––––––––
 The Phantom.core.board.Board.freeze method is exactly as follows:

        ```
        def freeze(self):
            """Lock the board in place."""
            self.isFrozen = True
            self.pieces = list(self.pieces)
        ```

 The most important thing that happens is the `self.pieces = list(self.pieces)`.
 The reason:
     For the Phantom.ai.basic.mover.make_random_move function to work, it needs to select a random
     element from the board's pieces.  From the `random` module sourcecode, the choice method does this:

         `return seq[int(self.random() * len(seq))]`

    Since the `set` type does not support indexing, `choice` cannot be used.  Therefore we must convert
    the set of pieces to a list before the AI can make a choice.
'''

def program_use(): return """
                    HOW DO I USE PHANTOM?
–––––––––––––––––––––––––––––––––––––––––
 That depends what you're trying to do.

 To simply play chess against another human, you can do this:
     ```
     >>> from Phantom.core.game_class import PhantomGame
     >>> g = ChessGame()
     >>> g
          New Game 1
     –––––––––––––––––––
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

     >>> g.move('e2e4')  # accepts moves in algebraic chess notation
     >>> g

          New Game 1
     –––––––––––––––––––
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
 and you can continue to play from here.
 If you wish to load a previously saved game:
     ```
     >>> from Phantom.core.game_class import PhantomGame
     >>> g = ChessGame('Game 1')  # load one of the default games
     >>> g=
            Game 1
     –––––––––––––––––––
       a b c d e f g h
     8 r n   q   b n r 8 <
     7 .   . b p k p p 7
     6 p p p .   .   . 6
     5 .   . p . p .   5
     4   .   P P B P . 4
     3 .   N   .   . N 3
     2 P P P . Q P   P 2
     1 .   K R . B . R 1
       a b c d e f g h
     ```
"""

def bottom():
    pass
