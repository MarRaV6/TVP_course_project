# TODO сделать красиво
# TODO (?) запуск файла программы через вызов main.py или compiler и vm
# TODO больше тестов
# TODO status code

# TODO ISINT
# TODO равенство

# TODO определить все простые числа в интервале
# TODO комментарии


import os
from os import path as osp

from core.compiler import Compiler
from core.lexer import Lexer
from core.parser import Parser
from core.vm import VirtualMachine

test_dir = 'test/'


def run_tests():
    vm = VirtualMachine()

    test_files = sorted(os.listdir(test_dir))

    for i, file_name in enumerate(test_files):
        full_path = osp.join(test_dir, file_name)

        print('>>> Run test #{} ({})'.format(i, full_path))
        with open(full_path) as f:
            text = f.read()

            compiler = Compiler()
            parser = Parser(Lexer(text))

            ast = parser.parse()

            print(ast)  # выведем дерево

            program = compiler.compile(ast)

            vars = vm.run(program)

            print('Execution finished.')
            for i in range(26):
                if vars[i] != '$':
                    print('{} = {}'.format(chr(i + ord('a')), vars[i]))

        print('\n' + '#' * 40 + '\n')


if __name__ == '__main__':
    run_tests()