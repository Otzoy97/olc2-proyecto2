from interpreter.instruction import Instruction

class XorBitWise(Instruction):
    def __init__(self, andbw, xorbw, row):
        self.andbw = andbw
        self.xorbw = xorbw
        self.row = row