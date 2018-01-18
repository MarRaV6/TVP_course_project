from .parser import Parser
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
        if node.kind == Parser.VAR:
            self.gen(ASM.IFETCH)
            self.gen(node.value)

        elif node.kind == Parser.CONST:
            self.gen(ASM.IPUSH)
            self.gen(node.value)

        elif node.kind == Parser.ADD:
            self.compile(node.op1)
            self.compile(node.op2)
            self.gen(ASM.IADD)

        elif node.kind == Parser.SUB:
            self.compile(node.op1)
            self.compile(node.op2)
            self.gen(ASM.ISUB)

        elif node.kind == Parser.LT:
            self.compile(node.op1)
            self.compile(node.op2)
            self.gen(ASM.ILT)

        elif node.kind == Parser.SET:
            self.compile(node.op2)
            self.gen(ASM.ISTORE)
            self.gen(node.op1.value)

        elif node.kind == Parser.IF1:
            self.compile(node.op1)
            self.gen(ASM.JZ)
            addr = self.pc
            self.gen(0)
            self.compile(node.op2)
            self.program[addr] = self.pc

        elif node.kind == Parser.IF2:
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

        elif node.kind == Parser.WHILE:
            addr1 = self.pc
            self.compile(node.op1)
            self.gen(ASM.JZ)
            addr2 = self.pc
            self.gen(0)
            self.compile(node.op2)
            self.gen(ASM.JMP)
            self.gen(addr1)
            self.program[addr2] = self.pc

        elif node.kind == Parser.DO:
            addr = self.pc
            self.compile(node.op1)
            self.compile(node.op2)
            self.gen(ASM.JNZ)
            self.gen(addr)

        elif node.kind == Parser.SEQ:
            self.compile(node.op1)
            self.compile(node.op2)

        elif node.kind == Parser.EXPR:
            self.compile(node.op1)
            self.gen(ASM.IPOP)

        elif node.kind == Parser.PRINT:
            self.compile(node.op1)
            self.gen(ASM.PRINT)

        elif node.kind == Parser.PROG:
            self.compile(node.op1)
            self.gen(ASM.HALT)

        return self.program
