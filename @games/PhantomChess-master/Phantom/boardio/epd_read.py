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

"""Read Extended Position Description (EPD) notation.

Syntax:

    <EPD> ::=   <Piece Placement>
           ' ' <Side to move>
           ' ' <Castling ability>
           ' ' <En passant target square>
          {' ' <operation>}

    <Piece Placement> ::= equal to FEN piece placement

    <Side to move> ::= equal to FEN side to move

    <Castling ability> ::= equal to FEN castling ability

    <En passant target square> ::= equal to FEN en passant target square

    <operation> ::= <opcode> {' '<operand>} ';'
    <opcode>    ::= <letter> {<letter> | <digit> | '_'} (up to 14)
    <operand>   ::= <stringOperand>
                  | <sanMove>
                  | <unsignedOperand>
                  | <ingegerOperand>
                  | <floatOperand>
    <stringOperand> ::= '"' {<char>} '"'
    <sanMove>   ::= <PieceCode> [<Disambiguation>] <targetSquare> [<promotion>] ['+'|'#']
                  | <castles>
    <castles>   ::= 'O-O' | 'O-O-O'
    <PieceCode> ::= '' | 'N' | 'B' | 'R' | 'Q' | 'K'|
    <Disambiguation> ::= <fileLetter> | <digit18>
    <targetSquare> ::= <fileLetter> <digit18>
    <fileLetter> ::= letter a-h
    <promotion> ::= '=' <PiecePromotion>
    <PiecePromotion> ::= 'N' | 'B' | 'R' | 'Q'
    <unsignedOperand> ::= <digit19> { <digit> } | '0'
    <integerOperand> ::= ['-' | '+'] <unsignedIntegerOperand>
    <floatOperand> ::= <integerOperand> '.' <digit> {<digit>}
    <digit18>   ::= An integer in range(1, 9)
    <digit19>   ::= An integer in range(1, 10)
    <digit>     ::= '0' | <digit19>

Opcode mneumonics:

    Mneumonic      | Meaning
    ---------------+-----------------------------------------------
    acn            | analysis count nodes
    acs            | analysis count seconds
    am             | avoid move(s)
    bm             | best move(s)
    c0             | comment (primary, also c1 - c9)
    ce             | centipawn evaluation
    dm             | direct mate fullmove count
    draw_accept    | accept a draw offer
    draw_claim     | claim a draw
    draw_offer     | offer a draw
    draw_reject    | reject a draw
    eco            | Encyclopedia of Chess Openings opening code
    fmvn           | fullmove number
    hmvc           | halfmove clock
    id             | position identification
    nic            | _New In Chess_ opening code
    noop           | no operation (equivalent of 'pass' in Python)
    pm             | predicted move
    pv             | predcted variation
    rc             | repetition count
    resign         | game resignation
    sm             | supplied move
    tcgs           | telecommunication game selector
    tcri           | telecommunication receiver identification
    tcsi           | telecommunication sender identification
    v0             | variation (primary, also v1 - v9)
"""

from Phantom.core.board import Board
from Phantom.constants import default_halfmove, default_fullmove, save_epd, phantom_dir
import os

opcodes = {
'acn'         : 'analysis count nodes',
'acs'         : 'analysis count seconds',
'am'          : 'avoid move(s)',
'bm'          : 'best move(s)',
'ce'          : 'centipawn evaluation',
'dm'          : 'direct mate fullmove count',
'draw_accept' : 'accept a draw',
'draw_claim'  : 'claim a draw',
'draw_offer'  : 'offer a draw',
'draw_reject' : 'reject a draw',
'eco'         : 'ECO code',
'fmvn'        : 'fullmove number',
'hmvc'        : 'halfmove clock',
'id'          : 'positition identification',
'nic'         : 'NIC code',
'noop'        : 'no operation',
'pm'          : 'predicted move',
'pv'          : 'predcted variation',
'rc'          : 'repetiton count',
'resign'      : 'resign from game',
'sm'          : 'supplied move',
'tcgs'        : 'telecommunication game selector',
'tcri'        : 'telecommunication reciever identification',
'tcsi'        : 'telecommunication sender identification'}

def valid_lines_from_file(file_path):
    with open(file_path) as in_file:
        return [line.strip() for line in in_file.readlines()
                if line.strip() and line.strip()[0] != '#']

def _load_name(name):
    ret = None
    file_path = os.path.join(phantom_dir, 'boardio', save_epd)
    for line in valid_lines_from_file(file_path):
        lname, _, val = line.partition(':')
        if lname.strip() == name:
                    ret = val.strip()
    return ret

def list_games():
    file_path = os.path.join(phantom_dir, 'boardio', save_epd)
    return [line.partition(':')[0].strip() for line in valid_lines_from_file(file_path)]

def load_epd(string):
    """Load an EPD from a string and return a board with namespace variables set accordingly."""
    halfmove = str(default_halfmove)
    fullmove = str(default_fullmove)
    fields = string.split()
    layout, moving, castling_rights, en_passant_rights = fields[:4]
    operations = ' '.join(fields[4:])
    op_fields = operations.split(';')[:-1]  # remove last '' element
    fen = ' '.join([layout, moving, castling_rights, en_passant_rights, halfmove, fullmove])
    b = Board(None, fen)
    b.data['raw_operations'] = operations
    b.data['op_fields'] = op_fields
    op_data = {}
    for operation in op_fields:
        fields = operation.strip().split()
        opcode = fields[0]
        operand = fields[1:]
        name = opcodes[opcode]
        value = ''.join([o for o in operand])  # operand will be a list, make into a single object
        op_data.update({opcode: (name, value)})
    b.data['op_data'] = op_data
    if 'fmvn' in op_data:
        b.fullmove_clock = int(op_data['fmvn'][1])
    if 'hmvc' in op_data:
        b.halfmove_clock = int(op_data['hmvc'][1])
    return b

def load_test_string(name):
    from Phantom.constants import test_suite
    file_path = os.path.join(phantom_dir, 'boardio', test_suite)
    for line in valid_lines_from_file(file_path):
        lname, _, val = line.partition(':')
        if lname.strip() == name:
            return val.strip()

def load_test(name):
    """Load a test from the self-test suite."""
    return load_epd(load_test_string(name))

def list_tests():
    from Phantom.constants import test_suite
    file_path = os.path.join(phantom_dir, 'boardio', test_suite)
    return [line.partition(':')[0].strip() for line in valid_lines_from_file(file_path)]
