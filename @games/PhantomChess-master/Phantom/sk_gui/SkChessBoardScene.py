#!/usr/bin/env python
# -*- coding: utf-8 -*-
from __future__ import (absolute_import, division, print_function, unicode_literals)

import dialogs, os, sk, sound, ui
import Phantom.constants as C
from Phantom.core.exceptions import ChessError, InvalidMove, LogicError
from Phantom.core.pieces import ChessPiece
from Phantom.core.game_class import ChessGame

w, h = ui.get_screen_size()
# globals values are reset in SkChessBoardScene.did_change_size()
square_size = min(w-24, h-24) / 8
#half_ss = square_size / 2
tile_Size = sk.Size(square_size, square_size)
piece_Size = sk.Size(square_size - 2, square_size - 2)


class sk_BoardSquare(sk.SpriteNode):
    def __init__(self, tile):
        sk.SpriteNode.__init__(self) # , sk.Texture(tile.color))
        self.alpha = 0.2
        self.color = tile.tile_color
        self.name = tile.fen_loc  # as_chess
        # invert y because board goes top to bottom but
        #                     sk goes bottom to top
        half_ss = square_size / 2
        self.position = (tile.x * square_size + half_ss,
                   (7 - tile.y) * square_size + half_ss)
        self.size = tile_Size

    def __contains__(self, touch_or_point):  # if touch in sk_BoardSquare
        try:
            return self.frame.contains_point(touch_or_point.location)
        except AttributeError:
            return self.frame.contains_point(touch_or_point)


class sk_ChessPiece(sk.SpriteNode):
    def __init__(self, piece):
        assert piece and isinstance(piece, ChessPiece)
        sk.SpriteNode.__init__(self, sk.Texture(C.image_path_fmt.format(piece.name)))
        self.alpha = 0.5
        self.piece = piece
        self.size = piece_Size
        self.touch_enabled = True

    @property
    def fen_loc(self):
        return self.piece.fen_loc

    @property
    def name(self):
        return self.piece.name

    def move(self, target):
        assert C.is_valid_fen_loc(target)
        try:
            return self.piece.board.move(self.piece.fen_loc + target)
        except (ChessError, InvalidMove, LogicError) as e:
            dialogs.hud_alert('{}: {}'.format(e.__class__.__name__, e))
        return False


class SkChessBoardScene(sk.Scene):
    def __init__(self, game, frame):
        sk.Scene.__init__(self)
        self.game = game
        self.alpha = 0.2  # highly transparent
        #self.frame = frame
        self.save_position = None
        self.board_tiles_dict = self.create_board_tiles_dict()
        for tile in self.tiles:
            self.add_child(tile)
        self.pieces = self.create_pieces_list()

    @property
    def name(self):
        return game.name

    @property
    def tiles(self):
        return self.board_tiles_dict.itervalues()

    def create_board_tiles_dict(self):
        # return a dictionary of {Phantom.core.coord.point.Coord :
        #                          sk_BoardSquare} entries
        # useful for node hit-testing, greatly simplifies touch_began
        return {tile.fen_loc : sk_BoardSquare(tile)
                for tile in self.game.board.tiles}

    def create_pieces_list(self):
        def make_and_place_piece(piece):
            gui_piece = sk_ChessPiece(piece)
            gui_piece.position = self.board_tiles_dict[piece.fen_loc].position
            gui_piece.prev_position = gui_piece.position
            self.add_child(gui_piece)
            return gui_piece
        return [make_and_place_piece(piece) for piece
                in self.game.board.get_piece_list()]

    def create_board_tiles_dict(self):
        # return a dictionary of {Phantom.core.coord.point.Coord :
        #                          sk_BoardSquare} entries
        # useful for node hit-testing, greatly simplifies touch_began
        return {tile.fen_loc : sk_BoardSquare(tile)
                for tile in self.game.board.tiles}

    def did_change_size(self, old_size):
        print('did_change_size: {} --> {}'.format(old_size, self.size))
        #w, h = ui.get_screen_size()
        global square_size  #, half_ss, tile_Size, piece_Size
        w, h = self.size
        square_size = min(w, h) / 8
        #half_ss = square_size / 2
        tile_Size = sk.Size(square_size, square_size)
        piece_Size = sk.Size(square_size - 2, square_size - 2)
        for node in self.get_children_with_name('*'):
            if isinstance(node, sk_BoardSquare):
                node.size = tile_Size
            elif isinstance(node, sk_ChessPiece):
                node.size = piece_Size
            else:
                print(node)

    def update(self):
        pass

    def touch_began(self, node, touch):
        if node == self:
            return
        self.save_position = node.position

    def touch_moved(self, node, touch):
        if node == self:
            return
        node.position = touch.location

    def touch_ended(self, node, touch):
        if node == self:
            return
        for square in self.get_children_with_name('*'):
            #print(square.name)
            if isinstance(square, sk_BoardSquare) and touch in square:
                target_fen_loc = square.name
                save_fen_loc = node.fen_loc
                #node.move() is called on a different thread so it returns None!!!
                move_was_made = node.move(target_fen_loc) # always returns None!!
                #print('mwm 1', move_was_made)  # fails!!
                move_was_made = node.fen_loc != save_fen_loc
                #print('mwm 2', move_was_made)
                if move_was_made:
                    for piece in self.get_children_with_name('*'):
                        # remove the killed sk_ChessPiece
                        if (piece != node
                        and isinstance(piece, sk_ChessPiece)
                        and piece.fen_loc == node.fen_loc):
                            if piece.piece.ptype == 'king':
                                import dialogs
                                dialogs.hud_alert('Game over man!')
                            piece.remove_from_parent()
                    #import dialogs
                    #dialogs.hud_alert(str(type(self.view.superview)))
                    self.view.superview.update_view(node.piece)
                    node.position = square.position
                    sound.play_effect('8ve:8ve-tap-professional')
                else:
                    node.position = self.save_position
                    sound.play_effect('8ve:8ve-beep-rejected')
                not_str = '' if move_was_made else 'not '
                fmt = '{} at {} was {}moved to square {}\n'
                print(fmt.format(node.name, save_fen_loc, not_str, square.name))


if __name__ == '__main__':
    print('=' * 30)
    from SkChessView import SkChessView
    SkChessView()
