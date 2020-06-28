from interpreter.instruction import Instruction

class Relational(Instruction):
    def __init__(self, exp, acc, row):
        self.exp = exp
        self.acc = acc
        self.row =row