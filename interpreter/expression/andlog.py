from interpreter.instruction import Instruction

class AndLogical(Instruction):
    def __init__(self, orbw, andlog, row):
        self.orbw = orbw
        self.andlog = andlog
        self.row = row