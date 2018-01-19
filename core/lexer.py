import sys

from core.exceptions import LexerError
from .token import Token


class Lexer:

    SYMBOLS = {'{': Token.LBRA, '}': Token.RBRA, '=': Token.EQUAL, ';': Token.SEMICOLON, '(': Token.LPAR,
               ')': Token.RPAR, '+': Token.PLUS, '-': Token.MINUS, '*': Token.MULTI, '/': Token.SEG, '%': Token.MOD,
               '<': Token.LESS, '>': Token.MORE, '~': Token.CMPR}

    WORDS = {'if': Token.IF, 'else': Token.ELSE, 'do': Token.DO, 'while': Token.WHILE, 'print': Token.PRINT}

    def __init__(self, program_text):
        self._program_text = program_text
        self._current_symbol = 0
        self._ch = ' '
        self._value = None
        self._sym = None

    @property
    def value(self):
        return self._value

    @property
    def sym(self):
        return self._sym

    @property
    def current_symbol(self):
        return self._current_symbol

    @property
    def program_text(self):
        return self._program_text

    def _error(self, msg):
        raise LexerError('Lexer error: {}\nCurrent sym: {}'.format(msg, self._current_symbol))

    def _getc(self):
        try:
            self._ch = self._program_text[self._current_symbol]
            self._current_symbol += 1
        except IndexError:
            self._ch = ''

    def next_token(self):
        self._value = None
        self._sym = None
        while self._sym is None:
            if len(self._ch) == 0:
                self._sym = Token.EOF

            elif self._ch.isspace():
                self._getc()

            elif self._ch in Lexer.SYMBOLS:
                self._sym = Lexer.SYMBOLS[self._ch]
                self._getc()

            elif self._ch.isdigit() or (self._ch == '0'):
                intval = 0
                floatval = 0.0
                find_point = True
                i = 1
                while self._ch.isdigit() or (self._ch == '.') or (self._ch == '0'):
                    if self._ch == '.':
                        find_point = False
                        self._getc()
                    else:
                        if find_point:
                            intval = intval * 10 + int(self._ch)
                        else:
                            floatval = floatval + (0.1 ** i) * int(self._ch)
                            i += 1
                        self._getc()

                self._value = intval if find_point else intval + floatval
                self._sym = Token.NUM

            elif self._ch.isalpha():
                ident = ''
                while self._ch.isalpha():
                    ident = ident + self._ch.lower()
                    self._getc()

                if ident in Lexer.WORDS:
                    self._sym = Lexer.WORDS[ident]

                # если после последовательности букв осталась одна, это переменная
                elif len(ident) == 1:
                    self._sym = Token.ID
                    self._value = ord(ident) - ord('a')

                else:
                    self._error('Unknown identifier: ' + ident)
            else:
                self._error('Unexpected symbol: ' + self._ch)
