from interpreter.instruction import Instruction

class Declaration(Instruction):
    def __init__(self, exp, row):
        self.exp = exp
        self.row = row


    def firstRun(self):
        pass