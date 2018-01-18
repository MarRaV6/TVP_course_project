import sys

from .lexer import Lexer


class Node:
    def __init__(self, kind, value=None, op1=None, op2=None, op3=None):
        self.kind = kind
        self.value = value
        self.op1 = op1
        self.op2 = op2
        self.op3 = op3

    def __repr__(self):
        return "Node({}, {})".format(self.kind, self.value)

    __str__ = __repr__


class Parser:
    VAR, CONST, ADD, SUB, LT, SET, IF1, IF2, WHILE, DO, EMPTY, SEQ, EXPR, PROG, PRINT = range(15)

    def __init__(self, lexer):
        self.lexer = lexer

    def error(self, msg):
        print('Parser error:', msg)
        sys.exit(1)

    def term(self):
        if self.lexer.sym == Lexer.ID:
            n = Node(Parser.VAR, self.lexer.value)
            self.lexer.next_token()
            return n
        elif self.lexer.sym == Lexer.NUM:
            n = Node(Parser.CONST, self.lexer.value)
            self.lexer.next_token()
            return n
        else:
            return self.paren_expr()

    def summa(self):
        n = self.term()
        while self.lexer.sym == Lexer.PLUS or self.lexer.sym == Lexer.MINUS:
            if self.lexer.sym == Lexer.PLUS:
                kind = Parser.ADD
            else:
                kind = Parser.SUB
            self.lexer.next_token()
            n = Node(kind, op1=n, op2=self.term())
        return n

    def test(self):
        n = self.summa()
        if self.lexer.sym == Lexer.LESS:
            self.lexer.next_token()
            n = Node(Parser.LT, op1=n, op2=self.summa())
        return n

    def expr(self):
        if self.lexer.sym != Lexer.ID:
            return self.test()
        n = self.test()
        if n.kind == Parser.VAR and self.lexer.sym == Lexer.EQUAL:
            self.lexer.next_token()
            n = Node(Parser.SET, op1=n, op2=self.expr())
        return n

    def paren_expr(self):
        if self.lexer.sym != Lexer.LPAR:
            self.error('"(" expected')
        self.lexer.next_token()
        n = self.expr()
        if self.lexer.sym != Lexer.RPAR:
            self.error('")" expected')
        self.lexer.next_token()
        return n

    def statement(self):
        """
        Разбор выражения, вернет узел или None
        :return:
        """
        if self.lexer.sym == Lexer.IF:
            n = Node(Parser.IF1)
            self.lexer.next_token()
            n.op1 = self.paren_expr()
            n.op2 = self.statement()
            if self.lexer.sym == Lexer.ELSE:
                n.kind = Parser.IF2
                self.lexer.next_token()
                n.op3 = self.statement()

        elif self.lexer.sym == Lexer.WHILE:
            n = Node(Parser.WHILE)
            self.lexer.next_token()
            n.op1 = self.paren_expr()
            n.op2 = self.statement()

        elif self.lexer.sym == Lexer.DO:
            n = Node(Parser.DO)
            self.lexer.next_token()
            n.op1 = self.statement()
            if self.lexer.sym != Lexer.WHILE:
                self.error('"while" expected')
            self.lexer.next_token()
            n.op2 = self.paren_expr()
            if self.lexer.sym != Lexer.SEMICOLON:
                self.error('";" expected')

        elif self.lexer.sym == Lexer.SEMICOLON:
            n = Node(Parser.EMPTY)
            self.lexer.next_token()

        elif self.lexer.sym == Lexer.LBRA:
            n = Node(Parser.EMPTY)
            self.lexer.next_token()
            while self.lexer.sym != Lexer.RBRA:
                n = Node(Parser.SEQ, op1=n, op2=self.statement())
            self.lexer.next_token()

        elif self.lexer.sym == Lexer.PRINT:
            n = Node(Parser.PRINT)
            self.lexer.next_token()
            n.op1 = self.paren_expr()

        else:
            n = Node(Parser.EXPR, op1=self.expr())
            if self.lexer.sym != Lexer.SEMICOLON:
                self.error('";" expected')
            self.lexer.next_token()

        return n

    def parse(self):
        """
        Парсинг программы
        :return: дерево разбора
        """
        self.lexer.next_token()
        node = Node(Parser.PROG, op1=self.statement())
        if (self.lexer.sym != Lexer.EOF):
            self.error("Invalid statement syntax")
        return node
