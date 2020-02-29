# -*- coding: utf-8 -*-

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

"""The chessboard itself."""
from __future__ import print_function

from Phantom.constants import *
from Phantom.core.chessobj import PhantomObj
from Phantom.core.players import Player, Side
from Phantom.core.exceptions import InvalidDimension, InvalidMove, LogicError, ChessError
from Phantom.core.pieces import ChessPiece, King, Queen, Rook, Bishop, Knight, Pawn
from Phantom.core.coord.vectored_lists import north, south, east, west, ne, se, nw, sw
from Phantom.core.coord.point import Coord, Grid
from Phantom.boardio.save import save
from Phantom.boardio.load import loadgame, listgames
from Phantom.boardio.boardcfg import Cfg, Namespace
from Phantom.utils.debug import call_trace, log_msg
from Phantom.utils.decorators import exc_catch
from Phantom.functions import round_down, dist
import uuid

__all__ = []

def load(name):
    fen = loadgame(name)
    game = Board(Player('white'), Player('black'), fen)
    game.set_name(name)
    return game
__all__.append('load')

class Tile (PhantomObj):
    
    isfrozen = False
    
    def __init__(self, pos, color):
        self.x = pos.x
        self.y = pos.y
        self.color = Side(color)
        self.coord = pos
        if use_unicode:
            self.char = d_white_space if self.color == 'white' else d_black_space
        else:
            self.char = c_white_space if self.color == 'white' else c_black_space
__all__.append('Tile')


class Board (PhantomObj):
    
    isfrozen = False  # is the board frozen?
    movenum = 0       # how many moves have been made
    
    def __init__(self, p1=Player('white'), p2=Player('black'), fen=opening_fen, **cfgkws):
        
        self.player1 = p1
        self.player2 = p2
        self.player1.set_board(self)
        self.player2.set_board(self)
        self.pieces = set()
        self.dead = set()
        self.name = 'New Game'
        self.cfg = Cfg(**cfgkws)
        self.cfg.set_board(self)
        self.game = None
        self.lastmove = (None, None)
        self._uuid = uuid.uuid4()
        self.data = Namespace()
        self.start_pos = fen
        
        tile_color = 'black'
        op_color = lambda c: 'white' if c == 'black' else 'black'
        self.tiles = set()
        for x in range(grid_width):
            for y in range(grid_height):
                self.tiles.add(Tile(Coord(x, y), tile_color))
                tile_color = op_color(tile_color)
            tile_color = op_color(tile_color)
        
        # parse given FEN and create board layout
        fields = fen.split()
        if not len(fields) == 6:
            raise ChessError('Invalid FEN given to board', 'Phantom.core.board.Board.__init__')
        pieces = fields[0]
        moving_color = Side(fields[1])
        castling = fields[2]
        en_passant = fields[3]
        halfmove = int(fields[4])
        fullmove = int(fields[5])
        
        self.halfmove_clock = halfmove
        self.fullmove_clock = fullmove
        self.turn = moving_color
        self.castling_rights = castling
        self.en_passant_rights = en_passant
        
        # parse the FEN into a board layout
        rank_split = '/'
        is_rank_split = lambda char: char == rank_split
        is_file_split = lambda char: char in '12345678'
        is_white_chr = lambda char: char in 'RNBKQP'
        is_black_chr = lambda char: char in 'rnbkqp'
        is_piece_chr = lambda char: is_white_chr(char) or is_black_chr(char)
        
        ranks = pieces.split(rank_split)
        y_c = grid_height
        for rank in ranks:
            y_c -= 1
            if y_c < 0: break
            fileind = 0
            for char in rank:
                if is_piece_chr(char):
                    klass = ChessPiece.type_from_chr(char)
                    pos = Coord(fileind, y_c)
                    owner = self.player1 if is_white_chr(char) else self.player2
                    color = owner.color.color
                    newpiece = klass(pos, color, owner)
                    if newpiece.coord not in klass.default_origins:
                        newpiece.firstmove = False
                    self.pieces.add(newpiece)
                elif is_file_split(char):
                    fileind += int(char)
                    continue
                fileind += 1
    
    def __hash__(self):
        return int(self._uuid) % len(self.pieces) + self.fullmove_clock
    
    # implementation detail 0, 1
    def __getitem__(self, x):
        possible = []
        for piece in self.pieces:
            if piece.coord == x:
                possible.append(piece)
        # if there was only one item, return it otherwise a list of them all
        if len(possible) == 0:
            return None
        return possible[0] if len(possible) == 1 else possible
    
    def tile_at(self, pos):
        for tile in self.tiles:
            if tile.coord == pos:
                return tile
    
    def __contains__(self, elem):
        return elem in self.pieces
    
    #@call_trace(3)  # ccc: I am not sure what call_trace is needed here
    def get_piece_list(self, ptype=None, color=None):
        pieces = [p for p in self.pieces if p.ptype == ptype] if ptype else self.pieces
        return [p for p in pieces if p.color == color] if color else pieces 

    @call_trace(4)
    def fen_str(self):
        rank_split = '/'
        fen = ''
        for y in range(grid_height, -1, -1):
            file_gap = 0
            for x in range(grid_width):
                piece = self[Coord(x, y)]
                if (piece == []) or (piece is None):
                    file_gap += 1
                    continue
                else:
                    if file_gap > 0:
                        fen += str(file_gap)
                        file_gap = 0
                    fen += piece.fen_char
            if not y in (8, 0):
                if file_gap > 0:
                    fen += str(file_gap)
                fen += rank_split
        self.upd_rights()  # make sure the castling rights aren't ''
        fen += ' {turn} {castle} {ep} {half} {full}'.format(
                turn=self.turn.color[0], castle=self.castling_rights, ep=self.en_passant_rights,
                half=str(self.halfmove_clock), full=str(self.fullmove_clock))
        return fen

    def all_legal(self):
        ret = {}
        for piece in self.pieces:
            try:
                ret.update({piece: piece.valid()})
            except AttributeError as e:
                continue
        return ret
    
    def _pprnt(self):
        spaces_center = (18 - (len(self.name))) / 2
        dash = '–' if self.cfg.use_unicode else '-'
        s = '{}{}\n{}\n'.format(' '*spaces_center, self.name, dash*19)
        for y in range(grid_height, -2, -1):
            for x in range(-1, grid_width+1):
                if y in (-1, 8) and not (x in (-1, 8)):
                    char = Coord.tochesskeys[x+1]
                elif y in range(0, 8) and x in (-1, 8):
                    char = str(y+1)
                    if self.cfg.disp_turn:
                        if y == 0 and self.turn == 'white' and x == 8:
                            if self.cfg.use_unicode:
                                char += ' {}'.format(d_turn_indicator)
                            else:
                                char += ' {}'.format(c_turn_indicator)
                        elif y == 7 and self.turn == 'black' and x == 8:
                            if self.cfg.use_unicode:
                                char += ' {}'.format(d_turn_indicator)
                            else:
                                char += ' {}'.format(c_turn_indicator)
                elif x in (-1, 8):
                    char = ' '
                else:
                    piece = self[Coord(x, y)]
                    if (piece == []) or (piece is None):
                        if self.cfg.disp_sqrs:
                            char = self.tile_at(Coord(x, y)).char
                        else:
                            char = ' '
                    else:
                        char = piece.disp_char
                s += '{} '.format(char)
            s += '\n'
        return s
    
    def pprint(self):
        """Print a pretty version of the board."""
        if in_pythonista:
            import console
            console.set_font('DejaVuSansMono', 18)
            print(self._pprnt())
            console.set_font()
        else:
            print(self._pprnt())
    
    def __str__(self):
        return self.fen_str()
    
    def save(self, name):
        self.set_name(name)
        save(self)
    
    def set_name(self, name):
        self.name = name
    
    def set_game(self, g):
        self.game = g
        self.cfg.set_game(g)
    
    def freeze(self):
        """Lock the board in place."""
        self.isfrozen = True
        self.pieces = list(self.pieces)
        self.player1.freeze()
        self.player2.freeze()
    
    def unfreeze(self):
        """Unlock the board."""
        self.isfrozen = False
        self.pieces = set(self.pieces)
        self.player1.unfreeze()
        self.player2.unfreeze()
        
    def premove(self):
        """Freeze everything and send a signal to players that a move will be made."""
        self.freeze()
        self.player1.premove()
        self.player2.premove()
    
    def postmove(self):
        """Unfreeze and send a signal to players that a move has been completed."""
        self.unfreeze()
        self.player1.postmove()
        self.player2.postmove()
    
    def switch_turn(self):
        if self.turn == 'white':
            self.turn = Side('black')
            self.player1.timer.pause()
            self.player2.timer.resume()
        elif self.turn == 'black':
            self.turn = Side('white')
            self.player1.timer.resume()
            self.player2.timer.pause()
    
    def upd_rights(self):
        """This method soely exists so that if an exception occurs during a 
        method that should have reset either en passant rights or castling rights
        and wasnt able to because of the error.  This method will find any '' strings
        and correct them to '-'."""
        if self.castling_rights == '':
            self.castling_rights = '-'
        if self.en_passant_rights == '':
            self.en_passant_rigths = '-'
    
    @call_trace(2)
    @exc_catch(KeyError, ret='Could not kill specified piece', log=3)
    def kill(self, piece):
        if piece is None:
            return
        self.halfmove_clock = 0
        piece.owner.lose_piece(piece)
        self.dead.add(piece)
        self.pieces.remove(piece)
    
    @call_trace(1)
    @exc_catch(LogicError, ChessError, KeyError, ret='Cannot make specified move', log=4)
    def move(self, p, p2=None):
        if p2 is None:
            p1 = Coord.from_chess(p[0:2])
            p2 = Coord.from_chess(p[2:])
        else:
            if isinstance(p, str):
                p1 = Coord.from_chess(p)
            elif isinstance(p, Coord):
                p1 = p
            if isinstance(p2, str):
                p2 = Coord.from_chess(p2)
        if self.isfrozen:
            raise LogicError('Board is frozen and cannot move', 'Phantom.core.board.Board.move()')
        if self[p1] is None:
            raise ChessError('No piece at {}'.format(p1), 'Phantom.core.board.Board.move()')
        self.premove()
        player = self[p1].owner
        is_valid = player.validatemove(p1, p2)
        if is_valid or self.cfg.force_moves:
            log_msg('move: specified move is valid, continuing', 3)
            piece = self[p1]
            
            # update castling rights
            if piece.ptype == 'rook':
                if piece.coord == Coord(0, 0):
                    self.castling_rights = self.castling_rights.replace('Q', '')
                elif piece.coord == Coord(7, 0):
                    self.castling_rights = self.castling_rights.replace('K', '')
                elif piece.coord == Coord(0, 7):
                    self.castling_rights = self.castling_rights.replace('q', '')
                elif piece.coord == Coord(7, 7):
                    self.castling_rights = self.castling_rights.replace('k', '')
            elif piece.ptype == 'king':
                if piece.color == 'white':
                    self.castling_rights = self.castling_rights.replace('K', '')
                    self.castling_rights = self.castling_rights.replace('Q', '')
                elif piece.color == 'black':
                    self.castling_rights = self.castling_rights.replace('k', '')
                    self.castling_rights = self.castling_rights.replace('q', '')
            
            # update en_passant rights
            self.en_passant_rights = '-'
            if piece.ptype == 'pawn':
                if piece.firstmove:
                    if round_down(dist(p1, p2)) == 2:
                        file = piece.coord.as_chess()[0]
                        if piece.color == 'black':
                            self.en_passant_rights = '{}6'.format(file)
                        elif piece.color == 'white':
                            self.en_passant_rights = '{}3'.format(file)
            
            # update halfmove & fullmove
            
            # Here we update the halfmove_clock BEFORE it is altered, to save some else 
            # clauses later on.  We simply use a few ifs to determine if it needs to be
            # reset.
            self.halfmove_clock += 1
            
            if piece.ptype == 'pawn':
                self.halfmove_clock = 0
            if piece.color == 'black':
                self.fullmove_clock += 1
            
            target = self[p2]
            if self.data['move_en_passant']:
                if self[p1].color == 'white':
                    target = self[p1 - Coord(0, 1)]
                elif self[p1].color == 'black':
                    target = self[p1 + Coord(0, 1)]
                self.data['move_en_passant'] = False

            player.make_move(p1, p2)
            self.kill(target)
            self.lastmove = (p1, p2)
            self.switch_turn()
            self.postmove()
        else:
            self.postmove()
            log_msg('move: specified move is invalid', 2, err=True)
            raise InvalidMove('Attempted move ({} -> {}) is invalid!'.format(p1, p2), 'Phantom.core.board.Board.move()')
        self.unfreeze()
    
    def castle(self, pos):
        """Castle a king.  
        :param str pos: must be in ('K', 'Q', 'k', 'q') - the side & color to castle on
        """
        if pos not in self.castling_rights:
            raise InvalidMove("Cannot castle {}".format(pos))
        if pos == pos.upper():
            # white
            if pos == 'K':
                if (self[Coord(5, 0)] is None) and (self[Coord(6, 0)] is None):
                    self.premove()
                    self[Coord(4, 0)].move(Coord(6, 0))
                    self[Coord(7, 0)].move(Coord(5, 0))
                    self.castling_rights = self.castling_rights.replace('K', '')
                    self.castling_rights = self.castling_rights.replace('Q', '')
                    self.postmove()
                    self.switch_turn()
                    return
                else:
                    raise InvalidMove('Cannot castle {}: pieces in the way'.format(pos), 
                                      'Phantom.core.board.Board.castle()')
            elif pos == 'Q':
                if (self[Coord(3, 0)] is None) and (
                   self[Coord(2, 0)] is None) and (
                   self[Coord(1, 0)] is None):
                    self.premove()
                    self[Coord(4, 0)].move(Coord(2, 0))
                    self[Coord(0, 0)].move(Coord(3, 0))
                    self.castling_rights = self.castling_rights.replace('K', '')
                    self.castling_rights = self.castling_rights.replace('Q', '')
                    self.postmove()
                    self.switch_turn()
                else:
                    raise InvalidMove('Cannot castle {}: pieces in the way'.format(pos), 
                                      'Phantom.core.board.Board.castle()')
        elif pos == pos.lower():
            if pos == 'k':
                if (self[Coord(5, 7)] is None) and (self[Coord(6, 7)] is None):
                    self.premove()
                    self[Coord(4, 7)].move(Coord(6, 7))
                    self[Coord(7, 7)].move(Coord(5, 7))
                    self.castling_rights = self.castling_rights.replace('k', '')
                    self.castling_rights = self.castling_rights.replace('q', '')
                    self.postmove()
                    self.switch_turn()
                    return
                else:
                    raise InvalidMove('Cannot castle {}: pieces in the way'.format(pos),
                                      'Phantom.core.board.Board.castle()')
            elif pos == 'q':
                if (self[Coord(3, 7)] is None) and (
                   self[Coord(2, 7)] is None) and (
                   self[Coord(1, 7)] is None):
                    self.premove()
                    self[Coord(4, 7)].move(Coord(2, 7))
                    self[Coord(0, 7)].move(Coord(3, 7))
                    self.castling_rights = self.castling_rights.replace('k', '')
                    self.castling_rights = self.castling_rights.replace('q', '')
                    self.postmove()
                    self.switch_turn()
                else:
                    raise InvalidMove('Cannot castle {}: pieces in the way'.format(pos), 
                                      'Phantom.core.board.Board.castle()')
        if self.castling_rights == '':
            self.castling_rights = '-'
    
    @call_trace(3)
    @exc_catch(ChessError, LogicError, ret='Cannot promote', log=2)
    def promote(self, pos, to):
        if isinstance(pos, str):
            pos = Coord.from_chess(pos)
        elif isinstance(pos, Coord):
            pos = pos
        pawn = self[pos]
        if pawn.ptype != 'pawn':
            raise ChessError('Piece {} is not a pawn'.format(pawn), 'Phantom.core.board.Board.promote()')
        if to not in 'RNBQ':
            raise LogicError('Cannot promote pawn to piece type "{}"'.format(to), 'Phantom.core.board.Board.promote()')
        if pawn.color == 'black':
            if pawn.coord.y != 1:
                raise ChessError('Cannot promote {}'.format(pawn), 'Phantom.core.board.Board.promote()')
            x = pawn.coord.x
            newcls = ChessPiece.type_from_chr(to)
            color = pawn.color
            newpos = Coord(x, 0)
            new = newcls(newpos, color, pawn.owner)
            self.freeze()
            self.pieces.append(new)
            self.unfreeze()
            self.kill(pawn)
        elif pawn.color == 'white':
            if pawn.coord.y != 6:
                raise ChessError('Cannot promote {}'.format(pawn), 'Phantom.core.board.Board.promote()')
            x = pawn.coord.x
            newcls = ChessPiece.type_from_chr(to)
            color = pawn.color
            newpos = Coord(x, 7)
            new = newcls(newpos, color, pawn.owner)
            self.freeze()
            self.pieces.append(new)
            self.unfreeze()
            self.kill(pawn)
        self.switch_turn()
                       
    def set_checkmate_validation(self, val):
        self.cfg.do_checkmate = val
    
    # TODO: make this work
    def is_checkmate(self):
        if not self.cfg.do_checkmate:
            return False
        return False
    
    # TODO: make this work
    def will_checkmate(self, p1, p2):
        if not self.cfg.do_checkmate:
            return False
        test = Board(fen=self.fen_str())
        test.move(p1, p2)
        test.cfg.do_checkmate = self.cfg.do_checkmate
        return test.is_checkmate()
__all__.append('Board')

if __name__ == '__main__':
    b = Board()
    b.set_name('Chess')
    b.pprint()
