# coding: utf-8

# https://github.com/cclauss/Ten-lines-or-less/blob/master/sudoku_print.py

def border_line():
    return ('=' * 7).join('+' * 4)


def get_fmt(i):
    return '{}' if i % 3 else '+ {}'


def sudoku_line(i, line):
    s = '' if i % 3 else border_line() + '\n'
    return s + ' '.join(get_fmt(i).format(x if x != '0' else '_')
                        for i, x in enumerate(line)) + ' +'


def sudoku_board(board):
    return '\n'.join(sudoku_line(i, line) for i, line
                     in enumerate(board.splitlines())) + '\n' + border_line()

board = '''123456789\n234567890\n345678901\n456789012
567890123\n678901234\n789012345\n890123456\n901234567'''

print(sudoku_board(board))
