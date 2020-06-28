from interpreter.instruction import Instruction
from enum import Enum

class PostFixType(Enum):
    ARRAYACCESS     = 0
    CALL            = 1
    STRUCTACCESSS   = 2
    INCREMENT       = 3
    DECREMENT       = 4 

class Postfix(Instruction):
    def __init__(self, exp, type, row):
        self.exp = exp
        self.type = type
        self.row = row

    def firstRun(self):
        pass