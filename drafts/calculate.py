# coding: utf-8

# To call script from Drafts, use the follwing URL as URL Action:
# <pythonista://calculate.py?action=run&argv=[[draft]]>

# https://gist.github.com/hiilppp/7822439

# Python script to calculate arithmetic expressions in Pythonista and send them, along with their results, (back) to Drafts.

# Except for the last ten lines, this script was written by Erez Shinan, see <http://erezsh.wordpress.com/2013/02/24/how-to-write-a-calculator-in-70-python-lines-by-writing-a-recursive-descent-parser/>.

'''A Calculator Implemented With A Top-Down, Recursive-Descent Parser'''
# Author: Erez Shinan, Dec 2012

import re, collections, sys
from operator import add,sub,mul,div

Token = collections.namedtuple('Token', ['name', 'value'])
RuleMatch = collections.namedtuple('RuleMatch', ['name', 'matched'])

token_map = {'+':'ADD', '-':'ADD', '*':'MUL', '/':'MUL', '(':'LPAR', ')':'RPAR'}
rule_map = {
    'add' : ['mul ADD add', 'mul'],
    'mul' : ['atom MUL mul', 'atom'],
    'atom': ['NUM', 'LPAR add RPAR', 'neg'],
    'neg' : ['ADD atom'],
}
fix_assoc_rules = 'add', 'mul'

bin_calc_map = {'*':mul, '/':div, '+':add, '-':sub}
def calc_binary(x):
    while len(x) > 1:
        x[:3] = [ bin_calc_map[x[1]](x[0], x[2]) ]
    return x[0]

calc_map = {
    'NUM' : float,
    'atom': lambda x: x[len(x)!=1],
    'neg' : lambda (op,num): (num,-num)[op=='-'],
    'mul' : calc_binary,
    'add' : calc_binary,
}

def match(rule_name, tokens):
    if tokens and rule_name == tokens[0].name:      # Match a token?
        return tokens[0], tokens[1:]
    for expansion in rule_map.get(rule_name, ()):   # Match a rule?
        remaining_tokens = tokens
        matched_subrules = []
        for subrule in expansion.split():
            matched, remaining_tokens = match(subrule, remaining_tokens)
            if not matched:
                break   # no such luck. next expansion!
            matched_subrules.append(matched)
        else:
            return RuleMatch(rule_name, matched_subrules), remaining_tokens
    return None, None   # match not found

def _recurse_tree(tree, func):
    return map(func, tree.matched) if tree.name in rule_map else tree[1]

def flatten_right_associativity(tree):
    new = _recurse_tree(tree, flatten_right_associativity)
    if tree.name in fix_assoc_rules and len(new)==3 and new[2].name==tree.name:
        new[-1:] = new[-1].matched
    return RuleMatch(tree.name, new)

def evaluate(tree):
    solutions = _recurse_tree(tree, evaluate)
    return calc_map.get(tree.name, lambda x:x)(solutions)

def calc(expr):
    split_expr = re.findall('[\d.]+|[%s]' % ''.join(token_map), expr)
    tokens = [Token(token_map.get(x, 'NUM'), x) for x in split_expr]
    tree = match('add', tokens)[0]
    tree = flatten_right_associativity( tree )
    return evaluate(tree)

# if __name__ == '__main__':
#    while True:
#        print( calc(raw_input('> ')) )

import urllib
import webbrowser

a = re.sub(r"\s+", "", sys.argv[1])
b = str(calc(a))
a = re.sub(r"([+*-])(-?[^ +*-]+)", " \\1 \\2", a)
b = re.sub(r"\.0$", "", b)
c = a + " = " + b

webbrowser.open("drafts4://x-callback-url/create?text=" + urllib.quote(c))