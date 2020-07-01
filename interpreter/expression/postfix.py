from interpreter.instruction import Instruction
from interpreter.expression.primary import Primary
from interpreter.operator import Operator
from interpreter.st import Symbol, SymbolTable
from interpreter.quadruple import Quadruple, OperatorQuadruple
from copy import deepcopy

class Postfix(Instruction):
    def __init__(self, exp, acc, row):
        self.exp = exp
        self.acc = acc
        self.row = row
        self.access = []

    def firstRun(self, localE):
        t0 = self.exp.firstRun(localE)
        if t0[0] == "rawvalue":
            return t0
        for acc in self.acc:
            if acc[0] == Operator.CALL:
                for param in acc[1]:
                    #Recupera los parametros
                    p = param.firstRun(localE)
                    arg1 = p[1].temp if p[0] == "symbol" and p[1].type == 1 else p[1]
                    q0 = Quadruple(OperatorQuadruple.ASSIGNMENT,
                                   arg1, None, "$s0[$sp]")
                    q1 = Quadruple(OperatorQuadruple.PLUS, "$sp", 1, "$sp")
                    Quadruple.QDict.append(q0)
                    Quadruple.QDict.append(q1)
                q2 = Quadruple(OperatorQuadruple.GOTO, t0[0].temp, None, None)
                Quadruple.QDict.append(q2)
                q3 = Quadruple(OperatorQuadruple.LABEL,
                               t0[0].returnLabel, None, None)
                Quadruple.QDict.append(q3)
                return ("rawvalue", "$v0")
            elif acc[0] == Operator.STRUCTACCESS:
                self.access.append(str(f'"{acc[1]}"'))
            elif acc[0] == Operator.ARRAYACCESS:
                p = acc[1].firstRun(localE)
                arg1 = 0
                if p[0] == "symbol" and p[1].type == 1:  # debe ser una variable
                    arg1 = p[1].temp
                elif p[0] == "rawvalue":
                    arg1 = p[1]
                self.access.append(arg1)
            elif acc[0] == Operator.INCREMENT:
                # crea un nuevo cuadruple, aumenta el contador de temporales
                # incrementa el valor temporal t
                # devuelve el nombre del valor asignado inicialmente en q0
                arg1 = t0[1].temp if t0[0] == "symbol" else t0[1]
                q0 = Quadruple(OperatorQuadruple.ASSIGNMENT,
                               arg1, None, f"$t{SymbolTable.IdxTempVar}")
                Quadruple.QDict.append(q0)
                SymbolTable.IdxTempVar += 1
                Quadruple.QDict.append(
                    Quadruple(OperatorQuadruple.PLUS, arg1, 1, arg1))
                return ("tempname", q0.r)
            elif acc[0] == Operator.DECREMENT:
                arg1 = t0[1].temp if t0[0] == "symbol" else t0[1]
                q0 = Quadruple(OperatorQuadruple.ASSIGNMENT,
                               arg1, None, f"$t{SymbolTable.IdxTempVar}")
                Quadruple.QDict.append(q0)
                SymbolTable.IdxTempVar += 1
                Quadruple.QDict.append(
                    Quadruple(OperatorQuadruple.MINUS, arg1, 1, arg1))
                return ("tempname", q0.r)
        if len(self.access) > 0:
            arracc = ""
            for i in self.access:
                arracc += f"[{i}]"
            q0 = Quadruple(OperatorQuadruple.ASSIGNMENT,  f"{t0[1].temp}{arracc}", None, f"$t{SymbolTable.IdxTempVar}")
            SymbolTable.IdxTempVar += 1
            Quadruple.QDict.append(q0)
            return ("tempname", q0.r)
        return("rawvalue", 0)