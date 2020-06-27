from interpreter.instruction import Instruction

class Conditional(Instruction):
    def __init__(self, orlog, exp, cond, row):
        self.orlog = orlog
        self.exp = exp
        self.cond = cond
        self.row = row