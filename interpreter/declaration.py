from interpreter.instruction import Instruction
from interpreter.expression.struct import Struct
from interpreter.st import Symbol, SymbolTable
from interpreter.quadruple import Quadruple, OperatorQuadruple
from interpreter.expression.assignment import Assignment

class Declaration(Instruction):
    def __init__(self, exp, row):
        self.exp = exp
        self.row = row

    def firstRun(self, localE):
        '''Ejecuta la primera pasada recuperando los
        valores de asignación y nombre'''
        dec_spec = self.exp[0]
        declarator = self.exp[1]
        self.__sym = Symbol(f"$t{SymbolTable.IdxTempVar}")
        self.__sym.row = self.row
        self.__sym.type = 1
        SymbolTable.IdxTempVar += 1
        if isinstance(dec_spec, Struct):
            # Es un struct
            pass
        else:
            # Es otro tipo
            self.id_ = declarator[0]
            # Siempre es una lista de assignment o None
            dimension_ = declarator[1]
            if dimension_ != None:
                self.__sym.type = 3 #variable tipo array
                self.__sym.value = [] #inicializa la lista
                self.values = [] #almacenará los valores del arreglo
                Quadruple.QDict.append(Quadruple(OperatorQuadruple.ASSIGNMENT, "array()", None, self.__sym.temp))
                for assig_dim in dimension_:
                    res = assig_dim.firstRun(localE)
                    #almacena las dimensiones
                    self.__sym.dimension.append(res[1]) 
                if len(declarator) == 2:
                    self.linealizar(self.__sym.dimension,0,"") 
                else:
                    value_ = declarator[2]
                    if isinstance(value_, list):
                        for values_dim in value_:
                            res = values_dim.firstRun(localE)
                            resName = res[1].temp if res[0] == "symbol" else res[1]
                            self.values.append(resName)
                        self.linealizar(self.__sym.dimension, 0, "")
            if len(declarator) == 2:
                localE.add(self.id_, self.__sym)
            else:
                #es un valor plano
                if isinstance(declarator[2], Assignment):
                    valueSolve = value_.firstRun(localE)
                    nameValueSolve = valueSolve[1].temp if valueSolve[0] == "symbol" else valueSolve[1]
                    self.__sym.value = nameValueSolve
                    Quadruple.QDict.append(Quadruple(OperatorQuadruple.ASSIGNMENT, nameValueSolve, None, self.__sym.temp))
        localE.add(self.id_, self.__sym)

    def linealizar(self, arr, idx, cda):
        if len(arr) <= idx:
            temp = 0
            if len(self.values) > 0:
                temp = self.values.pop(0)
            Quadruple.QDict.append(Quadruple(OperatorQuadruple.ASSIGNMENT, temp, None, f"{self.__sym.temp}{cda}"))
            self.__sym.value.append(temp)
        for i in range(0, arr[idx]):
            cda += f"[{i}]"
            self.linealizar(arr, idx+1, cda)
            cda = cda[0:-3]