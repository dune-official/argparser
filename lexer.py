from .tokens import *
from .parser import Parser


class Lexer:

    def __init__(self, input_: str | list, aliases: dict):
        self.__input = list(input_) if isinstance(input_, str) else input_
        self.__input.append('$$')

        self.__pos = 0
        self.__tokens = []
        self.__after_assignment = False
        self.__aliases = aliases

    def peek(self):
        if self.__pos >= len(self.__input):
            self.__pos = len(self.__input) - 1
        return self.__input[self.__pos]

    def consume(self):
        rtn = self.peek()
        self.__pos += 1
        return rtn

    def lex(self):
        cur_char = self.peek()

        while cur_char != '$$':

            match cur_char.lower():

                # safeguard in case we ever skip past the end somehow
                case ' ' | '\t' | '\n' | '$$':
                    self.__lex_whitespace()

                case '-':
                    self.__lex_argument()

                case '=':
                    self.__lex_assignment()

                case 'a' | 'b' | 'c' | 'd' | 'e' | 'f' | 'g' | 'h' | 'i' | 'j' | 'k' | 'l' | 'm' | 'n' | 'o' | 'p' | 'q' | 'r' | 's' | 't' | 'u' | 'v' | 'w' | 'x' | 'y' | 'z' | '0' | '1' | '2' | '3' | '4' | '5' | '6' | '7' | '8' | '9' | '\"' | '\'':
                    self.__lex_value()

                case _:
                    cur_char = self.consume()

                    continue

            cur_char = self.peek()

        return Parser(Tokenstream(self.__tokens), self.__aliases)

    def __lex_value(self):

        value = []

        state = 0

        while True:

            match state:
                case 0:
                    first = self.consume()
                    match first:
                        case 'a' | 'b' | 'c' | 'd' | 'e' | 'f' | 'g' | 'h' | 'i' | 'j' | 'k' | 'l' | 'm' | 'n' | 'o' | 'p' | 'q' | 'r' | 's' | 't' | 'u' | 'v' | 'w' | 'x' | 'y' | 'z' | '0' | '1' | '2' | '3' | '4' | '5' | '6' | '7' | '8' | '9':
                            value.append(first)
                            state = 1
                        case '\'':
                            state = 2
                        case '"':
                            state = 3
                        case _:
                            raise SyntaxError(
                                f"Unknown token in input stream: {first}"
                            )

                case 1:
                    nxt = self.consume()
                    match nxt:
                        case 'a' | 'b' | 'c' | 'd' | 'e' | 'f' | 'g' | 'h' | 'i' | 'j' | 'k' | 'l' | 'm' | 'n' | 'o' | 'p' | 'q' | 'r' | 's' | 't' | 'u' | 'v' | 'w' | 'x' | 'y' | 'z' | '0' | '1' | '2' | '3' | '4' | '5' | '6' | '7' | '8' | '9':
                            value.append(nxt)
                        case ' ' | '$$':
                            state = 4
                        case _:
                            raise SyntaxError(
                                f"Unknown token in input stream: {nxt}"
                            )

                case 2:
                    nxt = self.consume()
                    match nxt:
                        case '\'':
                            state = 4
                        case '$$':
                            state = 5
                        case _:
                            value.append(nxt)

                case 3:
                    nxt = self.consume()
                    match nxt:
                        case '"':
                            state = 4
                        case '$$':
                            state = 5
                        case _:
                            value.append(nxt)

                case 4:
                    self.__tokens.append(ValueToken(''.join(value)))
                    return

                case 5:
                    raise SyntaxError(
                        "Unclosed parentheses in input stream"
                    )

    def __lex_assignment(self):
        self.consume()
        self.__tokens.append(AssignmentToken())
        self.__after_assignment = True

    def __lex_argument(self):

        argname = []

        self.consume()
        rettype = ArgSingleToken
        state = 1

        while True:
            match state:
                case 1:
                    first = self.consume()
                    match first.lower():
                        case '-':
                            state = 2
                        case 'a' | 'b' | 'c' | 'd' | 'e' | 'f' | 'g' | 'h' | 'i' | 'j' | 'k' | 'l' | 'm' | 'n' | 'o' | 'p' | 'q' | 'r' | 's' | 't' | 'u' | 'v' | 'w' | 'x' | 'y' | 'z':
                            argname.append(first)
                            state = 3
                        case '$$':
                            state = 5
                        case _:
                            raise SyntaxError(
                                f"Unknown token in input stream: {first}"
                            )
                case 2:
                    rettype = ArgDoubleToken
                    nxt = self.consume()
                    match nxt.lower():
                        case 'a' | 'b' | 'c' | 'd' | 'e' | 'f' | 'g' | 'h' | 'i' | 'j' | 'k' | 'l' | 'm' | 'n' | 'o' | 'p' | 'q' | 'r' | 's' | 't' | 'u' | 'v' | 'w' | 'x' | 'y' | 'z' | '0' | '1' | '2' | '3' | '4' | '5' | '6' | '7' | '8' | '9':
                            argname.append(nxt)
                            state = 3
                        case '$$':
                            state = 5
                        case _:
                            raise SyntaxError(
                                f"Unknown token in input stream: {nxt}"
                            )
                case 3:
                    nxt = self.consume()
                    match nxt.lower():
                        case 'a' | 'b' | 'c' | 'd' | 'e' | 'f' | 'g' | 'h' | 'i' | 'j' | 'k' | 'l' | 'm' | 'n' | 'o' | 'p' | 'q' | 'r' | 's' | 't' | 'u' | 'v' | 'w' | 'x' | 'y' | 'z' | '0' | '1' | '2' | '3' | '4' | '5' | '6' | '7' | '8' | '9':
                            argname.append(nxt)
                            state = 3
                        case '$$' | ' ':
                            state = 4
                        case '=':
                            state = 6
                        case _:
                            raise SyntaxError(
                                f"Unknown token in input stream: {nxt}"
                            )
                case 4:
                    self.__tokens.append(rettype(''.join(argname)))
                    return
                case 5:
                    raise SyntaxError(
                        "Unexpected input end in stream"
                    )
                case 6:
                    self.__tokens.append(rettype(''.join(argname)))
                    self.__tokens.append(AssignmentToken())
                    self.__after_assignment = True
                    return

    def __lex_whitespace(self):
        self.consume()
        return
