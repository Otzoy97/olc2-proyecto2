from interpreter.instruction import Instruction
from interpreter.st import SymbolTable, Symbol
from interpreter.dspecifier import DSpecifier
from interpreter.quadruple import Quadruple, OperatorQuadruple

class Switch(Instruction):
    def __init__(self, expression, statement):
        self.expression = expression
        self.statement = statement
        self.parent = None
        self.sym = SymbolTable()
        self.ToCompare = None

    def firstRun(self, localE):
        self.parent = localE
        pass

    def findSymbol(self, identifier):
        '''Busca un simbolo'''
        r = self.sym.find(identifier)
        if r == None:
            r = self.parent.findSymbol(identifier)
        return r

    def searchForLoop(self):
        return self.parent.searchForLoop()

    def valueToCompare(self):
        return self.ToCompare

class Label(Instruction):
    def __init__(self, identifier, statement):
        self.identifier = identifier
        self.statement = statement
        self.parent = None
        self.sym = SymbolTable()

    def firstRun(self, localE):
        self.parent = localE
        #Crea una etiqueta con el nombre de identifier
        q0 = Quadruple.createLabel(self.identifier)
        Quadruple.QDict.append(q0)
        #ejecuta los statement
        for sta in self.statement:
            sta.firstRun(self)

    def findSymbol(self, identifier):
        '''Busca un simbolo'''
        r = self.sym.find(identifier)
        if r == None:
            r = self.parent.findSymbol(identifier)
        return r

    def retrieveEnvironment(self):
        return self.parent.retrieveEnvironment()

    def searchForLoop(self):
        return self.parent.searchForLoop()

class Case(Instruction):
    def __init__(self, expression, statement):
        self.expression = expression
        self.statement = statement
        self.parent = None
        self.sym = SymbolTable()

    def firstRun(self, localE):
        self.parent = localE
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
        return self.parent.searchForLoop()
