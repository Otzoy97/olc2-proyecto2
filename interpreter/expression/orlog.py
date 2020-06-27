from interpreter.instruction import Instruction

class OrLogical(Instruction):
    def __init__(self, andlog,  orlog, row):
        self.andlog = andlog
        self.orlog = orlog
        self.row = row