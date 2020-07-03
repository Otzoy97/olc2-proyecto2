from interpreter.instruction import Instruction
from interpreter.st import SymbolTable, Symbol
from interpreter.quadruple import Quadruple, OperatorQuadruple
from interpreter.st import SymbolTable, Symbol

class While(Instruction):
    def __init__(self, expression, statement, parent):
        self.expression = expression
        self.statement = statement
        self.parent = parent
        self.sym = SymbolTable()
        self.EndLabel = ""
        self.StartLabel = ""
    
    def firstRun(self, localE):
        #establece el entorno padre
        self.parent = localE
        #crea la etiqueta a donde deberá saltar un continue
        self.StartLabel = Quadruple.createLabel()
        #crea la etiqueta a donde deberá saltar un break
        self.EndLabel = Quadruple.createLabel()
        #agrega la etiqueta inicial
        Quadruple.QDict.append(self.StartLabel)
        #ejecuta la expression
        expName = self.expression.firstRun(self)
        expName = expName[1].temp if expName[0] == "symbol" else expName[1]
        #crea la etiqueta if
        Quadruple.QDict.append(Quadruple(OperatorQuadruple.IF, f"!{expName}", None, self.EndLabel.r))
        #ejecuta el statemen
        for sta in self.statement:
            sta.firstRun(self)
        #coloca el goto
        Quadruple.QDict.append(Quadruple(OperatorQuadruple.GOTO,self.StartLabel.r, None,None ))
        #coloca la etiqueta del break
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