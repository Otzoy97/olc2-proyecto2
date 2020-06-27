from interpreter.instruction import Instruction

class AndBitWise(Instruction):
    def __init__(self, equal, andbw, row):
        self.equal = equal
        self.andbw = andbw
        self.row = row

    def firstRun(self):
        print("aea")