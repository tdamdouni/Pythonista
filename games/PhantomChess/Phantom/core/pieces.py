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

"""The core of the pieces."""

import Phantom.constants as C
from Phantom.utils.debug import call_trace  # , log_msg
import itertools
import uuid

grid_width = len(C.x_chars)

__all__ = []

# print(list(flatten(([], [0], (1, 2))))) # --> [0, 1, 2]
def flatten(list_of_lists):
    for a_list in list_of_lists:
        for element in a_list:
            yield element

class ChessPiece(object):  # (PhantomObj):
    # overwritten by subclasses
    ptype = None
    default_origins = []

    @staticmethod
    def type_from_chr(p_chr):
        """Get the piece class from a SAN character."""
        # 671: updated to use characters defined in PhantomConfig.cfg
        piece_dict = {C.piece_chars['black pawn'][0]: Pawn,
                      C.piece_chars['black rook'][0]: Rook,
                      C.piece_chars['black knight'][0]: Knight,
                      C.piece_chars['black bishop'][0]: Bishop,
                      C.piece_chars['black queen'][0]: Queen,
                      C.piece_chars['black king'][0]: King}
        return piece_dict.get(p_chr.lower(), None)

    def __init__(self, owner, fen_loc):
        self.owner = owner
        self.fen_loc = fen_loc
        as_ascii, as_unicode = C.piece_chars[self.name]
        self.fen_char = as_ascii
        self.disp_char = as_unicode if C.use_unicode else as_ascii
        # freeze: self.isFrozen = False  # piece level freeze
        self.promotable = False
        self.first_move = True
        self.directions_valid = self.directions_all
        self._uuid = uuid.uuid4()
        self.data = dict()  # should this be the UserDict mixin from the standard library?

        # this cache holds moves that are allowed by the .apply_ruleset() method
        # it will be updated after a move and is used to speed up the .valid() method
        # by shortening the list it must iterate through
        # ! self.subvalid_cache = self.update_cache()  FIXME!
        self.subvalid_cache = []
        # print(self.col, self.x)

    def __repr__(self):
        fmt = '<{} at {} ({}, {}) in {}>'
        return fmt.format(self.name, self.fen_loc, self.x, self.y, hex(id(self)))

    def __hash__(self):
        return int(self._uuid) % (self.owner.moves + 1)

    @property
    def board(self):
        return self.owner.board

    @property
    def color(self):
        return self.owner.color

    @property
    def is_my_turn(self):
        return self.owner.is_my_turn

    @property
    def name(self):
        return '{} {}'.format(self.color, self.ptype).lower()

    @property
    def as_type_at_loc(self):
        return '{} @ {}'.format(self.ptype, self.fen_loc)

    # @property
    # def image(self):
    #    return '{}_{}'.format(self.color, self.ptype)

    @property
    def col(self):
        return self.fen_loc[0]

    @property
    def row(self):
        return self.fen_loc[1]

    @property
    def x(self):
        # print('property x: {}.index({}) --> {}'.format(C.x_chars, self.col, C.x_chars.index(self.col)))
        return C.x_chars.index(self.col)

    @property
    def y(self):
        # print('property y: {}.index({}) --> {}'.format(C.y_chars, self.row, C.y_chars.index(self.row)))
        return C.y_chars.index(self.row)

    # 671: @ccc you were right in commit 79e3218 - __str__ causes loops
    @property
    def as_str(self):
        #valid = 'FIXME'  # [c.as_chess for c in self.valid()] # FIXME
        valid = ', '.join(self.all_valid_moves)
        threatens = ', '.join(self.board[loc].as_type_at_loc for loc in self.threatens)
        threats = ', '.join(piece.as_type_at_loc for piece in self.threatened_by)
        return """    {}
    Valid moves: {}
    Is promotable: {}
    This piece threatens: {}
    This piece is threatened by: {}
    """.format(repr(self), valid, self.promotable, threatens, threats)

    #@call_trace(3)
    @property
    def threatens(self):
        """List of fen_locs of pieces that this piece could kill."""
        # return [self.board[move] for move in self.valid() if self.board[move]]
        #print(self, 'threatens')
        reachable_neighbors = []
        for func in self.directions_all:
            reachable_neighbors += func()
        #print(self, 'threatens', [x for x in (dest for dest in reachable_neighbors
        #        if self.is_move_valid(dest) and self.friend_or_foe(dest) == 'foe')])
        return (dest for dest in reachable_neighbors
                if self.is_move_valid(dest) and self.friend_or_foe(dest) == 'foe')
        #print(sorted(reachable_neighbors))
        #print(0)
        #reachable_neighbors = [dest for dest in [func() for func in self.directions_all] if dest]
        #print('rn', reachable_neighbors)
        #print(dest for dest in (x for x in reachable_neighbors if x))
        #return (dest for dest in (x for x in reachable_neighbors)
        #        if self.is_move_valid(dest) and self.friend_or_foe(dest) == 'foe')

    # @call_trace(3)
    @property
    def threatened_by(self):
        """List pieces that could kill this piece."""
        return self.board.threatened_by(self)
        # return [piece for piece in self.board.all_legal()
        #        if piece.color != self.color and self.coord in piece.valid()]

    # @property
    # def as_chess(self):
    #    return '{} @ {}'.format(self.fen_char, self.fen_loc)

    # 671: should this be a property or a function?  Does it even matter?
    # ccc: property.  but perhaps only a property of Pawns
    @property
    def is_promotable(self):
        """Tests if a piece is promotable."""
        if self.ptype != 'pawn':
            return False
        return ((self.color == 'white' and self.row == '8')
                or (self.color == 'black' and self.row == '1'))

    def friend_or_foe(self, target):
        occupant = self.board[target]
        if occupant:
            return 'friend' if occupant.color == self.color else 'foe'
        else:
            return None

    # method is only usable after set_owner is used
    def suicide(self):
        self.board.kill(self)

    ## implementation detail 5
    # @call_trace(3)
    # def valid(self):
    #    return [pos for pos in self.subvalid_cache if self.owner.validatemove(self.coord, pos)]

    # ccc: could we use friend_or_foe()?
    # @call_trace(3)
    # def check_target(self, target):
    #    """See if a target is valid.  Does not perform full move validation."""
    #    piece = self.board[target]
    #    if not piece:
    #        log_msg('check_target: target is None, True', 5)
    #        ret = True
    #    elif piece.color == self.color:
    #        log_msg('check_target: target is same color, False', 5)
    #        ret = False
    #    else:
    #        log_msg('check_target: unknown, True', 5)
    #        ret = True
    #    return ret

    '''
    @call_trace(3)
    def check_path(self, path):
        """Check to see if a given path is clear."""
        for pos in path[:-1]:
            piece = self.board[pos]
            if piece:
                return False
        return True

    # TODO: make this work properly (sometimes it overshoots the target)
    # 671: this seems to work on all pieces except the bishops, would an
    #      iterative process be better:
    #    pdir = dirfinder(self, target)
    #    i = self.coord.__copy__()
    #    ret = []
    #    while not self.board[target]:
    #        i += some other coord at a dist of one in the correct direction
    #        ret.append(i)
    #    return ret

    # @ccc pointed out in issue #49 that a piece at (7, 7) has pieces to southeast
    #      and northwest, neither of which is correct.
    @call_trace(3)
    def path_to(self, target):
        """Generate a path to a target."""
        pdir = self.dir_finder(target)                        # get the direction to target
        dist_to = int(round_down(dist(self.coord, target)))   # determine distance to target
        path = pdir[1](self)                                  # get list of squares in target direction
        squares = path                                        # copy list
        while len(squares) > dist_to:                         # shrink list iteratively until len(squares) == dist_to
            squares = squares[:-1]                            # shrink list iteratively until len(squares) == dist_to
        return squares                                        # return list
    '''

    # This applies the piece's ruleset as described in level 1.1
    def apply_ruleset(self, target):
        return True

    @property
    def all_moves(self):
        """returns a list of all fen_locs that can be moved to.
        It does NOT check the validity of each move."""
        return sorted(flatten(func() for func in self.directions_valid))

        #def print_neighbors(self):
        #print('Neighbors for {}:'.format(self))
        #print('\n'.join('{:>5}: {}'.format(func.__name__, ' '.join(func()))
        #                for func in self.directions_all))
        #return 'FIXME'

    @property
    def all_valid_moves(self):
        return (dest for dest in self.all_moves if self.is_move_valid(dest))
        #def print_neighbors(self):
        #print('Neighbors for {}:'.format(self))
        #print('\n'.join('{:>5}: {}'.format(func.__name__, ' '.join(func()))
        #                for func in self.directions_all))
        #return 'FIXME'

    @call_trace(3)
    def clear_path_to_target(self, target):  # knight and pawn will have their own implementations
        pdir = self.dir_finder(target)  # get the direction to target
        if not pdir:
            return False  # you can not get there
        for fen_loc in pdir[1]():  # pdir is ['north', north()]
            if fen_loc == target:
                return True  # target was reached
            if self.board[fen_loc]:
                return False  # another piece is in the way

    @call_trace(2)
    def is_move_valid(self, target):  # used by move() and threatens()
        return (C.is_valid_fen_loc(target)
                and self.friend_or_foe(target) != 'friend'
                and self.apply_ruleset(target)
                and self.clear_path_to_target(target))

    @call_trace(2)
    def move(self, dest):
        if not self.is_my_turn:
            return False
        if not self.is_move_valid(dest):
            return False
        self.fen_loc = dest
        self.owner.moves += 1  # my boss likes to take credit for my work
        self.first_move = False
        return True

    # @call_trace(2)
    # def move(self, target):
    #    """Go somewhere."""
    #    self.board.kill(self.board[target])
    #    self.coord = target
    #    self.subvalid_cache = self.update_cache()
    #    self.first_move = False

    @call_trace(4)
    def update_cache(self):
        """Return an updated subvalid cache."""
        return []  # FIXME
        # return [tile.fen_loc for tile in self.board.tiles if self.apply_ruleset(tile.fen_loc)]

    @property
    def north_part(self):  # 'd4' --> '5678'
        return reversed(C.y_chars.partition(self.row)[0])

    @property
    def south_part(self):  # 'd4' --> '321'
        return C.y_chars.partition(self.row)[2]

    @property
    def east_part(self):  # 'd4' --> 'efgh'
        return C.x_chars.partition(self.col)[2]

    @property
    def west_part(self):  # 'd4' --> 'cba'
        return reversed(C.x_chars.partition(self.col)[0])

    # the following functions return a list of max_count or fewer
    # neighboring fen_locs in order from closest to furthest
    # 'a4'.north()  --> a5 a6 a7 a8
    # 'a4'.north(1) --> a5
    # 'a4'.north(2) --> a5 a6
    def north(self, max_count=grid_width):
        return [x + y for x, y in zip(self.col * max_count, self.north_part)]

    def south(self, max_count=grid_width):
        return [x + y for x, y in zip(self.col * max_count, self.south_part)]

    def east(self, max_count=grid_width):
        return [x + y for x, y in zip(self.east_part, self.row * max_count)]

    def west(self, max_count=grid_width):
        return [x + y for x, y in zip(self.west_part, self.row * max_count)]

    def ne(self, max_count=grid_width):
        return [x + y for x, y in zip(self.east_part, self.north_part)][:max_count]

    def se(self, max_count=grid_width):
        return [x + y for x, y in zip(self.east_part, self.south_part)][:max_count]

    def nw(self, max_count=grid_width):
        return [x + y for x, y in zip(self.west_part, self.north_part)][:max_count]

    def sw(self, max_count=grid_width):
        return [x + y for x, y in zip(self.west_part, self.south_part)][:max_count]

    @property
    def directions_major(self):
        return self.north, self.east, self.south, self.west

    @property
    def directions_diagonal(self):
        return self.ne, self.se, self.sw, self.nw

    @property
    def directions_all(self):
        return (self.north, self.ne, self.east, self.se,
                self.south, self.sw, self.west, self.nw)

    def print_neighbors(self):
        print('Neighbors for {}:'.format(self))
        print('\n'.join('{:>5}: {}'.format(func.__name__, ' '.join(func()))
                        for func in self.directions_all))
        print('    valid_moves:', ', '.join(self.all_moves))
        print('all_valid_moves:', ', '.join(self.all_valid_moves))

    def dir_finder(self, target, max_count=grid_width):
        """Locate the direction in which the target lies and return a 2-tuple of:
        (the string of the direction, the function that gives it)"""
        # for func in (self.north, self.south, self.east, self.west,
        #                self.ne, self.nw, self.se, self.sw):
        for func in self.directions_all:
            if target in func(max_count):
                return func.__name__, func
        return None


__all__.append('ChessPiece')

# Individual piece subtypes

class Pawn(ChessPiece):
    ptype = 'pawn'
    # default_origins = [Coord(x, y) for x in range(C.grid_width) for y in (1, 6)]
    default_origins = 'a2 b2 c2 d2 e2 f2 g2 h2 a7 b7 c7 d7 e7 f7 g7 h7'.split()
    # default_origins = [x+'2' for x in C.x_chars] + [x+'7' for x in C.x_chars]
    # assert default_origins == default_originz
    # y = '2' if self.color == 'white' else '7'
    # default_origins = [x+y for x in C.x_chars]
    # tests = [Coord(1, 1), Coord(-1, 1)]

    def __init__(self, owner, fen_loc):
        ChessPiece.__init__(self, owner, fen_loc)
        default_row = '2' if self.color == 'white' else '7'
        self.en_passant_rights = self.row == default_row

    #@call_trace(4)
    @property
    def threatens(self):
        """Returns a list of fen_locs of pieces that this piece could kill."""
        if self.color == 'white':
            diagonal_kills = self.ne(1) + self.nw(1)
        else:
            diagonal_kills = self.se(1) + self.sw(1)
        #print(self, 'pawn threatens', [x for x in [diagonal_kill for diagonal_kill in diagonal_kills
        #        if self.friend_or_foe(diagonal_kill) == 'foe']])
        return [diagonal_kill for diagonal_kill in diagonal_kills
                if self.friend_or_foe(diagonal_kill) == 'foe']

    @call_trace(4)
    def apply_ruleset(self, target):
        if not self.first_move:
            self.en_passant_rights = False
        forward_steps = 2 if self.en_passant_rights else 1
        if self.color == 'white':
            allowed = self.north(forward_steps)
        else:
            allowed = self.south(forward_steps)
        allowed = [x for x in allowed if not self.friend_or_foe(x)] + self.threatens
        #print('{}.apply_ruleset({}) --> {}'.format(self, target, allowed))
        return target in allowed
        '''
        
        
        if self.color == 'white':
            op = lambda a, b: a + b
        elif self.color == 'black':
            op = lambda a, b: a - b

        allowed = [Coord(self.x, op(self.y, 1)).as_chess]
        if self.first_move:
            allowed.append(Coord(self.x, op(self.y, 2)).as_chess)
        print(allowed)
        for move in allowed:
            piece = self.board.pieces_dict.get(move, None)
            if piece and piece.color == self.color:
            #if move in self.board.pieces_dict:
                allowed.remove(move)
        tests = [op(self.zcoord, self.tests[0]), op(self.zcoord, self.tests[1])]
        for test in tests:
            if test.as_chess in self.board.pieces:
                allowed.append(test.as_chess)

        ret = target in allowed

        if self.board.en_passant_rights == '-':
            self.board.data['move_en_passant'] = False
        elif Coord.from_chess(self.board.en_passant_rights) in tests:
            self.board.data['move_en_passant'] = True
            ret = True
        else:
            self.board.data['move_en_passant'] = False

        return ret
    '''

    # The reason for overriding this method is that the pawns, after moving,
    # may *not* have en passant rights or other weird things that pawns can do
    # These would not be included in the .subvalidcache list and therefore not
    # displayed on the GUI as valid moves
    #def valid(self):
    #    self.subvalid_cache = self.update_cache()
    #    return [p for p in self.subvalid_cache if self.owner.validate_move(self.coord, p)]


__all__.append('Pawn')


class Rook(ChessPiece):
    ptype = 'rook'
    # default_origins = [Coord(x, y) for x in (0, 7) for y in (0, 7)]
    default_origins = 'a1 a8 h1 h8'.split()

    def __init__(self, owner, fen_loc):
        ChessPiece.__init__(self, owner, fen_loc)
        self.directions_valid = self.directions_major  # north, south, east, west

    @call_trace(4)
    def apply_ruleset(self, target):
        # return (target in self.north()
        #     or target in self.south()
        #     or target in self.east()
        #     or target in self.west())
        for func in self.directions_major:
            if target in func():
                return True

    @call_trace(2)
    def move(self, dest):
        return_code = ChessPiece.move(self, dest)
        if return_code and self.first_move:
            castling_partner = {'a1': 'Q',
                                'h1': 'K',
                                'a8': 'q',
                                'h8': 'k'}.get(self.fen_loc, '')
            self.board.castling_rights = self.board.castling_rights.replace(castling_partner, '')
        return return_code

__all__.append('Rook')


class Bishop(ChessPiece):
    ptype = 'bishop'
    # default_origins = [Coord(x, y) for x in (2, 5) for y in (0, 7)]
    default_origins = 'c1 c8 f1 f8'.split()

    def __init__(self, owner, fen_loc):
        ChessPiece.__init__(self, owner, fen_loc)
        self.directions_valid = self.directions_diagonal  # ne, se, sw, nw

    @call_trace(4)
    def apply_ruleset(self, target):
        # return (target in self.ne()
        #     or target in self.se()
        #     or target in self.sw()
        #     or target in self.nw())
        for func in self.directions_diagonal:
            if target in func():
                return True

__all__.append('Bishop')


class Queen(ChessPiece):
    ptype = 'queen'
    # default_origins = [Coord(3, y) for y in (0, 7)]
    default_origins = 'd1 d8'.split()

    @call_trace(4)
    def apply_ruleset(self, target):
        # return (target in self.north()
        #     or target in self.ne()
        #     or target in self.east()
        #     or target in self.se()
        #     or target in self.south()             
        #     or target in self.sw()
        #     or target in self.west()
        #     or target in self.nw())
        for func in self.directions_all:
            if target in func():
                return True


__all__.append('Queen')


class King(ChessPiece):
    ptype = 'king'
    # default_origins = [Coord(4, y) for y in (0, 7)]
    default_origins = 'e1 e8'.split()

    # @call_trace(4)
    # def _apply_ruleset(self, target):
    #    return round_down(dist(self.coord, target)) == 1

    @call_trace(4)
    def apply_ruleset(self, target):
        # return (target in self.north(1)
        #     or target in self.ne(1)
        #     or target in self.east(1)
        #     or target in self.se(1)
        #     or target in self.south(1)             
        #     or target in self.sw(1)
        #     or target in self.west(1)
        #     or target in self.nw(1))
        for func in self.directions_valid:
            if target in func(1):
                return True

    @property
    def all_moves(self):
        """returns a list of all fen_locs that can be moved to.
        It does NOT check the validity of each move."""
        return sorted(flatten(func(1) for func in self.directions_all))

    '''
    return False  # FIXME!!
        if not self.board.cfg.do_checkmate:
            return self._apply_ruleset(target)
        empty_board = self._apply_ruleset(target)  # could move if there were no pieces on the board
        other_allowed = []
        self.board.set_checkmate_validation(False)  # avoid recursion
        for piece in self.board.pieces:
            if piece.color != self.color:
                other_allowed.extend(piece.valid())
        self.board.set_checkmate_validation(True)
        return False if target in other_allowed else empty_board
    '''


__all__.append('King')


class Knight(ChessPiece):
    ptype = 'knight'
    # default_origins = [Coord(x, y) for x in (1, 6) for y in (0, 7)]
    default_origins = 'b1 b8 g1 g8'.split()

    def knight_moves(self):  # front page drivin' news
        the_moves = []
        for x, y in itertools.permutations((-1, 1, -2, 2), 2):
            if abs(x) != abs(y):
                x = self.x + x
                y = self.y + y
                if 0 <= x <= 7 and 0 <= y <= 7:
                    the_moves.append(C.x_chars[x] + C.y_chars[y])
        # print('{}.knight_moves: {} ({}, {}) {}'.format(self.__class__.__name__, self, self.x, self.y, the_moves))
        return tuple(the_moves)

    @call_trace(4)
    def apply_ruleset(self, target):
        return target in self.knight_moves()

    @property
    def all_moves(self):
        """returns a list of all fen_locs that can be moved to.
        It does NOT check the validity of each move."""
        return self.knight_moves()


    @call_trace(4)
    # override this method for two reasons:
    # A. knights can jump over pieces so this is irrelevant
    # B. the path generator doesn't work properly for the knight's direction of movement
    #    and this saves having to implement special-case code in the ChessPiece.path_to method
    # def path_to(self, target):
    #    return [0]
    def clear_path_to_target(self, target):
        return True

    #@call_trace(4)
    @property
    def threatens(self):
        """Returns a list of fen_locs of pieces that this piece could kill."""
        return (dest for dest in self.knight_moves()
                if self.friend_or_foe(dest) == 'foe')

__all__.append('Knight')

if __name__ == '__main__':
    print('=' * 20)
    from Phantom.core.players import Player

    p = Pawn(Player(None, 'white'), 'a4')
    p.print_neighbors()
    print(p.as_str())
    p.fen_loc = 'b5'
    p.print_neighbors()
    print(p.as_str())
