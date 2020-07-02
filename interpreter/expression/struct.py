from interpreter.instruction import Instruction

class Struct(Instruction):
    def __init__(self, id, dec):
        self.id = id
        self.dec = dec

    def firstRun(self, localE, parent):
        pass