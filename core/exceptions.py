class CompileError(Exception):
    """Ошибка компиляции программы"""
    pass


class LexerError(CompileError):
    """
    Ошибка лексера, возникает при нахождении некорректных грамматических конструкций:
        a++;
        +-while(){}
    """
    pass


class ParserError(CompileError):
    """

    """
    pass
