from interpreter.instruction import Instruction
from interpreter.expression.struct import Struct
from interpreter.st import Symbol, SymbolTable, SymbolType
from interpreter.quadruple import Quadruple, OperatorQuadruple
from interpreter.expression.assignment import Assignment

class Declaration(Instruction):
    def __init__(self, exp, row):
        self.exp = exp
        self.row = row

    def firstRun(self, localE, parent):
        '''Ejecuta la primera pasada recuperando los
        valores de asignación y nombre'''
        dec_spec = self.exp[0]
        if isinstance(dec_spec, Struct):
            # Es un struct
            #reccore la lista de declaración para obtener valores
            for struct_dec in self.exp[1:]:
                sym = Symbol(f"$t{SymbolTable.IdxTempVar}")
                sym.environment = parent.retrieveEnvironment()
                sym.row = self.row
                sym.type = SymbolType.STRUCT
                SymbolTable.IdxTempVar += 1
                Quadruple.QDict.append(Quadruple(OperatorQuadruple.ASSIGNMENT, "array()", None, sym.temp))
                localE.sym.add(struct_dec[0], sym)
        else:
            for declarator in self.exp[1:]:
                self.__sym = Symbol(f"$t{SymbolTable.IdxTempVar}")
                self.__sym.row = self.row
                self.__sym.type = SymbolType.VARIABLE
                self.__sym.environment = parent.retrieveEnvironment()
                SymbolTable.IdxTempVar += 1
                # Es otro tipo
                self.id_ = declarator[0]
                # Siempre es una lista de assignment o None
                dimension_ = declarator[1]
                if dimension_ != None:
                    self.__sym.type = SymbolType.ARRAY #variable tipo array
                    self.__sym.value = [] #inicializa la lista
                    self.values = [] #almacenará los valores del arreglo
                    q0 = Quadruple(OperatorQuadruple.ASSIGNMENT, "array()", None, self.__sym.temp)
                    for assig_dim in dimension_:
                        res = assig_dim.firstRun(localE, parent)
                        #almacena las dimensiones
                        self.__sym.dimension.append(res[1]) 
                    if len(declarator) == 2:
                        self.linealizar(self.__sym.dimension,0,"") 
                    else:
                        value_ = declarator[2]
                        if isinstance(value_, list):
                            Quadruple.QDict.append(q0)
                            for values_dim in value_:
                                res = values_dim.firstRun(localE, parent)
                                resName = res[1].temp if res[0] == "symbol" else res[1]
                                self.values.append(resName)
                            self.linealizar(self.__sym.dimension, 0, "")
                        else:
                            #es un valor plano
                            self.__sym.type = SymbolType.VARIABLE
                            valueSolve = declarator[2].firstRun(localE, parent)
                            nameValueSolve = valueSolve[1].temp if valueSolve[0] == "symbol" else valueSolve[1]
                            self.__sym.value = nameValueSolve
                            Quadruple.QDict.append(Quadruple(OperatorQuadruple.ASSIGNMENT, nameValueSolve, None, self.__sym.temp))                        
                    localE.sym.add(self.id_, self.__sym)
                    return
                if len(declarator) == 2:
                    localE.sym.add(self.id_, self.__sym)
                    Quadruple.QDict.append(Quadruple(OperatorQuadruple.ASSIGNMENT, 0, None, self.__sym.temp))
                else:
                    #es un valor plano
                    valueSolve = declarator[2].firstRun(localE, parent)
                    nameValueSolve = valueSolve[1].temp if valueSolve[0] == "symbol" else valueSolve[1]
                    self.__sym.value = nameValueSolve
                    Quadruple.QDict.append(Quadruple(OperatorQuadruple.ASSIGNMENT, nameValueSolve, None, self.__sym.temp))
                localE.sym.add(self.id_, self.__sym)

    def linealizar(self, arr, idx, cda):
        if len(arr) <= idx:
            temp = 0
            if len(self.values) > 0:
                temp = self.values.pop(0)
            Quadruple.QDict.append(Quadruple(OperatorQuadruple.ASSIGNMENT, temp, None, f"{self.__sym.temp}{cda}"))
            self.__sym.value.append(temp)
            return
        for i in range(0, arr[idx]):
            cda += f"[{i}]"
            self.linealizar(arr, idx+1, cda)
            cda = cda[0:-3]