from interpreter.instruction import Instruction
from enum import Enum

class PrimaryType(Enum):
    CONSTANT = 0
    IDENTIFIER = 1

class Primary(Instruction):
    def __init__(self, value, type, row):
        self.value = value
        self.type = type
        self.row = row

    def firstRun(self):
        pass