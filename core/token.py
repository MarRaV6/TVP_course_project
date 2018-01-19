from enum import IntEnum


class Token(IntEnum):
    NUM = 0
    ID = 1
    IF = 2
    ELSE = 3
    WHILE = 4
    DO = 5
    LBRA = 6
    RBRA = 7
    LPAR = 8
    RPAR = 9
    PLUS = 10
    MINUS = 11
    MULTI = 12
    LESS = 13
    EQUAL = 14
    SEMICOLON = 15
    PRINT = 16
    EOF = 17

