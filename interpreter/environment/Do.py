from interpreter.instruction import Instruction
from interpreter.st import SymbolTable, Symbol, SymbolType

class Do(Instruction):
    def __init__(self, expression, statement, parent):
        self.sym = SymbolTable()
        self.expression = expression
        self.statement = statement
        self.parent = parent
        self.EndLabel = ""
        self.StartLabel = ""

    def firstRun(self, localE):
        pass

    def findSymbol(self, identifier):
        '''Busca un simbolo'''
        r = self.sym.find(identifier)
        if r == None:
            r = self.parent.findSymbol(identifier)
        return r

    def retrieveEnvironment(self):
        return self.parent.retrieveEnvironment()

    def searchForLoop(self):
        return (self.StartLabel, self.EndLabel)