# coding: utf-8

# Set HUMAN_WANTS_TO_PLAY to True to try to beat the computer
# Set HUMAN_WANTS_TO_PLAY to False to have the computer play against itself

HUMAN_WANTS_TO_PLAY = False

'''
    http://en.m.wikipedia.org/wiki/Tic-tac-toe#Strategy
    
    'X' or 'O') Win
    'Draw')     Draw
    6) Block
    5) Fork
    4) Blocking an opponent's fork
    3) Center
    2) Opposite corner
    1) Empty corner
    0) Empty side
'''

import collections, console, random, time, ui

def change_char(s='spring', i=1, c='t'):  # convert 'spring' to 'string'
    return s[:i] + c + s[i+1:]

def opponent(player):
    return 'O' if player == 'X' else 'X'

class TTT_Board(object):
    # class variables:
    board_center  = 4
    board_corners = [0, 2, 6, 8]
    board_edges   = [1, 3, 5, 7]
    images = { 'X' : ui.Image.named('ionicons-close-256'),
               'O' : ui.Image.named('ionicons-ios7-circle-outline-256') }
    # ways_to_win is a list of indexes for the eight ways to win
    ways_to_win = '012 345 678 036 147 258 048 246'.split()
    ways_to_win = [[int(x) for x in y] for y in ways_to_win]
    
    def __init__(self, view):
        self.view = view
        self.board = ' ' * 9
        self.curr_player = 'X'

    def __str__(self):
        template = ''.join([' ' if c in 'XO' else str(i)
                            for i, c in enumerate(self.board)])
        suffix = ', '.join([x for x in template if x != ' '])
        suffix = '\n' + 'Available squares: ' + suffix if suffix else 'No available squares.'
        s = ''
        for row in xrange(3):
            if row:
                s += '\n{}  -  {}\n'.format('-' * 9, '-' * 9)
            s += '{}  -  {}'.format(
                ' | '.join([self.board[row*3+col] for col in xrange(3)]),
                ' | '.join([template[row*3+col]   for col in xrange(3)]))
        return s + suffix

    def switch_players(self):
        self.curr_player = opponent(self.curr_player)

    def clear_board(self):
        self.board = ' ' * 9
        self.view.update_board()

    def board_is_empty(self):
        return self.board.strip() == ''

    def board_is_full(self):
        return not ' ' in self.board

    def set_square(self, square=4):
        assert 0 <= square <= 8, '{} is an invalid square.'.format(square)
        assert self.board[square] == ' ', '{} is occupied.'.format(square)
        self.board = change_char(self.board, square, self.curr_player)
        self.view.update_board()

    def is_game_over(self):  # returns: 'X' or 'O' or 'Draw' or None
        ttt = [''.join([self.board[x] for x in y]) for y in self.ways_to_win]
        for player in 'XO':
            if player * 3 in ttt:  # 'XXX' or 'OOO'
                msg = 'Player {} wins!'.format(player)
                print(msg + '\n' + '#' * 20)
                console.hud_alert(msg)
                return player  # player has won the game
        if self.board_is_full():
            msg = 'Game ends in a draw.'
            print(msg + '\n' + '#' * 20)
            console.hud_alert(msg)
            return 'Draw'      # the game ends in a draw
        return None

    def take_a_turn(self):
        print(self)
        game_status = self.get_analysis()
        print('get_analysis({}) --> {}'.format(self.curr_player, game_status))
        if isinstance(game_status[0], int):
            self.set_square(game_status[0])

    def find_fork(self):
        # Option 1: diagonal == opponent, self, opponent and "L" to right or left all blank
        cp = self.curr_player
        op = opponent(cp)
        if self.board[self.board_center] == cp:  # if curr_player is in center square
            if all([self.board[i] == op for i in (0, 8)]):
                if all([self.board[i] == ' ' for i in (1, 2, 5)]):
                    return random.choice((1, 5)), 'Block fork (special)'
                elif all([self.board[i] == ' ' for i in (3, 6, 7)]):
                    return random.choice((3, 7)), 'Block fork (special)'
            elif all([self.board[i] == op for i in (2, 6)]):
                if all([self.board[i] == ' ' for i in (0, 1, 3)]):
                    return random.choice((1, 3)), 'Block fork (special)'
                elif all([self.board[i] == ' ' for i in (5, 7, 8)]):
                    return random.choice((5, 7)), 'Block fork (special)'
        # Option 2:
        ttt = [''.join([self.board[x] for x in y]) for y in self.ways_to_win]
        # look for a winning move or block opponent's winning move
        forker     = ' ' * 2 + cp
        block_fork = ' ' * 2 + op
        sorted_ttt = [''.join(sorted(t)) for t in ttt]
        for fork_or_block_fork in (forker, block_fork):
            indexes = []
            for i, t in enumerate(sorted_ttt):
                if t == fork_or_block_fork:
                    indexes += [x for x in self.ways_to_win[i] if self.board[x] == ' ']
            if indexes:
                index, count = collections.Counter(indexes).most_common(1)[0]
                if count > 1:
                    return index, 'Fork' if fork_or_block_fork.strip() == cp else 'Block fork'
        
    def get_analysis(self):
        # first move on an empty board
        if self.board_is_empty():
            return random.choice(self.board_corners), 'Initial move'
        # look for a winner or a draw
        game_over = self.is_game_over()
        if game_over:  # 'Draw' or 'X' or 'O' or None
            return game_over, ('Draw.' if game_over == 'Draw' else 'Winner!')
        # look for a winning move or block opponent's winning move
        winner = ' ' + self.curr_player * 2
        loser  = ' ' + opponent(self.curr_player) * 2
        ttt = [''.join([self.board[x] for x in y]) for y in self.ways_to_win]
        sorted_ttt = [''.join(sorted(t)) for t in ttt]
        for win_or_lose in (winner, loser):
            try:
                win_index = sorted_ttt.index(win_or_lose)
                indexes = self.ways_to_win[win_index]
                for i in indexes:
                    if self.board[i] == ' ':
                        return i, 'Win' if win_or_lose == winner else 'Block'
                assert False, 'No winner/loser in {}!!'.format(indexes)
            except ValueError:
                pass
        # look for a fork or block opponent's fork
        ff = self.find_fork()
        if ff:
            return ff
        # ...
        # board center
        if self.board[self.board_center] == ' ':
            return self.board_center, 'Center'
        # opposite corner
        for i, c in enumerate(self.board_corners):
            opposite_corner = list(reversed(self.board_corners))[i]
            if (self.board[c] == opponent(self.curr_player)
            and self.board[opposite_corner] == ' '):
                return opposite_corner, 'Opposite corner'
        # empty corner
        bc = self.board_corners[:]  # unique copy
        random.shuffle(bc)
        for i in bc:
            if self.board[i] == ' ':
                return i, 'Corner'
        # board edge
        random.shuffle(self.board_edges)
        for i in self.board_edges:
            if self.board[i] == ' ':
                return i, 'Edge'

class TicTacToeView(ui.View):
    def __init__(self):
        self.board = TTT_Board(self)
        self.present('sheet')
        self.squares = [self.make_square(i) for i in xrange(9)]

    def make_square(self, index):
        square = ui.Button(name='Square {}'.format(index))
        square.action       = self.square_tapped
        square.bg_color     = 'ivory'
        square.border_width = 2
        square.border_color = 'lightblue'
        x, y = index % 3, index / 3
        w3, h3 = self.width / 3, self.height / 3
        square.frame = x*w3, y*h3, w3, h3
        self.add_subview(square)
        return square

    def update_board(self):
        for i, c in enumerate(self.board.board):
            self.squares[i].image = TTT_Board.images.get(c, None)

    def square_tapped(self, sender):
        self.board.set_square(int(sender.name[-1])) # int(last char of sender's name')
        self.update_board()
        self.board.switch_players()

print('#' * 20)
view = TicTacToeView()
ttt = view.board
games_to_play = 12
human_player = 'X' if HUMAN_WANTS_TO_PLAY else 'Z'
if not HUMAN_WANTS_TO_PLAY:
    console.hud_alert('To play yourself set HUMAN_WANTS_TO_PLAY to True.', 'success', 3)
while view.on_screen and games_to_play:
    if ttt.curr_player == human_player:
        time.sleep(1)
    else:  # computer player
        ttt.take_a_turn()
        ttt.switch_players()
    if ttt.is_game_over():
        ttt.clear_board()
        games_to_play -= 1

if not HUMAN_WANTS_TO_PLAY:
    console.hud_alert('To play yourself set HUMAN_WANTS_TO_PLAY to True.', 'success', 3)
if view.on_screen:
    time.sleep(2)
view.close()
