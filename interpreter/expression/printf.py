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
        if len(self.exp) > 1:
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
                if idx < len(self.exp) and baseString[i] == r"\\":
                    #trat ade recuperar el caractr siguiente:
                    try:
                        self.nextchar = "\\" +baseString[i+1]
                    except:
                        self.nextchar = "\\"
                    Quadruple.QDict.append(Quadruple(OperatorQuadruple.PRINT, f'"{self.nextchar}"', None, None))
                    i += 1
                else:
                    Quadruple.QDict.append(Quadruple(OperatorQuadruple.PRINT, f'"{str(baseString[i])}"', None, None))
                i += 1
        else:
            Quadruple.QDict.append(Quadruple(OperatorQuadruple.PRINT, f'"{baseString}"', None, None))
        return ("rawvalue", 0)
