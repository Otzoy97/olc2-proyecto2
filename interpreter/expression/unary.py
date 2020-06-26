from interpreter.expression.expression import Expression
from enum import Enum

class UnaryType(Enum):
    INCREMENT = 0
    DECREMENT = 1
    CAST      = 2
    SIZEOFU   = 3 #unaryExpression
    SIZEOFD   = 4 #dec_spec

class Unary(Expression):
    def __init__(self, postfix, unary, type, row):
        self.postfix = postfix
        self.unary   = unary
        self.type    = type
        self.row     = row