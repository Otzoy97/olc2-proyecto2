from interpreter.instruction import Instruction
from interpreter.operator import Operator
from interpreter.quadruple import Quadruple, OperatorQuadruple
from interpreter.st import Symbol, SymbolTable

class Assignment(Instruction):
    def __init__(self, exp1, assignment_type, exp2, row):
        self.exp1 = exp1
        self.assignment_type = assignment_type
        self.exp2 = exp2
        self.row = row
    
    def firstRun(self, localE):
        exp2Name = self.exp2.firstRun(localE)
        exp2Name = exp2Name[1].temp if exp2Name[0] == "symbol" else exp2Name[1]
        exp1Name = self.exp1.firstRun(localE)
        exp1Name = exp1Name[1].temp if exp1Name[0] == "symbol" else exp1Name[1]
        if Operator.ASSIGN == self.assignment_type:
            q0 = Quadruple(OperatorQuadruple.ASSIGNMENT,exp2Name,None,exp1Name)
            Quadruple.QDict.append(q0)
            return ("tempname", q0.r)
        elif Operator.TIMESA == self.assignment_type:
            q0 = Quadruple(OperatorQuadruple.TIMES, exp1Name, exp2Name, exp1Name)
            Quadruple.QDict.append(q0)
            return ("tempname", q0.r)
        elif Operator.QUOTA == self.assignment_type:
            q0 = Quadruple(OperatorQuadruple.QUOTIENT, exp1Name, exp2Name, exp1Name)
            Quadruple.QDict.append(q0)
            return ("tempname", q0.r)
        elif Operator.REMA == self.assignment_type:
            q0 = Quadruple(OperatorQuadruple.REMAINDER, exp1Name, exp2Name, exp1Name)
            Quadruple.QDict.append(q0)
            return ("tempname", q0.r)
        elif Operator.PLUSA == self.assignment_type:
            q0 = Quadruple(OperatorQuadruple.PLUS, exp1Name, exp2Name, exp1Name)
            Quadruple.QDict.append(q0)
            return ("tempname", q0.r)
        elif Operator.MINUSA == self.assignment_type:
            q0 = Quadruple(OperatorQuadruple.MINUS, exp1Name, exp2Name, exp1Name)
            Quadruple.QDict.append(q0)
            return ("tempname", q0.r)
        elif Operator.SHRA == self.assignment_type:
            q0 = Quadruple(OperatorQuadruple.SHR, exp1Name, exp2Name, exp1Name)
            Quadruple.QDict.append(q0)
            return ("tempname", q0.r)
        elif Operator.SHLA == self.assignment_type:
            q0 = Quadruple(OperatorQuadruple.SHL, exp1Name, exp2Name, exp1Name)
            Quadruple.QDict.append(q0)
            return ("tempname", q0.r)
        elif Operator.ANDBWA == self.assignment_type:
            q0 = Quadruple(OperatorQuadruple.ANDBW, exp1Name, exp2Name, exp1Name)
            Quadruple.QDict.append(q0)
            return ("tempname", q0.r)
        elif Operator.XORBWA == self.assignment_type:
            q0 = Quadruple(OperatorQuadruple.XORBW, exp1Name, exp2Name, exp1Name)
            Quadruple.QDict.append(q0)
            return ("tempname", q0.r)
        elif Operator.ORBWA == self.assignment_type:
            q0 = Quadruple(OperatorQuadruple.ORBW, exp1Name, exp2Name, exp1Name)
            Quadruple.QDict.append(q0)
            return ("tempname", q0.r)