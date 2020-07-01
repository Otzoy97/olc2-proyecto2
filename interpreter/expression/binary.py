from interpreter.instruction import Instruction
from interpreter.quadruple import Quadruple, OperatorQuadruple
from interpreter.operator import Operator
from interpreter.st import Symbol, SymbolTable

class Binary(Instruction):
    def __init__(self, exp1, op, exp2):
        self.exp1 = exp1
        self.op = op
        self.exp2 = exp2

    def firstRun(self, localE):
        pass
        