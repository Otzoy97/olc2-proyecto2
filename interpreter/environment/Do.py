from interpreter.instruction import Instruction
from interpreter.st import SymbolTable, Symbol, SymbolType
from interpreter.quadruple import Quadruple, OperatorQuadruple
from interpreter.st import SymbolTable, Symbol

class Do(Instruction):
    def __init__(self, expression, statement):
        self.sym = SymbolTable()
        self.expression = expression
        self.statement = statement
        self.parent = None
        self.EndLabel = ""
        self.StartLabel = ""

    def firstRun(self, localE):
        self.parent = localE
        #establece la etiqueta a donde la condición deberá saltar
        slabel = Quadruple.createLabel() 
        #etablece la etiqueta a donde un continue podrá saltar
        self.StartLabel = Quadruple.createLabel()
        #establece la etiqueta final a donde un break podría saltar
        self.EndLabel = Quadruple.createLabel()
        #almacena la etiqueta inicial
        Quadruple.QDict.append(slabel)
        #ejecuta el statement
        for sta in self.statement:
            sta.firstRun(self)
        #almacena la etiqueta del continue
        Quadruple.QDict.append(self.StartLabel)
        #ejecuta la condición
        expname = self.expression.firstRun(self)
        expname = expname[1].temp if expname[0] == "symbol" else expname[1]
        #almacena la expresión de condición
        Quadruple.QDict.append(Quadruple(OperatorQuadruple.IF, expname, None, slabel.r))
        #almacena la etiqueta de salida
        Quadruple.QDict.append(self.EndLabel)
        
    def findSymbol(self, identifier):
        '''Busca un simbolo'''
        r = self.sym.find(identifier)
        if r == None:
            r = self.parent.findSymbol(identifier)
        return r

    def retrieveEnvironment(self):
        return self.parent.retrieveEnvironment()

    def searchForLoop(self):
        return (self.StartLabel.r, self.EndLabel.r)