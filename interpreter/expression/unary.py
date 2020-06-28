from interpreter.instruction import Instruction
from enum import Enum

class UnaryType(Enum):
    INCREMENT = 0
    DECREMENT = 1
    CAST      = 2
    SIZEOFU   = 3 #unaryExpression
    SIZEOFD   = 4 #dec_spec

class Unary(Instruction):
    def __init__(self, exp, acc, row):
        self.exp = exp
        self.acc = acc
        self.row = row