from interpreter.instruction import Instruction

class Jump(Instruction):
    def __init__(self, op, exp):
        self.op = op
        self.exp = exp

    def firstRun(self):
        pass
