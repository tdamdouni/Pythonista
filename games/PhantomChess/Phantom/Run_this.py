#!/usr/bin/env python
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

"""To start a new game, simply run this file."""

from Phantom.core.game_class import ChessGame
from Phantom.docs.documentation import program_use
from Phantom.utils.lic import license
from Phantom.boardio.epd_read import load_test

game = ChessGame()
print("""PhantomChess Copyright (C) 2015 671620616
This program comes with ABSOLUTELY NO WARRANTY; for details enter 'license'
This is free software, and you are welcome to redistribute it
under certain conditions; type 'license' for details.

Your game can be displayed by typing 'game'
To move, type 'e2e4' or similar.
To execute a function, simply type the function as you normally would.
To exit, type 'quit' or close the program.
For a full list of commands, type 'help'.""")

print(game)

if __name__ == '__main__':
    import re
    move_re = coord_re = valid_filename_re = None  # will be created just in time
    help_str = """
    quit                  Exit the program
    exit                  Exit the program
    e2e4                  Move a piece from e2 to e4
    e2                    Get information about the piece at e2
    game                  Show the current layout of the game
    save xxxxxxx          Save the game under the name xxxxxxx
    load xxxxxxx          Load the game named xxxxxxx
    saves                 Get a list of all saved games
    gui                   Activate a GUI (Pythonista)
    sk                    Activate a sk GUI (Pythonista)
    quit                  Exit the game
    help                  Show this help text
    reset                 Reset the game to the opening position
    license               Show license information (it's a long read)
    castle x              Castle on the side 'x' - x can be:
                            K - white kingside
                            Q - white queenside
                            k - black kingside
                            q - black queenside
    promote aa b          Promote the pawn at aa to type b - b can be:
                            Q - queen
                            R - rook
                            N - knight
                            B - bishop

    ===== AI commands =====
        Prefix all commands listed below with "ai "
        Example: "ai rate"

        easy              Make a random move
        hard              Make a smart move
        rate              Get an integer representing the positional score of the board
    """.encode('utf-8')

    def is_cmd(pattern, user):
        finds = pattern.findall(user)
        return finds and finds[0] == user

    def is_valid_filename(filename):
        global valid_filename_re
        valid_filename_re = valid_filename_re or re.compile(r'[a-zA-Z0-9_\x20]+')  # just in time
        return is_cmd(valid_filename_re, filename)

    def ai_command(command):
        if command == 'easy':
            game.ai_easy()
            return game
        elif command == 'hard':
            game.ai_hard()
            return game
        elif command == 'rate':
            return game.ai_rateing
        else:
            return 'Valid "ai" commands are "easy", "hard", and "rate".'

    def is_text_command(user_in):
        global game, valid_filename_re
        cmd_parts = user_in.split()
        if not cmd_parts:
            return False
        cmd = cmd_parts[0].lower()
        if not cmd in 'ai castle game gui help license load promote reset save saves sk'.split():
            return False  # fast fail
        modifier = cmd_parts[1] if len(cmd_parts) > 1 else ''  # some commands require a modifier
        if cmd == 'ai':
            print(str(ai_command(modifier.lower())))
        elif cmd == 'castle':
            if modifier in 'KQkq':
                game.castle(modifier)
            else:
                print('"castle" must be followed by "K", "Q", "k", or "q".')
        elif cmd == 'game':
            print(game)
        elif cmd == 'gui':
            game.scene_gui()
        elif cmd == 'help':
            print(help_str)
        elif cmd == 'license':
            print(license())
        elif cmd == 'load':
            filename = ' '.join(cmd_parts[1:])
            if is_valid_filename(filename):
                from Phantom.core.game_class import load_game
                game = load_game(filename)
                print(game)
            else:
                print(filename + ' is not a valid filename.')
        elif cmd == 'promote':
            game.promote(cmd_parts[1], cmd_parts[2])
        elif cmd == 'reset':
            game = ChessGame()
            print(game)
        elif cmd == 'save':
            filename = ' '.join(cmd_parts[1:])
            if is_valid_filename(filename):
                game.board.save(filename)
            else:
                print(filename + ' is not a valid filename.')
        elif cmd == 'saves':
            from Phantom.boardio.load import list_games
            print('\n'.join('{:>3} {}'.format(i+1, game_name)
                       for i, game_name in enumerate(sorted(list_games()))))
        elif cmd == 'sk':
            game.sk_gui()
        else:
            assert False, 'This should never happen.'
        return True

    running = True
    while running:
        user_in = raw_input(':> ').strip()
        if not user_in:
            continue
        if user_in.split()[0].lower() in ('quit', 'exit'):
            running = False
        elif '(' in user_in and ')' in user_in:
            # assume a function was called
            exec user_in  # 671: remove exec somehow?
        elif not is_text_command(user_in):
            coord_re = coord_re or re.compile(r'[a-h][1-8]')  # just in time
            if is_cmd(coord_re, user_in):
                print("\tGetting information for {}...".format(user_in))
                pos = Coord.from_chess(user_in)
                piece = game.board[pos]
                print(piece.as_str() if piece else '\tNo piece at {}'.format(user_in))
            else:
                # assume a move, like "e2e4"
                move_re = move_re or re.compile(r'[a-h][1-8][a-h][1-8]')  # just in time
                if is_cmd(move_re, user_in):
                    # is definitely a move
                    game.move(user_in)
                    print(game)
