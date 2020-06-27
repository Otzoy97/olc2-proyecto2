from interpreter.instruction import Instruction
from enum import Enum

class AdditiveType(Enum):
    PLUS    = 0
    MINUS   = 1

class Additive(Instruction):
    def __init__(self, multi, add, type, row):
        self.multi = multi
        self.add = add
        self.type = type
        self.row =row