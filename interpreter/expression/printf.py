from interpreter.instruction import Instruction
from interpreter.st import Symbol, SymbolTable
from interpreter.quadruple import Quadruple, OperatorQuadruple
from interpreter.operator import Operator

class Printf(Instruction):
    def __init__(self, exp):
        self.exp = exp

    def firstRun(self, localE):
        baseString = self.exp[0][1:-1]
        idx = 1
        i = 0
        if len(self.exp) > 1:
            while i < len(baseString):
                if idx < len(self.exp) and baseString[i] == r"%":
                    baseName = self.exp[idx].firstRun(localE)
                    if baseName[0] == "symbol":
                        Quadruple.QDict.append(Quadruple(OperatorQuadruple.PRINT, baseName[1].temp, None, None))
                    else:
                        Quadruple.QDict.append(Quadruple(OperatorQuadruple.PRINT, baseName[1], None, None))
                    idx += 1
                    i += 1
                else:
                    Quadruple.QDict.append(Quadruple(OperatorQuadruple.PRINT, f'"{str(baseString[i])}"', None, None))
                i += 1
        else:
            Quadruple.QDict.append(Quadruple(OperatorQuadruple.PRINT, f'"{baseString}"', None, None))
        return ("rawvalue", 0)
