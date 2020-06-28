from interpreter.instruction import Instruction
from interpreter.st import SymbolTable, Symbol, SymbolType
from interpreter.dspecifier import DSpecifier

class Function(Instruction):
    def __init__(self, decSpec, declarator, cStatement, row):
        self.sym = SymbolTable()
        self.decSpec = decSpec
        self.dec = declarator
        self.csta = cStatement
        self.row = row

    def firstRun(self):
        pass