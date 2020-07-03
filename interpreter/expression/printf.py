from interpreter.instruction import Instruction
from interpreter.st import Symbol, SymbolTable
from interpreter.quadruple import Quadruple, OperatorQuadruple
from interpreter.operator import Operator

class Printf(Instruction):
    def __init__(self, exp):
        self.exp = exp

    def firstRun(self, localE):
        baseString = self.exp[0]
        buff = ""
        idx = 1
        i = 0
        while i < len(baseString) - 1:
            if baseString[i] == r"%":
                baseName = self.exp[idx].firstRun(localE)
                baseName = baseName[1].temp if baseName[0] == "symbol" else baseName[1]
                buff += str(baseName)
                idx += 1
                i += 1
            else:
                buff += str(baseString[i])
            i += 1
        Quadruple.QDict.append(Quadruple(OperatorQuadruple.PRINT, f'"{buff}"', None, None))
        return ("rawvalue", 0)
