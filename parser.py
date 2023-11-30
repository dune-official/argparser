from .tokens import *
from .nodes import *


class Parser:

    def __init__(self, stream: Tokenstream, aliases: dict):
        self.__stream = stream
        self.__aliases = aliases

    def parse(self, precedence=0):
        """
        Parses the tokens in the stream recursively.

        Alternatively to the token type, its precedence can be used since it is unique to the token.

        Currently, the only null denoter are the argument tokens, but when that changes (it won't), a match case structure would be needed.

        :param precedence:
        :return:
        """

        current_token = self.__stream.next()
        lookahead = self.__stream.peek()

        if isinstance(current_token, ArgSingleToken) and isinstance(lookahead, ValueToken):
            self.__stream.insert(AssignmentToken())

        if isinstance(lookahead, (ArgToken, StopToken)):
            self.__stream.insert(AssignmentToken())

        if not isinstance(current_token, ArgToken):
            raise ValueError(
                "Parse error: Expected argument"
            )

        left = ArgNode(self.__aliases.get(current_token.tokenvalue.lower(), current_token.tokenvalue))

        # crucial part to the pratt parser is the loop here
        while self.__stream.peek().precedence > precedence:
            current_token = self.__stream.next()

            match current_token.precedence:
                case 0x04:
                    left = self.parse_assignment(left)
                case 0x02:
                    left = self.parse_expression(left)
                case _:
                    raise ValueError(
                        f"Parse error: Unknown Token: {type(current_token)}"
                    )

        return left

    def parse_assignment(self, lhs):
        if not isinstance(self.__stream.peek(), ValueToken):
            rhs = ValueNode(None)
        else:
            rhs = self.__stream.next()
            rhs = ValueNode(rhs.tokenvalue)

        if isinstance(self.__stream.peek(), ArgToken):
            self.__stream.insert(ExressionToken())

        return AssignmentNode(lhs, rhs)

    def parse_expression(self, lhs):
        if not isinstance(self.__stream.peek(), ArgToken):
            raise ValueError(
                f"Parse error: Illegal Expression after assignment ({type(lhs)})"
            )

        return ExpressionNode(lhs, self.parse(TokenPrecedence.EXPRESSION))
