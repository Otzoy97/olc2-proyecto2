from interpreter.instruction import Instruction
from interpreter.quadruple import Quadruple, OperatorQuadruple
from interpreter.st import SymbolTable, Symbol

class Conditional(Instruction):
    def __init__(self, exp1, exp2, exp3, row):
        self.exp1 = exp1 #condition
        self.exp2 = exp2 #val_true
        self.exp3 = exp3 #val_false
        self.row = row

    def firstRun(self, localE):
        #solve condition
        cond = self.exp1.firstRun(localE)
        val_true = self.exp2.firstRun(localE)
        ## $tn = val_true
        ## if !cond goto Ln
        ## $tn = val_false
        ## Ln:
        condName = cond[1].temp if cond[0] == "symbol" else cond[1]
        val_trueName = ""
        #
        # verifica tipos
        #
        if val_true[0] == "symbol":
            val_trueName = val_true[1].temp
        elif val_true[0] == "rawvalue":
            q0 = Quadruple(OperatorQuadruple.ASSIGNMENT, val_true[1], None, f"$t{SymbolTable.IdxTempVar}")
            SymbolTable.IdxTempVar += 1
            Quadruple.QDict.append(q0)
            val_trueName = q0.r
        elif val_true[0] == "tempname":
            val_trueName = val_true[1]
        #
        # crea la etiqueta y la instrucción IF
        #
        q2 = Quadruple.createLabel()
        q1 = Quadruple(OperatorQuadruple.IF,f"{condName}", "",q2.r)
        Quadruple.QDict.append(q1)
        val_false = self.exp3.firstRun(localE)
        #
        # verifica tipos
        #
        if val_false[0] == "symbol":
            q3 = Quadruple(OperatorQuadruple.ASSIGNMENT, val_false[1].temp, None, val_trueName)
            Quadruple.QDict.append(q3)
        elif val_false[0] == "rawvalue":
            q3 = Quadruple(OperatorQuadruple.ASSIGNMENT, val_false[1], None, val_trueName)
            Quadruple.QDict.append(q3)
        elif val_false[0] == "tempname":
            q3 = Quadruple(OperatorQuadruple.ASSIGNMENT, val_false[1], None, val_trueName)
            Quadruple.QDict.append(q3)
        Quadruple.QDict.append(q2)
        return ("tempname", val_trueName)
