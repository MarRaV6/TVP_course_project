from core.exceptions import ParserError
from .lexer import Token, Lexer
from .ast import Node, NodeType


class Parser:
    _MATH_OP = [Token.PLUS, Token.MINUS, Token.MULTI, Token.SEG, Token.MOD]

    def __init__(self, lexer: Lexer):
        self.lexer = lexer

    def _error(self, msg):
        cs = self.lexer.current_symbol
        code_fragment = self.lexer.program_text[0 if cs < 15 else cs-10 : cs+2]
        raise ParserError('Parser error: {}\nFragment: ...\n{}\n...'.format(msg, code_fragment))

    def _term(self):
        """
        Разбор терминальных токенов - константы, переменные
        """
        if self.lexer.sym == Token.ID:
            n = Node(NodeType.VAR, self.lexer.value)
            self.lexer.next_token()
            return n
        elif self.lexer.sym == Token.NUM:
            n = Node(NodeType.CONST, self.lexer.value)
            self.lexer.next_token()
            return n
        else:
            return self._paren_expr()

    def _calculate(self):
        """
        Разбор арифметических выражений
        """
        n = self._term()
        while self.lexer.sym in Parser._MATH_OP:
            if self.lexer.sym == Token.PLUS:
                kind = NodeType.ADD
            elif self.lexer.sym == Token.MINUS:
                kind = NodeType.SUB
            elif self.lexer.sym == Token.MULTI:
                kind = NodeType.MULTI
            elif self.lexer.sym == Token.MOD:
                kind = NodeType.MOD
            else:
                kind = NodeType.SEG
            self.lexer.next_token()
            n = Node(kind, op1=n, op2=self._term())
        return n

    def _test(self):
        """
        Разбор операций сравнения
        """
        n = self._calculate()
        if self.lexer.sym == Token.LESS:
            self.lexer.next_token()
            n = Node(NodeType.LT, op1=n, op2=self._calculate())

        elif self.lexer.sym == Token.MORE:
            self.lexer.next_token()
            n = Node(NodeType.RT, op1=n, op2=self._calculate())

        elif self.lexer.sym == Token.CMPR:
            self.lexer.next_token()
            n = Node(NodeType.CMPR, op1=n, op2=self._calculate())

        return n

    def _expr(self):
        """
        Разбор выражений
        :return:
        """
        if self.lexer.sym != Token.ID:
            return self._test()

        n = self._test()
        if n.kind == NodeType.VAR and self.lexer.sym == Token.EQUAL:
            self.lexer.next_token()
            n = Node(NodeType.SET, op1=n, op2=self._expr())

        return n

    def _paren_expr(self):
        """
        Разбор выражений в скобках
        """
        if self.lexer.sym != Token.LPAR:
            self._error('"(" expected')
        self.lexer.next_token()
        n = self._expr()
        if self.lexer.sym != Token.RPAR:
            self._error('")" expected')
        self.lexer.next_token()
        return n

    def _statement(self):
        """
        Разбор языковой конструкции, цикла, условия, скобок
        """
        if self.lexer.sym == Token.IF:
            n = Node(NodeType.IF1)
            self.lexer.next_token()
            n.op1 = self._paren_expr()
            n.op2 = self._statement()
            if self.lexer.sym == Token.ELSE:
                n.kind = NodeType.IF2
                self.lexer.next_token()
                n.op3 = self._statement()

        elif self.lexer.sym == Token.WHILE:
            n = Node(NodeType.WHILE)
            self.lexer.next_token()
            n.op1 = self._paren_expr()
            n.op2 = self._statement()

        elif self.lexer.sym == Token.DO:
            n = Node(NodeType.DO)
            self.lexer.next_token()
            n.op1 = self._statement()
            if self.lexer.sym != Token.WHILE:
                self._error('"while" expected')
            self.lexer.next_token()
            n.op2 = self._paren_expr()
            if self.lexer.sym != Token.SEMICOLON:
                self._error('";" expected')

        elif self.lexer.sym == Token.SEMICOLON:
            n = Node(NodeType.EMPTY)
            self.lexer.next_token()

        elif self.lexer.sym == Token.LBRA:
            n = Node(NodeType.EMPTY)
            self.lexer.next_token()
            while self.lexer.sym != Token.RBRA:
                n = Node(NodeType.SEQ, op1=n, op2=self._statement())
            self.lexer.next_token()

        elif self.lexer.sym == Token.PRINT:
            n = Node(NodeType.PRINT)
            self.lexer.next_token()
            n.op1 = self._paren_expr()

        else:
            n = Node(NodeType.EXPR, op1=self._expr())
            if self.lexer.sym != Token.SEMICOLON:
                self._error('";" expected')
            self.lexer.next_token()

        return n

    def parse(self):
        """
        Парсинг программы
        :return: Дерево разбора
        """
        self.lexer.next_token()
        node = Node(NodeType.PROGRAM, op1=self._statement())
        if self.lexer.sym != Token.EOF:
            self._error("Invalid statement syntax")
        return node
