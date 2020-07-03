from interpreter.instruction import Instruction
from interpreter.quadruple import Quadruple, OperatorQuadruple
from interpreter.operator import Operator
from interpreter.st import Symbol, SymbolTable

class Unary(Instruction):
    def __init__(self, exp, op):
        self.exp = exp
        self.op = op

    def firstRun(self, localE):
        args = self.exp.firstRun(localE)
        tempName = args[1].temp if args[0] == "symbol" else args[1]
        if self.op == Operator.CASTINT:
            q0 = Quadruple(OperatorQuadruple.ASSIGNMENT, f"(int){tempName}", None, f"$t{SymbolTable.IdxTempVar}")
            SymbolTable.IdxTempVar += 1
            Quadruple.QDict.append(q0)
            return ("tempname", q0.r)
        elif self.op == Operator.CASTFLOAT:
            q0 = Quadruple(OperatorQuadruple.ASSIGNMENT, f"(float){tempName}", None, f"$t{SymbolTable.IdxTempVar}")
            SymbolTable.IdxTempVar += 1
            Quadruple.QDict.append(q0)
            return ("tempname", q0.r)
        elif self.op == Operator.CASTCHAR:
            q0 = Quadruple(OperatorQuadruple.ASSIGNMENT, f"(char){tempName}", None, f"$t{SymbolTable.IdxTempVar}")
            SymbolTable.IdxTempVar += 1
            Quadruple.QDict.append(q0)
            return ("tempname", q0.r)
        elif self.op == Operator.INCREMENT:
            q0 = Quadruple(OperatorQuadruple.PLUS, tempName, 1, tempName)
            Quadruple.QDict.append(q0)
            return ("tempname", q0.r)
        elif self.op == Operator.DECREMENT:
            q0 = Quadruple(OperatorQuadruple.MINUS, tempName, 1, tempName)
            Quadruple.QDict.append(q0)
            return ("tempname", q0.r)
        elif self.op == Operator.AMPERSAND:
            q0 = Quadruple(OperatorQuadruple.AMP, tempName, None, f"$t{SymbolTable.IdxTempVar}")
            SymbolTable.IdxTempVar += 1
            Quadruple.QDict.append(q0)
            return ("tempname", q0.r)
        elif self.op == Operator.PLUS:
            return args
        elif self.op == Operator.MINUS:
            q0 = Quadruple(OperatorQuadruple.ASSIGNMENT, f"-{tempName}", None, f"$t{SymbolTable.IdxTempVar}")
            SymbolTable.IdxTempVar += 1
            Quadruple.QDict.append(q0)
            return ("tempname", q0.r)
        elif self.op == Operator.NOTBW:
            q0 = Quadruple(OperatorQuadruple.NOTBW, tempName, None, f"$t{SymbolTable.IdxTempVar}")
            SymbolTable.IdxTempVar += 1
            Quadruple.QDict.append(q0)
            return ("tempname", q0.r)
        elif self.op == Operator.NOT:
            q0 = Quadruple(OperatorQuadruple.NOT, tempName, None, f"$t{SymbolTable.IdxTempVar}")
            SymbolTable.IdxTempVar += 1
            Quadruple.QDict.append(q0)
            return ("tempname", q0.r)