from interpreter.instruction import Instruction

class Cast(Instruction):
    def __init__(self, unary, cast, decSpec, row):
        self.unary = unary
        self.cast = cast
        self.decSpec = decSpec
        self.row = row