from interpreter.instruction import Instruction
from interpreter.dspecifier import DSpecifier

class Cast(Instruction):
    def __init__(self, exp, acc, row):
        self.exp = exp
        self.acc = acc
        self.row = row

    def firstRun(self):
        pass