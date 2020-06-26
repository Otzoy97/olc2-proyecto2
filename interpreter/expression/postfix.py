from interpreter.expression.expression import Expression
from enum import Enum

class PostFixType (Enum):
    ARRAYACCESS = 0
    PARAMETERLIST = 1
    DOTACCESSS = 2
    INCREMENT = 3
    DECREMENT = 4    

class Postfix(Expression):
    def __init__(self, primary, postfix, type, row):
        self.primary = primary
        self.postfix = postfix
        self.type = type
        self.row = row