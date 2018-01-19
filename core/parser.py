from core.exceptions import ParserError
from .lexer import Token, Lexer
from .ast import Node, NodeType


class Parser:
    _MATH_OP = [Token.PLUS, Token.MINUS, Token.MULTI, Token.SEG, Token.MOD]

    def __init__(self, lexer: Lexer):
        self.lexer = lexer

    def error(self, msg):
        cs = self.lexer.current_symbol
        code_fragment = self.lexer.program_text[0 if cs < 15 else cs-10 : cs+2]
        raise ParserError('Parser error: {}\nFragment: ...\n{}\n...'.format(msg, code_fragment))

    def term(self):
        if self.lexer.sym == Token.ID:
            n = Node(NodeType.VAR, self.lexer.value)
            self.lexer.next_token()
            return n
        elif self.lexer.sym == Token.NUM:
            n = Node(NodeType.CONST, self.lexer.value)
            self.lexer.next_token()
            return n
        else:
            return self.paren_expr()

    def calculate(self):
        n = self.term()
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
            n = Node(kind, op1=n, op2=self.term())
        return n

    def test(self):
        n = self.calculate()
        if self.lexer.sym == Token.LESS:
            self.lexer.next_token()
            n = Node(NodeType.LT, op1=n, op2=self.calculate())

        elif self.lexer.sym == Token.MORE:
            self.lexer.next_token()
            n = Node(NodeType.RT, op1=n, op2=self.calculate())

        elif self.lexer.sym == Token.CMPR:
            self.lexer.next_token()
            n = Node(NodeType.CMPR, op1=n, op2=self.calculate())

        return n

    def expr(self):
        if self.lexer.sym != Token.ID:
            return self.test()

        n = self.test()
        if n.kind == NodeType.VAR and self.lexer.sym == Token.EQUAL:
            self.lexer.next_token()
            n = Node(NodeType.SET, op1=n, op2=self.expr())

        return n

    def paren_expr(self):
        if self.lexer.sym != Token.LPAR:
            self.error('"(" expected')
        self.lexer.next_token()
        n = self.expr()
        if self.lexer.sym != Token.RPAR:
            self.error('")" expected')
        self.lexer.next_token()
        return n

    def statement(self):
        """
        Разбор выражения, вернет узел или None
        :return:
        """
        if self.lexer.sym == Token.IF:
            n = Node(NodeType.IF1)
            self.lexer.next_token()
            n.op1 = self.paren_expr()
            n.op2 = self.statement()
            if self.lexer.sym == Token.ELSE:
                n.kind = NodeType.IF2
                self.lexer.next_token()
                n.op3 = self.statement()

        elif self.lexer.sym == Token.WHILE:
            n = Node(NodeType.WHILE)
            self.lexer.next_token()
            n.op1 = self.paren_expr()
            n.op2 = self.statement()

        elif self.lexer.sym == Token.DO:
            n = Node(NodeType.DO)
            self.lexer.next_token()
            n.op1 = self.statement()
            if self.lexer.sym != Token.WHILE:
                self.error('"while" expected')
            self.lexer.next_token()
            n.op2 = self.paren_expr()
            if self.lexer.sym != Token.SEMICOLON:
                self.error('";" expected')

        elif self.lexer.sym == Token.SEMICOLON:
            n = Node(NodeType.EMPTY)
            self.lexer.next_token()

        elif self.lexer.sym == Token.LBRA:
            n = Node(NodeType.EMPTY)
            self.lexer.next_token()
            while self.lexer.sym != Token.RBRA:
                n = Node(NodeType.SEQ, op1=n, op2=self.statement())
            self.lexer.next_token()

        elif self.lexer.sym == Token.PRINT:
            n = Node(NodeType.PRINT)
            self.lexer.next_token()
            n.op1 = self.paren_expr()

        else:
            n = Node(NodeType.EXPR, op1=self.expr())
            if self.lexer.sym != Token.SEMICOLON:
                self.error('";" expected')
            self.lexer.next_token()

        return n

    def parse(self):
        """
        Парсинг программы
        :return: дерево разбора
        """
        self.lexer.next_token()
        node = Node(NodeType.PROGRAM, op1=self.statement())
        if self.lexer.sym != Token.EOF:
            self.error("Invalid statement syntax")
        return node
