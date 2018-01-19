from .ast import NodeType
from .asm import ASM


class Compiler:
    """
    Компилятор, преобразует АСТ в ассемблерный код виртуальной машины
    """
    def __init__(self):
        self.program = []
        self.pc = 0

    def gen(self, command):
        # если это асм комманда, то вывести ее value, иначе это адрес
        self.program.append(command.value if isinstance(command, ASM) else command)
        self.pc = self.pc + 1

    def compile(self, node):
        if node.kind == NodeType.VAR:
            self.gen(ASM.IFETCH)
            self.gen(node.value)

        elif node.kind == NodeType.CONST:
            self.gen(ASM.IPUSH)
            self.gen(node.value)

        elif node.kind == NodeType.ADD:
            self.compile(node.op1)
            self.compile(node.op2)
            self.gen(ASM.IADD)

        elif node.kind == NodeType.SUB:
            self.compile(node.op1)
            self.compile(node.op2)
            self.gen(ASM.ISUB)

        elif node.kind == NodeType.MULTI:
            self.compile(node.op1)
            self.compile(node.op2)
            self.gen(ASM.IMULTI)

        elif node.kind == NodeType.LT:
            self.compile(node.op1)
            self.compile(node.op2)
            self.gen(ASM.ILT)

        elif node.kind == NodeType.RT:
            self.compile(node.op1)
            self.compile(node.op2)
            self.gen(ASM.IRT)

        elif node.kind == NodeType.SET:
            self.compile(node.op2)
            self.gen(ASM.ISTORE)
            self.gen(node.op1.value)

        elif node.kind == NodeType.IF1:
            self.compile(node.op1)
            self.gen(ASM.JZ)
            addr = self.pc
            self.gen(0)
            self.compile(node.op2)
            self.program[addr] = self.pc

        elif node.kind == NodeType.IF2:
            self.compile(node.op1)
            self.gen(ASM.JZ)
            addr1 = self.pc
            self.gen(0)
            self.compile(node.op2)
            self.gen(ASM.JMP)
            addr2 = self.pc
            self.gen(0)
            self.program[addr1] = self.pc
            self.compile(node.op3)
            self.program[addr2] = self.pc

        elif node.kind == NodeType.WHILE:
            addr1 = self.pc
            self.compile(node.op1)
            self.gen(ASM.JZ)
            addr2 = self.pc
            self.gen(0)
            self.compile(node.op2)
            self.gen(ASM.JMP)
            self.gen(addr1)
            self.program[addr2] = self.pc

        elif node.kind == NodeType.DO:
            addr = self.pc
            self.compile(node.op1)
            self.compile(node.op2)
            self.gen(ASM.JNZ)
            self.gen(addr)

        elif node.kind == NodeType.SEQ:
            self.compile(node.op1)
            self.compile(node.op2)

        elif node.kind == NodeType.EXPR:
            self.compile(node.op1)
            self.gen(ASM.IPOP)

        elif node.kind == NodeType.PRINT:
            self.compile(node.op1)
            self.gen(ASM.PRINT)

        elif node.kind == NodeType.PROGRAM:
            self.compile(node.op1)
            self.gen(ASM.HALT)

        return self.program
