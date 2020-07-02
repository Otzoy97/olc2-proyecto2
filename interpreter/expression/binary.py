from interpreter.instruction import Instruction
from interpreter.quadruple import Quadruple, OperatorQuadruple
from interpreter.operator import Operator
from interpreter.st import Symbol, SymbolTable

class Binary(Instruction):
    def __init__(self, exp1, op, exp2):
        self.exp1 = exp1
        self.op = op
        self.exp2 = exp2

    def firstRun(self, localE, parent):
        arg1 = self.exp1.firstRun(localE, parent)
        arg2 = self.exp2.firstRun(localE, parent)
        tempName1 = arg1[1].temp if arg1[0] == "symbol" else arg1[1]
        tempName2 = arg2[1].temp if arg2[0] == "symbol" else arg2[1]
        q0 = Quadruple(self.setOperator(), tempName1, tempName2, f"$t{SymbolTable.IdxTempVar}")
        SymbolTable.IdxTempVar += 1
        Quadruple.QDict.append(q0)
        return("tempname", q0.r)
    
    def setOperator(self):
        if self.op == Operator.OR:
            return OperatorQuadruple.OR
        elif self.op == Operator.AND:
            return OperatorQuadruple.AND
        elif self.op == Operator.ORBW:
            return OperatorQuadruple.ORBW
        elif self.op == Operator.XORBW:
            return OperatorQuadruple.XORBW
        elif self.op == Operator.ANDBW:
            return OperatorQuadruple.ANDBW
        elif self.op == Operator.EQ:
            return OperatorQuadruple.EQ
        elif self.op == Operator.NEQ:
            return OperatorQuadruple.NEQ
        elif self.op == Operator.LS:
            return OperatorQuadruple.LS
        elif self.op == Operator.GR:
            return OperatorQuadruple.GR
        elif self.op == Operator.LSE:
            return OperatorQuadruple.LSE
        elif self.op == Operator.GRE:
            return OperatorQuadruple.GRE
        elif self.op == Operator.SHL:
            return OperatorQuadruple.SHL
        elif self.op == Operator.SHR:
            return OperatorQuadruple.SHR
        elif self.op == Operator.PLUS:
            return OperatorQuadruple.PLUS
        elif self.op == Operator.MINUS:
            return OperatorQuadruple.MINUS
        elif self.op == Operator.TIMES:
            return OperatorQuadruple.TIMES
        elif self.op == Operator.QUOTIENT:
            return OperatorQuadruple.QUOTIENT
        elif self.op == Operator.REMAINDER:
            return OperatorQuadruple.REMAINDER
