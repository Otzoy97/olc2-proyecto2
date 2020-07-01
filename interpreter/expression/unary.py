from interpreter.instruction import Instruction
from interpreter.quadruple import Quadruple, OperatorQuadruple
from interpreter.operator import Operator
from interpreter.st import Symbol, SymbolTable

class Unary(Instruction):
    def __init__(self, exp, acc, row):
        self.exp = exp
        self.acc = acc
        self.row = row

    def firstRun(self, localE):
        t0 = self.exp.firstRun(localE)
        for acc in self.acc:
            if acc[0] == Operator.INCREMENT and (t0[0] == "tempname" or t0[0] == "symbol"):
                tempOrSymbol = t0[1] if t0[0] == "tempname" else t0[1].temp
                Quadruple.QDict.append(Quadruple(OperatorQuadruple.PLUS, tempOrSymbol, 1, tempOrSymbol))
                return ("tempname", tempOrSymbol)
            elif acc[0] == Operator.DECREMENT and (t0[0] == "tempname" or t0[0] == "symbol"):
                tempOrSymbol = t0[1] if t0[0] == "tempname" else t0[1].temp
                Quadruple.QDict.append(Quadruple(OperatorQuadruple.MINUS, tempOrSymbol, 1, tempOrSymbol))
                return ("tempname", tempOrSymbol)
            elif acc[0] == Operator.AMPERSAND and (t0[0] == "tempname" or t0[0] == "symbol"):
                tempOrSymbol = t0[1] if t0[0] == "tempname" else t0[1].temp
                q0 = Quadruple(OperatorQuadruple.AMP, tempOrSymbol, None, f"$t{SymbolTable.IdxTempVar}")
                Quadruple.QDict.append(q0)
                SymbolTable.IdxTempVar += 1
                return ("tempname", q0.r)
            elif acc[0] == Operator.UPLUS:
                #tempOrSymbol = t0[1] if t0[0] == "tempname" or t0[0] == "rawvalue" else t0[1].temp
                return t0
            elif acc[0] == Operator.UMINUS:
                tempOrSymbol = t0[1] if t0[0] == "tempname" or t0[0] == "rawvalue" else t0[1].temp
                q0 = Quadruple(OperatorQuadruple.ASSIGNMENT, f"-{tempOrSymbol}", None, f"$t{SymbolTable.IdxTempVar}")
                Quadruple.QDict.append(q0)
                SymbolTable.IdxTempVar += 1
                return ("tempname", q0.r)
            elif acc[0] == Operator.NOTBW:
                tempOrSymbol = t0[1] if t0[0] == "tempname" or t0[0] == "rawvalue" else t0[1].temp
                q0 = Quadruple(OperatorQuadruple.ASSIGNMENT, f"~{tempOrSymbol}", None, f"$t{SymbolTable.IdxTempVar}")
                Quadruple.QDict.append(q0)
                SymbolTable.IdxTempVar += 1
                return ("tempname", q0.r)
            elif acc[0] == Operator.NOT:
                tempOrSymbol = t0[1] if t0[0] == "tempname" or t0[0] == "rawvalue" else t0[1].temp
                q0 = Quadruple(OperatorQuadruple.ASSIGNMENT, f"!{tempOrSymbol}", None, f"$t{SymbolTable.IdxTempVar}")
                Quadruple.QDict.append(q0)
                SymbolTable.IdxTempVar += 1
                return ("tempname", q0.r)
        return t0