from interpreter.instruction import Instruction

class Shift(Instruction):
    def __init__(self, add, shift, type, row):
        self.add = add
        self.shift = shift
        self.type = type
        self.row =row