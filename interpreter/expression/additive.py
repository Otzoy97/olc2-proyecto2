from interpreter.expression.expression import Expression
from enum import Enum

class AdditiveType(Enum):
    PLUS    = 0
    MINUS   = 1

class Additive(Expression):
    def __init__(self, multi, add, type, row):
        self.multi = multi
        self.add = add
        self.type = type
        self.row =row