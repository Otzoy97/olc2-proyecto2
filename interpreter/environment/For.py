from interpreter.instruction import Instruction
from interpreter.st import SymbolTable, SymbolType, Symbol

class For(Instruction):
    def __init__(self, expressionInit, condition, increment, statement, row, parent):
        self.sym = SymbolTable()
        self.expressionInit = expressionInit
        self.condition = condition
        self.increment = increment
        self.statement = statement
        self.parent = parent
        self.row = row