from interpreter.instruction import Instruction

class AndLogical(Instruction):
    def __init__(self, exp, acc, row):
        self.exp = exp
        self.acc = acc
        self.acc = row