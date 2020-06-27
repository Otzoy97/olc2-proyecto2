from interpreter.instruction import Instruction

class OrBitWise(Instruction):
    def __init__(self, xorbw, orbw, row):
        self.xorbw = xorbw
        self.orbw = orbw
        self.row = row