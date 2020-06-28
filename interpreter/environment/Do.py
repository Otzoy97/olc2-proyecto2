from interpreter.instruction import Instruction
from interpreter.st import SymbolTable, Symbol, SymbolType

class Do(Instruction):
    def __init__(self, expression, statement, row, parent):
        self.sym = SymbolTable()
        self.expression = expression
        self.statement = statement
        self.row = row
        self.parent = parent

    def firstRun(self):
        pass