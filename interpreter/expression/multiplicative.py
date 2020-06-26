from interpreter.expression.expression import Expression
from enum import Enum

class MultiplicativeType(Enum):
    QUOTIENT = 0
    TIMES    = 1
    REMAINDER= 2

class Multiplicative(Expression):
    def __init__(self, cast, multi, type, row):
        self.cast = cast
        self.multi = multi
        self.type = type
        self.row = row