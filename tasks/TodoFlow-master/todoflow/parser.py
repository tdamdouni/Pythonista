from __future__ import absolute_import

from .lexer import Lexer
from .todos import Todos, Node
from .todoitem import Todoitem


class TodolistParserError(Exception):
    pass


class Parser(object):
    def __init__(self):
        self.newlines = []
        self.parsed_items = []
        self.items_in_parsing = []

    def parse(self, text):
        self.lexer = Lexer(text)
        new_item = None
        for token in self.lexer.tokens:
            if token.is_newline:
                self.newlines.append(Node(Todoitem.from_token(token)))
            elif token.is_text:
                new_item = self._handle_text(token)
            elif token.is_indent:
                self.items_in_parsing.append(new_item)
            elif token.is_dedent:
                self.items_in_parsing.pop()
            elif token.is_end:
                return self._handle_end()

    def _handle_text(self, token):
        new_item = Node(Todoitem.from_token(token))
        if self.items_in_parsing:
            for nl in self.newlines:
                self.items_in_parsing[-1].append_child(nl)
            self.newlines = []
            try:
                self.items_in_parsing[-1].append_child(new_item)
            except AttributeError:
                raise TodolistParserError('Error in parsing: {}'.format(self.items_in_parsing))
        else:
            self.parsed_items += self.newlines
            self.newlines = []
            self.parsed_items.append(new_item)
        return new_item

    def _handle_end(self):
        todos = Todos(Node(children=self.parsed_items + self.newlines))
        return todos


def parse(text):
    return Parser().parse(text)
