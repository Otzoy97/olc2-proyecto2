from interpreter.instruction import Instruction
from interpreter.st import SymbolTable, Symbol
from interpreter.quadruple import Quadruple, OperatorQuadruple
from interpreter.st import SymbolTable, Symbol

class If(Instruction):
    def __init__(self, expression, statement, else_statement):
        self.expression = expression
        self.statement = statement
        if not isinstance(statement, list):
            self.statement = [statement]
        else:
            self.statement = statement
        if else_statement != None:
            if not isinstance(statement, list):
                self.else_statement = [else_statement]
            else:
                self.else_statement = else_statement
        else:
            self.else_statement = []
        self.parent = None
        self.sym = SymbolTable()

    def firstRun(self, localE):
        self.parent = localE
        expname = self.expression.firstRun(self)
        expname = expname[1].temp if expname[0] == "symbol" else expname[1]
        qlabel = Quadruple.createLabel()
        Quadruple.QDict.append(Quadruple(OperatorQuadruple.IF, f"!{expname}", None, qlabel.r))
        for sta in self.statement:
            sta.firstRun(localE)
        Quadruple.QDict.append(qlabel)
        for sta in self.else_statement:
            sta.firstRun(localE)
            
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