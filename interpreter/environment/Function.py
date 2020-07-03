from interpreter.instruction import Instruction
from interpreter.st import SymbolTable, Symbol, SymbolType
from interpreter.dspecifier import DSpecifier
from interpreter.quadruple import Quadruple, OperatorQuadruple

class Function(Instruction):
    def __init__(self, decSpec, declarator, cStatement, row):
        self.sym = SymbolTable()
        self.decSpec = decSpec #no se usa
        self.dec = declarator
        self.csta = cStatement
        self.parent = None
        self.row = row

    def firstRun(self, localE):
        #establece el entorno padre
        self.parent = localE
        #recupera el identificador para la función
        functionId = self.dec[0]
        #guarda el sybolo en la tabla padre
        func = Symbol(functionId, None, SymbolType.FUNCTION, self.parent.retrieveEnvironment(),self.row)
        func.parlist = self.dec[1]
        self.parent.sym.addFunction(functionId, func)
        #almacena el número de parametros
        noParams = len(self.dec[1])
        counterParams = 0
        #recorre los parametros y los guarda en la tabla de simbolos local
        for param in self.dec[1]:
            s = Symbol("$s0[$ra]",None,SymbolType.VARIABLE,functionId, self.row)
            #indica que es una variable de función (local)
            s.param = True
            #establece el indice del parametro
            s.idxParam = noParams - counterParams
            counterParams += 1
            #agrega el symbolo a la tabla de simbolos locales
            self.sym.add(param, s)
        #añade la etiqueta de la función
        Quadruple.QDict.append(Quadruple(OperatorQuadruple.LABEL, None, None, functionId))
        #ejecuta los statements
        for sta in self.csta:
            sta.firstRun(self)
        #añade un etiqueta de retorno
        Quadruple.QDict.append(Quadruple(OperatorQuadruple.GOTO, "ret0", None, None))
        
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