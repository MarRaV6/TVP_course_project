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
    MULTI = 15
    RT = 16
    SEG = 17  # Обычное деление
    CMPR = 18  # Мягкое сравнение
    MOD = 19  # Взятие остатка
    #DIV = 18 #


class Node:
    """
    Узел для АСТ
    """
    def __init__(self, kind: NodeType, value=None, op1=None, op2=None, op3=None):
        """
        :param kind: Тип узла
        :param value: Значение (напр. значение константы в случае присваивания)
        :param op1: Первый
        :param op2: Второй
        :param op3: И третий возможный потомок
        """
        self.kind = kind
        self.value = value
        self.op1 = op1
        self.op2 = op2
        self.op3 = op3

    def __repr__(self):
        return "Node({}, {})".format(self.kind, self.value)

    def __str__(self, level=0):
        ident = ' ' * 4 * level

        if level == 0:
            result = '{}'.format(self.kind.name)
        else:
            result = '\n{}+-{}({})'.format(ident, self.kind.name, self.value if self.value else '')

        for c in [self.op1, self.op2, self.op3]:
            if c:
                result += c.__str__(level=level+1)

        return result