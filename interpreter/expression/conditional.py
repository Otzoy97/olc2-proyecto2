from interpreter.instruction import Instruction

class Conditional(Instruction):
    def __init__(self, exp1, exp2, exp3, row):
        self.exp1 = exp1
        self.exp2 = exp2
        self.exp3 = exp3
        self.row = row

    def firstRun(self):
        pass