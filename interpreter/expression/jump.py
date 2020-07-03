from interpreter.instruction import Instruction
from interpreter.st import Symbol, SymbolTable
from interpreter.quadruple import Quadruple, OperatorQuadruple
from interpreter.operator import Operator

class Jump(Instruction):
    def __init__(self, op, exp):
        self.exp = exp
        self.op = op

    def firstRun(self, localE):
        if self.op == Operator.CONTINUE_:
            #busca por un entorno padre que sea loop
            ret = localE.searchForLoop()
            if ret != None:
                #inserta una etiqueta goto
                Quadruple.QDict.append(Quadruple(OperatorQuadruple.GOTO, ret[0], None, None))
            return ("rawvalue", 0)
        elif self.op == Operator.BREAK_:
            #busca por un entorno padre que sea loop
            ret = localE.searchForLoop()
            if ret != None:
                #inserta una etiqueta goto
                Quadruple.QDict.append(Quadruple(OperatorQuadruple.GOTO, ret[1], None, None))
            return ("rawvalue", 0)
        elif self.op == Operator.RETURN_:
            if self.exp == None:
                Quadruple.QDict.append(Quadruple(OperatorQuadruple.GOTO, f"ret0", None, None))
            else:
                expName = self.exp.firstRun(localE)
                expName = expName[1].temp if expName[0] == "symbol"  else expName[1]
                Quadruple.QDict.append(Quadruple(OperatorQuadruple.ASSIGNMENT, expName, None, "$v0"))
                Quadruple.QDict.append(Quadruple(OperatorQuadruple.GOTO, f"ret0", None, None))
            return ("rawvalue", 0)
        elif self.op == Operator.GOTO:
            Quadruple.QDict.append(Quadruple(OperatorQuadruple.GOTO, self.exp, None, None ))
            return ("rawvalue", 0)