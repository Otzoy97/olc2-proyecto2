from interpreter.instruction import Instruction
from interpreter.st import Symbol, SymbolTable
from interpreter.quadruple import Quadruple, OperatorQuadruple
from interpreter.operator import Operator

class Printf(Instruction):
    def __init__(self, exp):
        self.exp = exp

    def firstRun(self, localE):
        baseString = self.exp[0].firstRun(localE)
        baseString = baseString[1]
        if isinstance(baseString, str):
            baseString = baseString[1:-1]
        else:
            return ("rawvalue", 0)
        idx = 1
        i = 0
        try:
            if len(self.exp) > 1:
                baseString = baseString.replace("\\n","\n")
                baseString = baseString.replace("\\t","\t")
                baseString = baseString.replace("\\r","\r")
                #FIXME: no imprime bien cuando hay un caracter de escpe
                while i < len(baseString):
                    if idx < len(self.exp) and baseString[i] == r"%":
                        baseName = self.exp[idx].firstRun(localE)
                        if baseName[0] == "symbol":
                            Quadruple.QDict.append(Quadruple(OperatorQuadruple.PRINT, baseName[1].temp, None, None))
                        else:
                            Quadruple.QDict.append(Quadruple(OperatorQuadruple.PRINT, baseName[1], None, None))
                        idx += 1
                        i += 1
                    elif ord(baseString[i]) == 10:
                        Quadruple.QDict.append(Quadruple(OperatorQuadruple.PRINT, f'"\\n"', None, None))
                    elif ord(baseString[i]) == 9:
                        Quadruple.QDict.append(Quadruple(OperatorQuadruple.PRINT, f'"   "', None, None))
                    elif ord(baseString[i]) == 13:
                        Quadruple.QDict.append(Quadruple(OperatorQuadruple.PRINT, f'"\\r"', None, None))
                    else:
                        Quadruple.QDict.append(Quadruple(OperatorQuadruple.PRINT, f'"{str(baseString[i])}"', None, None))
                    i += 1
            else:
                Quadruple.QDict.append(Quadruple(OperatorQuadruple.PRINT, f'"{baseString}"', None, None))
        except:
            print("problem in print")
        return ("rawvalue", 0)
