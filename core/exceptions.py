class CompileError(Exception):
    pass


class LexerError(CompileError):
    pass


class ParserError(CompileError):
    pass
