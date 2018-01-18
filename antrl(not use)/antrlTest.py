import sys
from antlr4 import *
from bnfLexer import bnfLexer
from bnfParser import bnfParser


def getTree(argv):
    input = FileStream('myfile.txt')
    lexer = bnfLexer(input)
    stream = CommonTokenStream(lexer)
    parser = bnfParser(stream)
    tree = parser.program()
    print(type(tree.getChild(0)))
    return tree

if __name__ == '__main__':
    getTree(sys.argv)