from interpreter.expression.expression import Expression
from enum import Enum

class RelationalType(Enum):
    LS    = 0
    LSE   = 1
    GR    = 2
    GRE   = 3

class Relational(Expression):
    def __init__(self, shift, rel, type, row):
        self.shift = shift
        self.rel = rel
        self.type = type
        self.row =row