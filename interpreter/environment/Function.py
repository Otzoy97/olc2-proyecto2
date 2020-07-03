from interpreter.instruction import Instruction
from interpreter.st import SymbolTable, Symbol, SymbolType
from interpreter.dspecifier import DSpecifier

class Function(Instruction):
    def __init__(self, decSpec, declarator, cStatement, parent, row):
        self.sym = SymbolTable()
        self.decSpec = decSpec
        self.dec = declarator
        self.csta = cStatement
        self.parent = parent
        self.row = row

    def firstRun(self):
        pass

    def findSymbol(self, identifier):
        '''Busca un simbolo'''
        r = self.sym.find(identifier)
        if r == None:
            r = self.parent.findSymbol(identifier)
        return r

    def retrieveEnvironment(self):
        return self.dec[1]

    def searchForLoop(self):
        return None