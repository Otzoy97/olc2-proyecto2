from interpreter.expression.expression import Expression
from enum import Enum

class EqualityType(Enum):
    EQ    = 0
    NEQ   = 1

class Equality(Expression):
    def __init__(self, rel, equal, type, row):
        self.rel = rel
        self.equal = equal
        self.type = type
        self.row =row