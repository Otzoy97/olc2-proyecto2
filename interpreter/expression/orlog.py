from interpreter.instruction import Instruction

class OrLogical(Instruction):
    def __init__(self, exp, acc, row):
        self.exp = exp
        self.acc = acc
        self.row = row

    def firstRun(self):
        pass