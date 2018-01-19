import sys

from .token import Token


class Lexer:

    SYMBOLS = {'{': Token.LBRA, '}': Token.RBRA, '=': Token.EQUAL, ';': Token.SEMICOLON, '(': Token.LPAR,
               ')': Token.RPAR, '+': Token.PLUS, '-': Token.MINUS, '*': Token.MULTI, '<': Token.LESS, '>': Token.MORE, '~': Token.CMPR}

    WORDS = {'if': Token.IF, 'else': Token.ELSE, 'do': Token.DO, 'while': Token.WHILE, 'print': Token.PRINT}

    def __init__(self, program_text):
        self.program_text = program_text
        self.cur = 0
        self.ch = ' '
        self.value = None
        self.sym = None

    def error(self, msg):
        print('Lexer error: ', msg)
        sys.exit(1)

    def getc(self):
        try:
            self.ch = self.program_text[self.cur]
            self.cur += 1
        except IndexError:
            self.ch = ''

    def next_token(self):
        self.value = None
        self.sym = None
        while self.sym is None:
            if len(self.ch) == 0:
                self.sym = Token.EOF

            elif self.ch.isspace():
                self.getc()

            elif self.ch in Lexer.SYMBOLS:
                self.sym = Lexer.SYMBOLS[self.ch]
                self.getc()

            elif self.ch.isdigit() or (self.ch == '0'):
                intval = 0
                before_point = 0.0
                flag = True
                i = 1
                while self.ch.isdigit() or (self.ch == '.') or (self.ch == '0'):
                    if self.ch == '.':
                        flag = False
                        self.getc()
                    else:
                        if flag:
                            intval = intval * 10 + int(self.ch)
                            self.getc()
                        else:
                            before_point = before_point + (0.1 ** i) * int(self.ch)
                            i += 1
                            self.getc()
                if flag:
                    self.value = intval
                else:
                    self.value = intval + before_point
                self.sym = Token.NUM

            elif self.ch.isalpha():
                ident = ''
                while self.ch.isalpha():
                    ident = ident + self.ch.lower()
                    self.getc()

                if ident in Lexer.WORDS:
                    self.sym = Lexer.WORDS[ident]

                # если после последовательности букв осталась одна, это переменная
                elif len(ident) == 1:
                    self.sym = Token.ID
                    self.value = ord(ident) - ord('a')

                else:
                    self.error('Unknown identifier: ' + ident) #TODO добавть возможность ввода многосимвольного имени переменной
            else:
                self.error('Unexpected symbol: ' + self.ch)
