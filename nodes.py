class Node:

    def __init__(self, content):
        self.__content = content

    @property
    def content(self):
        return self.__content

    def evaluate(self):
        return


class LeafNode(Node):

    def __init__(self, content):
        super().__init__(content)

    def evaluate(self):
        return super().content


class InnerNode(Node):

    def __init__(self, lhs, rhs):
        super().__init__(None)
        self.__lhs = lhs
        self.__rhs = rhs

    @property
    def lhs(self):
        return self.__lhs

    @property
    def rhs(self):
        return self.__rhs


class ArgNode(LeafNode):

    def __init__(self, argname):

        super().__init__(argname)


class ValueNode(LeafNode):

    def __init__(self, value):
        super().__init__(value)


class AssignmentNode(InnerNode):

    def __init__(self, lhs, rhs):
        super().__init__(lhs, rhs)

    def evaluate(self):
        return [super().lhs.evaluate(), super().rhs.evaluate()]


class ExpressionNode(InnerNode):
    def __init__(self, lhs, rhs):
        super().__init__(lhs, rhs)

    def evaluate(self):
        expression = []

        expression += super().lhs.evaluate()
        expression += super().rhs.evaluate()

        return expression
