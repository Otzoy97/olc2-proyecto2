from interpreter.instruction import Instruction
from interpreter.expression.primary import Primary
from interpreter.operator import Operator
from interpreter.st import Symbol, SymbolTable
from interpreter.quadruple import Quadruple, OperatorQuadruple
from copy import deepcopy

class Postfix(Instruction):
    def __init__(self, exp1, op, exp2):
        self.exp1 = exp1
        self.op = op
        self.exp2 = exp2
        self.access = []

    def firstRun(self, localE, parent):
        arg1 = self.exp1.firstRun(localE, parent)
        arg1Name = arg1[1].temp if arg1[0] == "symbol" else arg1[1]
        if self.op == Operator.ARRAYACCESS:
            exp = self.exp2.firstRun(localE, parent)
            expName = exp[1].temp if exp[0] == "symbol" else exp[1]
            return ("tempname", f"{arg1Name}[{expName}]")
        elif self.op == Operator.STRUCTACCESS:
            return ("tempname", f"{arg1Name}[\"{self.exp2}\"]")
        elif self.op == Operator.CALL:
            if arg1[0] !=  "symbol":
                return ("rawvalue", 0)
            self.noParam = 1
            for param in self.exp2:
                self.noParam += 1
                p = param.firstRun(localE, parent)
                pName = p[1].temp if p[0] == "symbol" else p[1]
                Quadruple.QDict.append(Quadruple(OperatorQuadruple.PLUS, "$sp", 1, "$sp"))
                Quadruple.QDict.append(Quadruple(OperatorQuadruple.ASSIGNMENT, pName, None, "$s0[$sp]"))
            Quadruple.QDict.append(Quadruple(OperatorQuadruple.PLUS, "$sp", 1, "$sp"))
            retlbl = Quadruple.addReturnLabel()
            Quadruple.QDict.append(Quadruple(OperatorQuadruple.ASSIGNMENT, retlbl, None, "$s0[$sp]"))
            Quadruple.QDict.append(Quadruple(OperatorQuadruple.GOTO, arg1Name, None, None))
            Quadruple.QDict.append(Quadruple(OperatorQuadruple.LABEL, f"ret{retlbl}", None, None))
            Quadruple.QDict.append(Quadruple(OperatorQuadruple.MINUS, "$sp", self.noParam, "$sp"))
            return ("tempname", "$v0")
        elif self.op == Operator.INCREMENT:
            q0 = Quadruple(OperatorQuadruple.ASSIGNMENT, arg1Name, None, f"$t{SymbolTable.IdxTempVar}")
            Quadruple.QDict.append(q0)
            SymbolTable.IdxTempVar += 1
            Quadruple.QDict.append(Quadruple(OperatorQuadruple.PLUS, arg1Name, 1, arg1Name))
            return ("tempname", q0.r)
        elif self.op == Operator.DECREMENT:
            q0 = Quadruple(OperatorQuadruple.ASSIGNMENT, arg1Name, None, f"$t{SymbolTable.IdxTempVar}")
            Quadruple.QDict.append(q0)
            SymbolTable.IdxTempVar += 1
            Quadruple.QDict.append(Quadruple(OperatorQuadruple.MINUS, arg1Name, 1, arg1Name))
            return ("tempname", q0.r)