from interpreter.instruction import Instruction
from interpreter.st import SymbolTable, Symbol, SymbolType

class If(Instruction):
    def __init__(self, expression, statement, else_statement, row, parent):
        self.expression = expression
        self.statement = statement
        self.else_statement = statement
        self.row = row
        self.parent = parent
        self.sym = SymbolTable()


    def findSymbol(self, identifier):
        '''Busca un simbolo'''
        r = self.sym.find(identifier)
        if r == None:
            r = self.parent.findSymbol(identifier)
        return r

    def retrieveEnvironment(self):
        return self.parent.retrieveEnvironment()