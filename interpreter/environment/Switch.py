from interpreter.instruction import Instruction
from interpreter.st import SymbolTable, Symbol, SymbolType

class Switch(Instruction):
    def __init__(self, expression, statement, row, parent):
        self.expression = expression
        self.statement = statement
        self.row = row
        self.parent = parent
        self.sym = SymbolTable()
