from __future__ import absolute_import

from .textutils import calculate_indent_level


class Token(object):
    token_ids = {
        'text': '*',
        'newline': 'n',
        'indent': '>',
        'dedent': '<',
        'end': '$',
    }

    def __init__(self, linenum):
        self.linenum = linenum

    def __getattr__(self, attr_name):
        try:
            return self.token_ids[attr_name.split('_')[-1]] == self.tok()
        except KeyError:
            raise AttributeError


class NewlineToken(Token):
    def tok(self):
        return self.token_ids['newline']

    def __init__(self, linenum, start):
        super(NewlineToken, self).__init__(linenum)
        self.start = start
        self.end = start


class IndentToken(Token):
    def tok(self):
        return self.token_ids['indent']


class DedentToken(Token):
    def tok(self):
        return self.token_ids['dedent']


class TextToken(Token):
    def __init__(self, text, linenum, start):
        super(TextToken, self).__init__(linenum)
        self.text = text
        self.start = start
        self.end = start + len(text)

    def tok(self):
        return self.token_ids['text']


class EndToken(Token):
    def tok(self):
        return self.token_ids['end']


class Lexer(object):
    def __init__(self, text):
        self.text = text
        self.lines = text.splitlines()
        if text.endswith('\n'):
            self.lines.append('')
        self._tokenize()

    def _tokenize(self):
        self.tokens = []
        self.indent_levels = [0]
        linenum = 0
        char_index = 0
        for linenum, line in enumerate(self.lines):
            if line:
                self._handle_indentation(line, linenum)
                self.tokens.append(TextToken(line, linenum, char_index))
            else:
                self.tokens.append(NewlineToken(linenum, char_index))
            char_index += len(line) + 1
        self.tokens.append(EndToken(linenum + 1))

    def _handle_indentation(self, line, linenum):
        indent_levels = self.indent_levels
        current_level = calculate_indent_level(line)
        if current_level > indent_levels[-1]:
            indent_levels.append(current_level)
            self.tokens.append(IndentToken(linenum))
        elif current_level < indent_levels[-1]:
            while current_level < indent_levels[-1]:
                indent_levels.pop()
                self.tokens.append(DedentToken(linenum))
