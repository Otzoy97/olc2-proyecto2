from interpreter.instruction import Instruction
from interpreter.st import SymbolTable, SymbolType, Symbol
from interpreter.quadruple import Quadruple, OperatorQuadruple

class For(Instruction):
    def __init__(self, expressionInit, condition, increment, statement):
        self.sym = SymbolTable()
        self.expressionInit = expressionInit
        self.condition = condition
        self.increment = increment
        if not isinstance(statement, list):
            self.statement = [statement]
        else:
            self.statement = statement
        self.parent = None
        self.EndLabel = ""
        self.StartLabel = ""

    def firstRun(self, localE):
        #establece el entorno padre
        self.parent = localE
        #ejecuta la expresión de asignación
        self.expressionInit.firstRun(self)
        #Agrega una etiqueta de salto
        q0 = Quadruple.createLabel()
        Quadruple.QDict.append(q0)
        #Crea la etiqueta de salida
        self.EndLabel = Quadruple.createLabel()
        #Crea la etiqueta de continue
        self.StartLabel = Quadruple.createLabel()
        #ejeccuta la condición
        nameCon = self.condition.firstRun(self)
        nameCon = nameCon[1].temp if nameCon[0] == "symbol" else nameCon[1]
        #guarda la condición
        Quadruple.QDict.append(Quadruple(OperatorQuadruple.IF, f"!{nameCon}", None, self.EndLabel.r))
        #ejecuta los statements
        for sta in self.statement:
            sta.firstRun(self)
        #coloca la etiqueta del continuea
        Quadruple.QDict.append(self.StartLabel)
        #ejecuta el incremento
        self.increment.firstRun(self)
        #inserta un goto
        Quadruple.QDict.append(Quadruple(OperatorQuadruple.GOTO, q0.r, None, None,))
        #inserta la etiqueta de salida
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