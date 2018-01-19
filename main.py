# TODO больше тестов
# TODO BREAK, DIV, SQRT, SQR, INPUT
# TODO комментарии
# TODO отрицательные числа
# TODO добавть возможность ввода многосимвольного имени переменной
# TODO (?) status code
# TODO (?) ASM код
# TODO (?) запуск файла программы через вызов main.py или compiler и vm


import os
from os import path as osp

from core import Compiler, Lexer, Parser, VirtualMachine

test_dir = 'test/'


def run_tests():
    vm = VirtualMachine()

    test_files = sorted(os.listdir(test_dir))

    for i, file_name in enumerate(test_files):
        full_path = osp.join(test_dir, file_name)

        print('>>> Run test #{} ({})'.format(i, file_name))
        with open(full_path) as f:
            text = f.read()

            compiler = Compiler()
            parser = Parser(Lexer(text))

            ast = parser.parse()

            # print(ast)  # выведем дерево

            program = compiler.compile(ast)

            vars = vm.run(program)

            print('Execution finished.')
            for j in range(26):
                if vars[j] != '$':
                    print('{} = {}'.format(chr(j + ord('a')), vars[j]))

        print('\n' + '#' * 40 + '\n')


if __name__ == '__main__':
    run_tests()