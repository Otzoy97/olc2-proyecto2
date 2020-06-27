from interpreter.instruction import Instruction
from enum import Enum

class ShiftType(Enum):
    SHL    = 0
    SHR    = 1

class Shift(Instruction):
    def __init__(self, add, shift, type, row):
        self.add = add
        self.shift = shift
        self.type = type
        self.row =row