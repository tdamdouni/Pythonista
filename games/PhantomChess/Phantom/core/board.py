# -*- coding: utf-8 -*-
from __future__ import (absolute_import, division, print_function, unicode_literals)

#        1         2         3         4         5         6         7         8
# 345678901234567890123456789012345678901234567890123456789012345678901234567890

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

import Phantom.constants as C
from Phantom.core.chessobj import PhantomObj
from Phantom.core.players import Player
from Phantom.core.exceptions import ChessError, InvalidMove, LogicError
from Phantom.core.pieces import ChessPiece
from Phantom.boardio.save import save
from Phantom.boardio.load import load_game
from Phantom.boardio.boardcfg import Cfg
from Phantom.utils.debug import call_trace, log_msg
from Phantom.utils.decorators import exc_catch
#from Phantom.functions import round_down, dist
import collections
import contextlib
import uuid

__all__ = []

def load(name):
    fen_str = load_game(name)
    game = Board(None, fen_str)
    game.set_name(name)
    return game
__all__.append('load')

class Tile (PhantomObj):
    isfrozen = False

    def __init__(self, fen_loc):
        self.fen_loc = fen_loc
        self.color = C.color_by_number(self.x + self.y)
        if self.color == 'black':
            self.disp_char = C.black_space_char[int(C.use_unicode)]  # zero or one
        else:
            self.disp_char = C.white_space_char[int(C.use_unicode)]  # zero or one
        self.tile_color = C.grid_colors[self.color]
        #print(repr(self))

    def __repr__(self):
        fmt = '<{} {} at {} ({}, {}) in {}>'
        return fmt.format(self.color, self.__class__.__name__,
                            self.fen_loc, self.x, self.y, hex(id(self)))

    @property
    def col(self):
        return self.fen_loc[0]

    @property
    def row(self):
        return self.fen_loc[1]

    @property
    def x(self):
        return C.x_chars.index(self.col)

    @property
    def y(self):
        return C.y_chars.index(self.row)

__all__.append('Tile')

def _make_pieces_dict(fen_str='rnbqkbnr/pppppppp/8/8/8/8/PPPPPPPP/RNBQKBNR'):
    # returns a dict of {fen_str : fen_char} entries like {'e8': 'k'}
    pieces_dict = collections.OrderedDict()
    for y, row_fen in enumerate(fen_str.split('/')):
        x = 0
        for c in row_fen:
            if c.isdigit():
                x += int(c)
            else:
                pieces_dict[C.fen_loc_from_xy(x, y)] = c
                x += 1
    return pieces_dict

class Board (PhantomObj):
    # ccc: would a chess server ever run multiple boards at the same time?
    #      if so, these should be instance variables, not class variables.
    isfrozen = False  # is the board frozen?  ccc: are all boards frozen
    movenum = 0       # how many moves have been made  ccc: moves on all boards combined

    def __init__(self, chess_game, fen_str=None, **cfgkws):
        self.game = chess_game
        self.fen_str = fen_str or C.opening_fen
        assert isinstance(self.fen_str, basestring), str(type(self.fen_str))
        self.players_dict = {color : Player(self, color) for color in C.colors}
        self.tiles_dict = {fen_loc: Tile(fen_loc) for fen_loc in C.fen_locs()}
        self.dead = set()
        self.name = 'New Game'
        self.cfg = Cfg(**cfgkws)
        self.cfg.set_board(self)
        self.lastmove = (None, None)
        self.move_count = 0
        self._uuid = uuid.uuid4()
        self.data = dict()
        self.start_pos = self.fen_str
        self.turn = 'white'
        self.castling_rights = None
        self.en_passant_rights = None
        self.halfmove_clock = None
        self.fullmove_clock = None
        pieces = self.fen_parse(self.fen_str)
        self.pieces_dict = self.make_pieces_dict(pieces)

    def fen_parse(self, fen_str):
        # parse given FEN and create board layout
        assert isinstance(fen_str, basestring), str(type(fen_str))
        fields = fen_str.split()
        if not len(fields) == 6:
            print('\n'.join(fields))
            #import sys
            #sys.exit(len(fields))
            raise ChessError('Invalid FEN given to board',
                             'Phantom.core.board.fen_parse')
        pieces, moving_color, castling, en_passant, halfmove, fullmove = fields
        self.turn = 'white' if moving_color.lower() == 'w' else 'black'
        self.castling_rights = castling
        self.en_passant_rights = en_passant
        self.halfmove_clock = int(halfmove)
        self.fullmove_clock = int(fullmove)
        return pieces

    # Do players need to make / own their pieces?
    def make_piece(self, fen_loc, fen_char):
        fmt =  'Invalid fen_char: {} not in {}.'
        assert fen_char in C.fen_chars, fmt.format(fen_char, C.fen_chars)
        color = 'white' if fen_char in C.white_chars else 'black'
        return self.players_dict[color].make_piece(fen_loc, fen_char)

    def make_pieces_dict(self, pieces_fen):
        pieces_dict = _make_pieces_dict(pieces_fen)
        # replace each fen_char in the dict with a real Piece object
        for fen_loc, fen_char in pieces_dict.iteritems():
            pieces_dict[fen_loc] = self.make_piece(fen_loc, fen_char)
        return pieces_dict

    @property
    def players(self):
        return self.players_dict.itervalues()

    @property
    def tiles(self):
        return self.tiles_dict.itervalues()
    
    @property
    def pieces(self):
        return self.pieces_dict.itervalues()

    def __contains__(self, piece):
        return piece in self.pieces

    def __hash__(self):
        return int(self._uuid) % len(self.pieces) + self.fullmove_clock

    # implementation detail 0, 1
    def __getitem__(self, fen_loc):
        assert C.is_valid_fen_loc(fen_loc), '__getitem__({})'.format(fen_loc)
        return self.pieces_dict.get(fen_loc, None)

    def disp_char(self, fen_loc):
        #if fen_loc in self.pieces_dict:
        #    return self.pieces_dict[fen_loc].disp_char
        #else:
        #    return self.tiles_dict[fen_loc].disp_char
        return (self[fen_loc] or self.tile_at(fen_loc)).disp_char

    def tile_at(self, fen_loc):
        return self.tiles_dict[fen_loc]
    
    def get_player_by_color(self, color):
        return self.players_dict[color]

    def get_piece_list(self, ptype=None, color=None):
        pieces = self.pieces
        pieces = [p for p in pieces if p.ptype == ptype] if ptype else pieces
        return   [p for p in pieces if p.color == color] if color else pieces

    @call_trace(4)
    def as_fen_str(self):  # FIXME: could this be __repr__()?
        rank_split = C.fen_rank_split or '/'
        fen = ''
        for y in C.y_chars:
            file_gap = 0
            for x in C.x_chars:
                fen_loc = x+y
                piece = self[fen_loc]
                if not piece:
                    file_gap += 1
                    continue
                else:
                    if file_gap > 0:
                        fen += str(file_gap)
                        file_gap = 0
                    fen += piece.fen_char
            if y != '1':
                if file_gap > 0:
                    fen += str(file_gap)
                fen += rank_split
        self.upd_rights()  # make sure the castling rights aren't ''
        fen += ' {turn} {castle} {ep} {half} {full}'.format(
                turn=self.turn[0], castle=self.castling_rights,
                ep=self.en_passant_rights, half=self.halfmove_clock,
                full=self.fullmove_clock)
        print('as_fen_str:', fen)
        return fen

    def all_legal(self):  # FIXME: Still needed?
        ret = {}
        for piece in self.pieces:
            try:
                ret.update({piece: piece.valid()})
            except AttributeError:  # ccc: why would this exception be thrown?
                continue
        return ret

    def _pprnt(self):  #  FIXME: could this be __str__()?
        dash   = '–' if self.cfg.use_unicode else '-'
        turn_indicator = ' ' + C.turn_indicator[int(C.use_unicode)]  # zero or one
        header = '  ' + ' '.join(C.x_chars)
        lines = [self.name.center(19), dash * 19, header]
        fmt = '{} {} {}{}'
        for y in C.y_chars:
            pieces = ' '.join(self.disp_char(x+y) for x in C.x_chars)
            ti = turn_indicator if ((y == '1' and self.turn == 'white')
                                 or (y == '8' and self.turn == 'black')) else ''
            lines.append(fmt.format(y, pieces, y, ti))
        lines.append(header)
        return '\n'.join(lines).encode(C.default_encoding)          

    def pprint(self):
        """Print a pretty version of the board."""
        in_pythonista = False
        try:
            import console
            console.set_font('DejaVuSansMono', 18)
            in_pythonista = True
        except ImportError:
            pass
        print(self._pprnt())
        if in_pythonista:
            console.set_font()

    def __str__(self):
        return self.fen_str

    def save(self, name):
        self.set_name(name)
        save(self)

    def set_name(self, name):
        self.name = name

    def set_game(self, g):
        self.game = g
        self.cfg.set_game(g)

    #freeze:def freeze(self):
    #freeze:    """Lock the board in place."""
    #freeze:    self.isfrozen = True
    #freeze:    #self.pieces = list(self.pieces)
    #freeze:    for player in self.players:
    #freeze:        player.freeze()

    #freeze:def unfreeze(self):
    #freeze:    """Unlock the board."""
    #freeze:    self.isfrozen = False
    #freeze:    #self.pieces = set(self.pieces)
    #freeze:    for player in self.players:
    #freeze:        player.unfreeze()

    #freeze:@contextlib.contextmanager
    #freeze:def frozen(self):
    #freeze:    self.freeze()
    #freeze:    yield
    #freeze:    self.unfreeze()

    def premove(self):
        """Freeze everything and send a signal to players that a move will be
        made."""
        #freeze:self.freeze()
        for player in self.players:
            player.premove()

    def postmove(self):
        """Unfreeze and send a signal to players that a move has been
        completed."""
        #freeze:self.unfreeze()
        for player in self.players:
            player.postmove()

    def switch_turn(self):
        for player in self.players:
            if player.color == self.turn:
                player.timer.pause()
            else:
                player.timer.resume()
        self.turn = C.opposite_color(self.turn)

    def upd_rights(self):
        """This method soely exists so that if an exception occurs during a
        method that should have reset either en passant rights or castling
        rights and wasnt able to because of the error.  This method will find
        any '' strings and correct them to '-'."""
        self.castling_rights = self.castling_rights or '-'
        self.en_passant_rights = self.en_passant_rights or '-'

    #@call_trace(2)
    #@exc_catch(KeyError, ret='Could not kill specified piece', log=3)
    #def kill(self, piece):
    #    if not piece:
    #        return
    #    self.halfmove_clock = 0
    #    piece.owner.lose_piece(piece)
    #    self.dead.add(piece)
    #    self.pieces.remove(piece)

    # accepts: move('a1', 'b2') or move('a1b2')
    @call_trace(1)
    #@exc_catch(LogicError, ChessError, KeyError,
    #           ret='Cannot make specified move', log=4)
    def move(self, srce, dest=None):
        if not dest:                      # if srce is 'a1b2':
            srce, dest = srce[:2], srce[2:]  # srce = 'a1', dest = 'b2'
        assert C.is_valid_fen_loc(srce)
        assert C.is_valid_fen_loc(dest)
        #freeze:if self.isfrozen:
        #freeze:    raise LogicError('Board is frozen and cannot move',
        #freeze:                     'Phantom.core.board.Board.move()')
        piece = self[srce]
        if not piece:
            raise ChessError('No piece at {}'.format(srce),
                             'Phantom.core.board.Board.move()')
            #return False
        if piece.color != self.turn:
            raise ChessError("It is not {}'s turn.".format(piece.color),
                             'Phantom.core.board.Board.move()')
            #return False
        return_code = piece.move(dest)
        if return_code:
            dead_guy = self.pieces_dict.pop(dest, None)
            self.pieces_dict[dest] = self.pieces_dict.pop(srce)
            if dead_guy and dead_guy.ptype == 'king':
                print('Game over man!!')
                #import sys
                #sys.exit('Game over man!!')
            print(piece.as_str)
            # print('history:', self.game.history)
            # print('  moves:', self.game.moves)
            # piece.print_neighbors()
            self.move_count += 1
            self.switch_turn()
        return return_code

        '''
        target = self[dest]
        if target and target.owner == piece.owner:
            print('You can not kill one of your own men!')
            return False

        self.premove()
        player = piece.owner
        if not player.validate_move(srce, dest):
            print('Move is not valid and was rejected: {} --> {}'.format(srce, dest))
            return False
        #print('True = {}.validatemove({}, {})'.format(player, srce, dest))
        if True:  # is_valid or self.cfg.force_moves:
            log_msg('move: specified move is valid, continuing', 3)
            # update castling rights
            if piece.ptype == 'rook':
                castling_partner = {'a1' : 'Q',
                                    'h1' : 'K',
                                    'a8' : 'q',
                                    'h8' : 'k'}.get(piece.fen_loc, '')
                self.castling_rights = self.castling_rights.replace(castling_partner, '')
            elif piece.ptype == 'king':  # ccc: if __queen__ moves, can she stll castle?
                if piece.color == 'white':
                    self.castling_rights = self.castling_rights.replace('K', '')
                    self.castling_rights = self.castling_rights.replace('Q', '')
                elif piece.color == 'black':
                    self.castling_rights = self.castling_rights.replace('k', '')
                    self.castling_rights = self.castling_rights.replace('q', '')

            # ccc: en_passent rights moved into Pawn
            # update en_passant rights
            #self.en_passant_rights = '-'
            #if piece.ptype == 'pawn':
            #    if piece.first_move:
            #        if round_down(dist(srce, dest)) == 2:
            #            file = piece.coord.as_chess[0]
            #            if piece.color == 'black':
            #                self.en_passant_rights = '{}6'.format(file)
            #            elif piece.color == 'white':
            #                self.en_passant_rights = '{}3'.format(file)

            # update halfmove & fullmove

            # Here we update the halfmove_clock BEFORE it is altered, to save
            # some else clauses later on.  We simply use a few ifs to determine
            # if it needs to be reset.
            self.halfmove_clock += 1

            if piece.ptype == 'pawn':
                self.halfmove_clock = 0
            if piece.color == 'black':
                self.fullmove_clock += 1

            #target = self[dest]
            #if self.data.get('move_en_passant', None):
            #    if piece.color == 'white':
            #        target = self[srce - Coord(0, 1)]
            #    elif piece.color == 'black':
            #        target = self[srce + Coord(0, 1)]
            #    self.data['move_en_passant'] = False

            #player.make_move(p1, p2)
            #print(0, piece, srce, dest)
            #print('sb', self.pieces_dict.get(srce, None))
            piece = self.pieces_dict.pop(srce)  # vacate srce square
            #print('sa', self.pieces_dict.get(srce, None))
            #print(1, piece.fen_loc)
            piece.fen_loc = dest
            #print(2, piece.fen_loc)
            #print('db', self.pieces_dict.get(dest, None))
            self.pieces_dict[dest] = piece      # links piece and unlinks target
            #print('da', self.pieces_dict.get(dest, None))
            #print(3, piece, srce, dest)

            #self.kill(target)
            self.lastmove = (srce, dest)
            self.switch_turn()
            self.postmove()
            #print(4)
        else:
            assert False, 'if True: above!!'
            self.postmove()
            log_msg('move: specified move is invalid', 2, err=True)
            raise InvalidMove('Attempted move ({} -> {}) is invalid!'.format(
                              srce, dest), 'Phantom.core.board.Board.move()')
        #freeze:self.unfreeze()
        print('return True')
        return True
        '''

    def threatened_by(self, piece):
        """Returns a list of pieces that threaten piece"""
        #print('{}.threatened_by({}) --> {}'.format(self, piece, self.get_piece_list(color=C.opposite_color(piece.color))))
        #for p in self.get_piece_list(color=C.opposite_color(piece.color)):
        #    print(p, [x for x in p.threatens])
        #print('done.')
        return (p for p in self.get_piece_list(color=C.opposite_color(piece.color))
#                 if p.is_move_valid(piece.fen_loc))
                if piece.fen_loc in p.threatens)

        #print(0, self.get_piece_list(color=C.opposite_color(piece.color)))
#        return (p for p in self.get_piece_list(color=C.opposite_color(piece.color))
#                 if p.is_move_valid(piece.fen_loc))
#                if piece.fen_loc in p.threatens)

    # ccc: TODO FIXME from here down is broken...

    def castle(self, pos):
        """Castle a king.
        :param str pos: must be in ('K', 'Q', 'k', 'q') - the side & color to
        castle on
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
            #freeze:self.freeze()
            self.pieces.append(new)
            #freeze:self.unfreeze()
            self.kill(pawn)
        elif pawn.color == 'white':
            if pawn.coord.y != 6:
                raise ChessError('Cannot promote {}'.format(pawn), 'Phantom.core.board.Board.promote()')
            x = pawn.coord.x
            newcls = ChessPiece.type_from_chr(to)
            color = pawn.color
            newpos = Coord(x, 7)
            new = newcls(newpos, color, pawn.owner)
            #freeze:self.freeze()
            self.pieces.append(new)
            #freeze:self.unfreeze()
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
    from Phantom.core.game_class import ChessGame
    b = ChessGame().board
    b.set_name('Chess')
    b.pprint()
