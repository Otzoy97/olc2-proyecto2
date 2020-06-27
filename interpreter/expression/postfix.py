from interpreter.instruction import Instruction
from enum import Enum

class PostFixType(Enum):
    ARRAYACCESS     = 0
    CALL            = 1
    STRUCTACCESSS   = 2
    INCREMENT       = 3
    DECREMENT       = 4 

class Postfix(Instruction):
    def __init__(self, primary, postfix, type, row):
        self.primary = primary
        self.postfix = postfix
        self.type = type
        self.row = row