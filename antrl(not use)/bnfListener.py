# Generated from bnf.g4 by ANTLR 4.7
from antlr4 import *
if __name__ is not None and "." in __name__:
    from .bnfParser import bnfParser
else:
    from bnfParser import bnfParser

# This class defines a complete listener for a parse tree produced by bnfParser.
class bnfListener(ParseTreeListener):

    # Enter a parse tree produced by bnfParser#program.
    def enterProgram(self, ctx:bnfParser.ProgramContext):
        pass

    # Exit a parse tree produced by bnfParser#program.
    def exitProgram(self, ctx:bnfParser.ProgramContext):
        pass


    # Enter a parse tree produced by bnfParser#block.
    def enterBlock(self, ctx:bnfParser.BlockContext):
        pass

    # Exit a parse tree produced by bnfParser#block.
    def exitBlock(self, ctx:bnfParser.BlockContext):
        pass


    # Enter a parse tree produced by bnfParser#consts.
    def enterConsts(self, ctx:bnfParser.ConstsContext):
        pass

    # Exit a parse tree produced by bnfParser#consts.
    def exitConsts(self, ctx:bnfParser.ConstsContext):
        pass


    # Enter a parse tree produced by bnfParser#plvars.
    def enterPlvars(self, ctx:bnfParser.PlvarsContext):
        pass

    # Exit a parse tree produced by bnfParser#plvars.
    def exitPlvars(self, ctx:bnfParser.PlvarsContext):
        pass


    # Enter a parse tree produced by bnfParser#procedure.
    def enterProcedure(self, ctx:bnfParser.ProcedureContext):
        pass

    # Exit a parse tree produced by bnfParser#procedure.
    def exitProcedure(self, ctx:bnfParser.ProcedureContext):
        pass


    # Enter a parse tree produced by bnfParser#statement.
    def enterStatement(self, ctx:bnfParser.StatementContext):
        pass

    # Exit a parse tree produced by bnfParser#statement.
    def exitStatement(self, ctx:bnfParser.StatementContext):
        pass


    # Enter a parse tree produced by bnfParser#condition.
    def enterCondition(self, ctx:bnfParser.ConditionContext):
        pass

    # Exit a parse tree produced by bnfParser#condition.
    def exitCondition(self, ctx:bnfParser.ConditionContext):
        pass


    # Enter a parse tree produced by bnfParser#expression.
    def enterExpression(self, ctx:bnfParser.ExpressionContext):
        pass

    # Exit a parse tree produced by bnfParser#expression.
    def exitExpression(self, ctx:bnfParser.ExpressionContext):
        pass


    # Enter a parse tree produced by bnfParser#term.
    def enterTerm(self, ctx:bnfParser.TermContext):
        pass

    # Exit a parse tree produced by bnfParser#term.
    def exitTerm(self, ctx:bnfParser.TermContext):
        pass


    # Enter a parse tree produced by bnfParser#factor.
    def enterFactor(self, ctx:bnfParser.FactorContext):
        pass

    # Exit a parse tree produced by bnfParser#factor.
    def exitFactor(self, ctx:bnfParser.FactorContext):
        pass


