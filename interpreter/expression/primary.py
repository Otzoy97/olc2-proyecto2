from interpreter.instruction import Instruction
from enum import Enum

class PrimaryType(Enum):
    FLOATING = 0
    CHARACTER = 1
    STRING = 2
    INTEGER = 3
    IDENTIFIER = 4

class Primary(Instruction):
    def __init__(self, value, type, row):
        self.value = value
        self.type = type
        self.row = row