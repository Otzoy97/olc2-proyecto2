from interpreter.instruction import Instruction
from interpreter.dspecifier import DSpecifier

class Cast(Instruction):
    def __init__(self, unary, cast, decSpec, row):
        self.unary = unary
        self.cast = cast
        self.decSpec = decSpec
        self.row = row