class Lexer:
    NUM, ID, IF, ELSE, WHILE, DO, LBRA, RBRA, LPAR, RPAR, PLUS, MINUS, LESS, \
    EQUAL, SEMICOLON, EOF, PRINT, MULTI = range(18)

    SYMBOLS = {'{': LBRA, '}': RBRA, '=': EQUAL, ';': SEMICOLON, '(': LPAR,
               ')': RPAR, '+': PLUS, '-': MINUS, '<': LESS, '*': MULTI}

    WORDS = {'if': IF, 'else': ELSE, 'do': DO, 'while': WHILE, 'print': PRINT}

    def __init__(self, program_text):
        self.ptext = program_text
        self.cur = 0
        self.ch = ' '

    def error(self, msg):
        print('Lexer error: ', msg)
        sys.exit(1)

    def getc(self):
        try:
            self.ch = self.ptext[self.cur]
            self.cur += 1
        except IndexError:
            self.ch = ''

    def next_token(self):
        self.value = None
        self.sym = None
        while self.sym is None:
            if len(self.ch) == 0:
                self.sym = Lexer.EOF

            elif self.ch.isspace():
                self.getc()

            elif self.ch in Lexer.SYMBOLS:
                self.sym = Lexer.SYMBOLS[self.ch]
                self.getc()

            elif self.ch.isdigit():
                intval = 0
                while self.ch.isdigit() or (self.ch == '.'):
                    intval = intval * 10 + int(self.ch)
                    self.getc()
                self.value = intval
                self.sym = Lexer.NUM

            elif self.ch.isalpha():
                ident = ''
                while self.ch.isalpha():
                    ident = ident + self.ch.lower()
                    self.getc()

                if ident in Lexer.WORDS:
                    self.sym = Lexer.WORDS[ident]

                # если после последовательности букв осталась одна, это переменная
                elif len(ident) == 1:
                    self.sym = Lexer.ID
                    self.value = ord(ident) - ord('a')

                else:
                    self.error('Unknown identifier: ' + ident) #TODO добавть возможность ввода многосимвольного имени переменной
            else:
                self.error('Unexpected symbol: ' + self.ch)
