# https://github.com/cclauss/Ten-lines-or-less/blob/master/sudoku_revisited.py

from random import sample


def random_board(cells=9):
    return [sample(range(1, cells + 1), cells) for i in range(cells)]


def board_format(board):
    s = '\n' + '| '.join(['- '] * 9) + '\n'
    b = s.replace('|', '-')
    return b + s.join(' | '.join(str(y) for y in x) for x in board) + b

print(board_format(random_board()))
