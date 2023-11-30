from .lexer import Lexer


class ArgParser:

    def __init__(self):

        # default aliases
        self.__aliases = {}

    def set_alias(self, alias: str, orig: str):
        self.__aliases[alias] = orig

    def clear_aliases(self):
        self.__aliases.clear()

    def parse_text(self, text):
        lx = lexer.Lexer(text, aliases=self.__aliases)
        parser = lx.lex()
        tree = parser.parse(0)
        return tree.evaluate()
