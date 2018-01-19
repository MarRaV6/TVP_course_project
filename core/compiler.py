from core.exceptions import CompileError
from .ast import NodeType
from .asm import ASM


class Compiler:
    """
    Компилятор, преобразует АСТ в ассемблерный код виртуальной машины
    """
    def __init__(self):
        self._program = []
        self._pc = 0

    def _gen_command(self, command):
        """
        Добавим комманду
        """
        self._program.append(command.value)
        self._pc += 1

    def _gen_addr(self, addr):
        """
        Добавим адрес
        """
        self._program.append(addr)
        self._pc += 1

    def _fix_addr(self, addr, value):
        """
        Исправим адрес
        """
        self._program[addr] = value

    def compile(self, node):
        if node.kind == NodeType.VAR:
            self._gen_command(ASM.IFETCH)
            self._gen_addr(node.value)

        elif node.kind == NodeType.CONST:
            self._gen_command(ASM.IPUSH)
            self._gen_addr(node.value)

        elif node.kind == NodeType.ADD:
            self.compile(node.op1)
            self.compile(node.op2)
            self._gen_command(ASM.IADD)

        elif node.kind == NodeType.SUB:
            self.compile(node.op1)
            self.compile(node.op2)
            self._gen_command(ASM.ISUB)

        elif node.kind == NodeType.MULTI:
            self.compile(node.op1)
            self.compile(node.op2)
            self._gen_command(ASM.IMULTI)

        elif node.kind == NodeType.SEG:
            self.compile(node.op1)
            self.compile(node.op2)
            self._gen_command(ASM.ISEG)

        elif node.kind == NodeType.MOD:
            self.compile(node.op1)
            self.compile(node.op2)
            self._gen_command(ASM.IMOD)

        elif node.kind == NodeType.LT:
            self.compile(node.op1)
            self.compile(node.op2)
            self._gen_command(ASM.ILT)

        elif node.kind == NodeType.RT:
            self.compile(node.op1)
            self.compile(node.op2)
            self._gen_command(ASM.IRT)

        elif node.kind == NodeType.SET:
            self.compile(node.op2)
            self._gen_command(ASM.ISTORE)
            self._gen_addr(node.op1.value)

        elif node.kind == NodeType.IF1:
            self.compile(node.op1)
            self._gen_command(ASM.JZ)
            addr = self._pc
            self._gen_addr(0)
            self.compile(node.op2)
            self._fix_addr(addr, self._pc)

        elif node.kind == NodeType.IF2:
            self.compile(node.op1)
            self._gen_command(ASM.JZ)
            addr1 = self._pc
            self._gen_addr(0)
            self.compile(node.op2)
            self._gen_command(ASM.JMP)
            addr2 = self._pc
            self._gen_addr(0)
            self._fix_addr(addr1, self._pc)
            self.compile(node.op3)
            self._fix_addr(addr2, self._pc)

        elif node.kind == NodeType.WHILE:
            addr1 = self._pc
            self.compile(node.op1)
            self._gen_command(ASM.JZ)
            addr2 = self._pc
            self._gen_addr(0)
            self.compile(node.op2)
            self._gen_command(ASM.JMP)
            self._gen_addr(addr1)
            self._fix_addr(addr2, self._pc)

        elif node.kind == NodeType.DO:
            addr = self._pc
            self.compile(node.op1)
            self.compile(node.op2)
            self._gen_command(ASM.JNZ)
            self._gen_addr(addr)

        elif node.kind == NodeType.SEQ:
            self.compile(node.op1)
            self.compile(node.op2)

        elif node.kind == NodeType.EXPR:
            self.compile(node.op1)
            self._gen_command(ASM.IPOP)

        elif node.kind == NodeType.PRINT:
            self.compile(node.op1)
            self._gen_command(ASM.PRINT)

        elif node.kind == NodeType.CMPR:
            self.compile(node.op1)
            self.compile(node.op2)
            self._gen_command(ASM.ICMPR)

        elif node.kind == NodeType.PROGRAM:
            self.compile(node.op1)
            self._gen_command(ASM.HALT)

        elif node.kind == NodeType.EMPTY:
            pass

        else:
            raise CompileError('Unknown AST node type: ' + str(node.kind))

        return self._program
