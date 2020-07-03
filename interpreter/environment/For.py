from interpreter.instruction import Instruction
from interpreter.st import SymbolTable, SymbolType, Symbol
from interpreter.quadruple import Quadruple, OperatorQuadruple

class For(Instruction):
    def __init__(self, expressionInit, condition, increment, statement, parent):
        self.sym = SymbolTable()
        self.expressionInit = expressionInit
        self.condition = condition
        self.increment = increment
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