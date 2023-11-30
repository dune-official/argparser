class TokenPrecedence:
    ARGUMENT = 0x3
    VALUE = 0x01
    ASSIGNMENT = 0x04
    EXPRESSION = 0x02
    STOP = 0x00


class Token:

    def __init__(self, tokenvalue, precedence):
        self.__tokenvalue = tokenvalue
        self.__precedence = precedence

    @property
    def tokenvalue(self):
        return self.__tokenvalue

    @property
    def precedence(self):
        return self.__precedence

    def __str__(self):
        return self.__tokenvalue if self.__tokenvalue is not None else ''


class ValueToken(Token):

    def __init__(self, value):
        super().__init__(value, TokenPrecedence.VALUE)


class ArgToken(Token):

    def __init__(self, argname: str):
        super().__init__(argname, TokenPrecedence.ARGUMENT)


class ArgSingleToken(ArgToken):

    def __init__(self, argname: str):
        super().__init__(argname)


class ArgDoubleToken(ArgToken):

    def __init__(self, argname: str):
        super().__init__(argname)


class AssignmentToken(Token):

    def __init__(self):
        super().__init__(None, TokenPrecedence.ASSIGNMENT)


class ExressionToken(Token):

    def __init__(self):
        super().__init__(None, TokenPrecedence.EXPRESSION)


class StopToken(Token):

    def __init__(self):
        super().__init__('$', 0)


class Tokenstream:

    def __init__(self, tokens: list[Token]):

        self.__list = tokens
        self.__pos = 0

        if not isinstance(self.__list[-1], StopToken):
            self.__list.append(StopToken())

    def peek(self):
        return self.__list[self.__pos]

    def next(self):
        toreturn = self.peek()
        self.__pos += 1
        return toreturn

    def insert(self, item: Token):
        self.__list.insert(self.__pos, item)

    def __next__(self):
        return self.next()
