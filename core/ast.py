from enum import IntEnum


class NodeType(IntEnum):
    VAR = 0
    CONST = 1
    ADD = 2
    SUB = 3
    LT = 4
    SET = 5
    IF1 = 6
    IF2 = 7
    WHILE = 8
    DO = 9
    EMPTY = 10
    SEQ = 11
    EXPR = 12
    PRINT = 13
    PROGRAM = 14


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
