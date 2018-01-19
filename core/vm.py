from .asm import ASM


class VirtualMachine:
    def __init__(self, EPS=0.00001):
        self.EPS = EPS

    def run(self, program):
        var = ['$' for i in range(26)]
        stack = []
        pc = 0
        while True:
            op = ASM(program[pc])
            if pc < len(program) - 1:
                arg = program[pc + 1]

            if op == ASM.IFETCH:
                stack.append(var[arg]); pc += 2

            elif op == ASM.ISTORE:
                var[arg] = stack.pop(); pc += 2

            elif op == ASM.IPUSH:
                stack.append(arg); pc += 2

            elif op == ASM.IPOP:
                stack.append(arg); stack.pop(); pc += 1

            elif op == ASM.IADD:
                stack[-2] += stack[-1]; stack.pop(); pc += 1

            elif op == ASM.ISUB:
                stack[-2] -= stack[-1]; stack.pop(); pc += 1

            elif op == ASM.IMULTI:
                stack[-2] *= stack[-1]; stack.pop(); pc += 1

            elif op == ASM.ISEG:
                stack[-2] /= stack[-1]; stack.pop(); pc += 1

            elif op == ASM.IMOD:
                stack[-2] %= stack[-1]; stack.pop(); pc += 1

            elif op == ASM.ILT:
                if stack[-2] < stack[-1]:
                    stack[-2] = 1
                else:
                    stack[-2] = 0
                stack.pop()
                pc += 1

            elif op == ASM.IRT:
                if stack[-2] > stack[-1]:
                    stack[-2] = 1
                else:
                    stack[-2] = 0
                stack.pop()
                pc += 1

            elif op == ASM.ICMPR:
                if abs(stack[-2] - stack[-1]) < self.EPS:
                    stack[-2] = 1
                else:
                    stack[-2] = 0

                stack.pop()
                pc += 1

            elif op == ASM.JZ:
                if stack.pop() == 0:
                    pc = arg
                else:
                    pc += 2

            elif op == ASM.JNZ:
                if stack.pop() != 0:
                    pc = arg
                else:
                    pc += 2

            elif op == ASM.JMP:
                pc = arg

            elif op == ASM.PRINT:
                print(stack.pop())
                pc += 1

            elif op == ASM.HALT:
                break

        return var
