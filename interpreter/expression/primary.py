from interpreter.instruction import Instruction
from interpreter.quadruple import Quadruple, OperatorQuadruple
from enum import Enum

class PrimaryType(Enum):
    CONSTANT = 0
    IDENTIFIER = 1

class Primary(Instruction):
    def __init__(self, value, type, row):
        self.value = value
        self.type = type
        self.row = row

    def firstRun(self, localE):
        if self.type == 1:
            #it is an identifier, look for it in the symbols table
            sym = localE.symTable.find(self.value)
            if sym != None:
                #there's a symbol associated with this identificator
                #return a temporary label
                return ("symbol", sym)
        else:
            #it is a raw value, it returns
            return ("rawvalue", self.value)
